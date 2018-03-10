# -*- coding: utf-8 -*-
import scrapy
from urllib import parse


class DianZanSpider(scrapy.Spider):
    name = 'dian_zan'
    allowed_domains = ['weixin.qq.com']
    # start_urls = ['https://mp.weixin.qq.com/mp/getappmsgext']

    def start_requests(self):

        yield scrapy.FormRequest(
            url='https://mp.weixin.qq.com/mp/getappmsgext',
            headers={'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; SM-N9108V Build/LMY47X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN',
                     },
            #
            cookies={
                'pvid': '7494844460',
                'rewardsn': '',
                'wxtokenkey': '10e9fdcc172142741602222ce7ee61691237ecb657567c116e42d5ca51b3749c',
                'wxuin': '2646451627',
                'devicetype': 'android-22',
                'version': '26060135',
                'lang': 'zh_CN',
                'pass_ticket': 'w3OIf482y0IHLlfHe3H+YZn6GwYP65voNf8HoD4xF5pHgMOqHn43aWV3gq7NfJdw',
                'wap_sid2': 'CKvL9u0JElxaZm1Cd0pLX2R1NmlfVFltSU1lOWF0eDVDRTNxc20yYWhXeENIRFlQWDNvUGlkUFpyUzVfRVRkVUlMZUxsVXd2YzBEM2huLWZESUd5QUl4UjFDV1pLTE1EQUFBfjCV8YTVBTgNQAE='
            },
            formdata={
                "__biz": 'MzA3MjEzNDYxMg==',
                "mid": '2650281467',
                "sn": '6e96bd4cef85d0e63b98516717ed013c',
                "idx": '1',
                "key": '777',
                "pass_ticket": 'w3OIf482y0IHLlfHe3H%252BYZn6GwYP65voNf8HoD4xF5pHgMOqHn43aWV3gq7NfJdw',
                "appmsg_token": '947_Zs6mEd10WxNMvvWjaiBtCmwd3Dqlo-JQ1VzW4HFV6G73ZH7xvqGLvZK8lEQScHaCNrZEEJqjhik4HcZg',
                "is_only_read": "1",
                "req_id": '0821xlWUPVCkK5bsQfT1rsXh',
                # "pass_ticket": 'w3OIf482y0IHLlfHe3H%252BYZn6GwYP65voNf8HoD4xF5pHgMOqHn43aWV3gq7NfJdw',
                "is_temp_url": "0",
            },
            method='POST',
            callback=self.parse
        )

    def parse(self, response):
        data = response.body
        pass
