import requests
from urllib import parse
from src.util.constant import ALL_AREA_KEY, AREA_TAIL, SHOULD_UPDATE, STATE_NCOV_INFO, UPDATE_CITY, TIME_SPLIT
from src.util.log import LogSupport
import json
import pandas as pd
import re
from src.util.redis_config import connect_redis, save_json_info, load_last_info, save_json_info_as_key
import time

class TXSpider():
    def __init__(self, debug=True):
        self.req = requests.Session()
        self.log = LogSupport()
        self.re = connect_redis()
        self.debug = debug

    def main(self):
        """
        主函数
        :return:
        """
        try:
            data = self.get_raw_real_time_info()
            now_data = self.change_raw_data_format(data)
            # 加载上一次最新的数据
            last_data = load_last_info(self.re)
            if not last_data:
                save_json_info(self.re, STATE_NCOV_INFO, now_data)
                last_data = now_data
            update_city = self.parse_increase_info(now_data, last_data)
            # 如果数据有更新，则保存新数据和更新的数据
            if len(update_city) > 0:
                self.re.set(SHOULD_UPDATE, 1)
                save_json_info(self.re, STATE_NCOV_INFO, now_data)
                save_json_info_as_key(self.re, UPDATE_CITY, update_city)
                self.log.logging.info("set update city {}".format(json.dumps(update_city)))
            else:
                # self.re.set(SHOULD_UPDATE, 0)
                self.log.logging.info("no update city")
        except BaseException as e:
            self.log.logging.exception(e)

    def get_state_all_url(self):
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_global_vars'
        return url

    def get_state_all(self):
        """
        获取全国数据
        :return:
        """
        res = self.req.get(url=self.get_state_all_url(), headers=self.get_tx_header())
        if res.status_code != 200:
            self.log.logging.error("获取全国数据失败")
        data = json.loads(json.loads(res.content.decode("utf-8"))['data'])[0]
        state_dict = {}
        state_dict['confirm'] = data['confirmCount']
        state_dict['dead'] = data['deadCount']
        state_dict['heal'] = data['cure']
        state_dict['suspect'] = data['suspectCount']
        state_dict['area'] = '全国'
        state_dict['country'] = '全国'
        state_dict['city'] = '全国'
        return {'全国': state_dict}



    def get_tx_header(self):
        return {
            'host': 'view.inews.qq.com',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'referer': 'https://news.qq.com/zt2020/page/feiyan.htm'
        }

    def get_real_time_url(self):
        base_url = 'https://view.inews.qq.com/g2/getOnsInfo?'
        params = {
            'name': 'wuwei_ww_area_counts'
        }
        return base_url + parse.urlencode(params)

    def get_raw_real_time_info(self):
        """
        从腾讯新闻获取各地病例数量的实时数据
        :return:
        """
        url = self.get_real_time_url()
        header = self.get_tx_header()
        res = self.req.get(url=url, headers=header)
        if res.status_code != 200:
            self.log.logging.error("Failed to get info")
            raise ConnectionError
        content = json.loads(res.content.decode("utf-8"))
        data = json.loads(content['data'])
        return data

    def change_raw_data_format(self, data):
        """
        将原始的json_list形式的数据转为dict, 填充缺失值并按省份、国家统计数据
        :param data:
        :return:
        """
        data_dict = {}
        for item in data:
            if item['city'] == '':
                if item['area'] == '':
                    item['city'] = item['country']
                    item['area'] = item['country']
                else:
                    item['city'] = item['area']
            data_dict[item['city']] = item
        # 统计各省份情况
        data_df = pd.DataFrame(data)
        data_province = data_df.loc[:, ['area', 'confirm', 'suspect', 'dead', 'heal']]
        data_province = data_province.groupby(by='area').sum().reset_index()
        data_province.sort_values(by='confirm', ascending=False, inplace=True)
        province_json = json.loads(data_province.to_json(orient='records', force_ascii=False))
        province_json = self.fill_unknow(province_json)
        province_dict = {x['area']: x for x in province_json}
        # 合并数据并保存
        state_dict = self.get_state_all()
        data_dict.update(province_dict)
        data_dict.update(state_dict)

        self.log.logging.info("update data success---")
        self.get_all_area(data_dict)
        return data_dict

    def fill_unknow(self, data):
        for item in data:
            if 'city' not in item or item['city'] == '':
                if 'area' not in item or item['area'] == '':
                    item['city'] = item['country']
                    item['area'] = item['country']
                else:
                    item['city'] = item['area']
        return data

    def get_all_area(self, data_dict):
        """
        保存所有地区的名称，供分词用
        :param data_dict:
        :return:
        """
        all_area = data_dict.keys()
        for area in all_area:
            short = re.subn(AREA_TAIL, '', area)[0]
            self.re.sadd(ALL_AREA_KEY, short)
            self.re.sadd(ALL_AREA_KEY, area)

    def parse_increase_info(self, now_data, last_data):
        # 计算有更新的城市/省份/国家
        update_city = []
        for index, value in now_data.items():
            if index in last_data:
                last_value = last_data[index]
                now_data[index]['n_confirm'] = value['confirm'] - last_value['confirm']
                now_data[index]['n_suspect'] = value['suspect'] - last_value['suspect']
                now_data[index]['n_dead'] = value['dead'] - last_value['dead']
                now_data[index]['n_heal'] = value['heal'] - last_value['heal']
            else:
                now_data[index]['n_confirm'] = value['confirm']
                now_data[index]['n_suspect'] = value['suspect']
                now_data[index]['n_dead'] = value['dead']
                now_data[index]['n_heal'] = value['heal']
            if self.check_whether_update(now_data[index]):
                update_city.append(now_data[index])
        return update_city

    def check_whether_update(self, item):
        return item['n_confirm'] > 0 or item['n_suspect'] > 0 or item['n_dead'] > 0 or item['n_heal'] > 0


if __name__=='__main__':
    tx = TXSpider()
    tx.main()


