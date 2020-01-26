import requests
from urllib import parse

from src.util.constant import REDIS_HOST, STATE_NCOV_INFO
from src.util.log import LogSupport
import json
import pandas as pd
import redis

class TXSpider():
    def __init__(self):
        self.req = requests.Session()
        self.log = LogSupport()
        self.re = self.connect_redis()

    def main(self):
        data = self.get_raw_real_time_info()
        self.parse_increase_info(data)

    def connect_redis(self):
        pool = self.get_pool()
        conn = redis.Redis(connection_pool=pool)
        return conn

    def get_pool(self):
        pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, decode_responses=True)
        return pool

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

    def parse_increase_info(self, data):
        last = self.load_last_info()
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
        province_dict = {x['area'] : x for x in province_json}
        # 合并数据并保存
        data_dict.update(province_dict)
        self.save_state_info(data_dict)

        # 计算有更新的城市/省份/国家
        update_city = []
        for index, value in data_dict.items():
            if index in last:
                last_value = last[index]
                data_dict[index]['n_confirm'] = value['confirm'] - last_value['confirm']
                data_dict[index]['n_suspect'] = value['suspect'] - last_value['suspect']
                data_dict[index]['n_dead'] = value['dead'] - last_value['dead']
                data_dict[index]['n_heal'] = value['heal'] - last_value['heal']
            else:
                data_dict[index]['n_confirm'] = value['confirm']
                data_dict[index]['n_suspect'] = value['suspect']
                data_dict[index]['n_dead'] = value['dead']
                data_dict[index]['n_heal'] = value['heal']
            if self.check_whether_update(data_dict[index]):
                update_city.append(data_dict[index])
        return update_city

    def check_whether_update(self, item):
        return item['n_confirm'] > 0 or item['n_suspect'] > 0 or item['n_dead'] or item['n_heal']

    def save_state_info(self, data):
        self.re.rpush(STATE_NCOV_INFO, json.dumps(data, ensure_ascii=False))

    def load_last_info(self):
        data_len = self.re.llen(STATE_NCOV_INFO)
        if data_len == 0:
            return None
        elif data_len >= 10:
            self.re.lpop(STATE_NCOV_INFO)
        last = json.loads(self.re.lrange(STATE_NCOV_INFO, -1, -1)[0])
        return last

if __name__=='__main__':
    pass


