import requests
from urllib import parse
from src.util.log import LogSupport
import json
import pandas

class TXSpider():

    def __init__(self):
        self.req = requests.Session()
        self.log = LogSupport()

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
            'name': 'wuwei_ww_area_counts',
        }
        return base_url + parse.urlencode(params)

    def get_real_time_info(self):
        url = self.get_real_time_url()
        header = self.get_tx_header()
        res = self.req.get(url=url, headers=header)
        if res.status_code != 200:
            self.log.logging.error("Failed to get info")
            raise ConnectionError
        content = json.loads(res.content.decode("utf-8"))


