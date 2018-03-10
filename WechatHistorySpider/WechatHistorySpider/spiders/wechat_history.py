# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import HistoryItem


class WechatHistorySpider(scrapy.Spider):
    name = 'wechat_history'
    allowed_domains = ['mp.weixin.qq.com']
    # start_urls = ['http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA3MjEzNDYxMg==#wechat_webview_type=1&wechat_redirect']

    def start_requests(self):
        url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3MjEzNDYxMg==&f=json&offset=0&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=Kzq7aEg6TFlxtxmgP8J2GtNB1M3eJCQjgid%2ByS5z1X200bRuv%2BWSFJ3n%2Fa%2Fb1tb7&wxtoken=&appmsg_token=947_UQlptWVopI1WO1wrcqG-MtrArs-t2L3HagUn6w~~&x5=0&f=json'
        yield scrapy.FormRequest(
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-N9108V Build/LMY47X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN'},
            # pvid=7494844460; rewardsn=; wxtokenkey=da229eae8f4a1b4d14d1a2d0cce1f758e49572d3177f9bf4f46f8eed173fa6e7; wxuin=2646451627; devicetype=android-22; version=26060135; lang=zh_CN; pass_ticket=Kzq7aEg6TFlxtxmgP8J2GtNB1M3eJCQjgid+yS5z1X200bRuv+WSFJ3n/a/b1tb7; wap_sid2=CKvL9u0JElw2M2Y1bkFkWm50eUl3YXFBVkJXd2dOLW5ZQTN1WFI3QVBqUi1WNmNZLVVsRG5WRXVEcUkyak0wZFBNdjh1czl4RVNHaFBkd2lZT2tOOXoySWYzeTNnN01EQUFBfjD4gI3VBTgNQJVO
            cookies={
                'pvid': '7494844460',
                'rewardsn': '',
                'wxtokenkey': 'da229eae8f4a1b4d14d1a2d0cce1f758e49572d3177f9bf4f46f8eed173fa6e7',
                'wxuin': '2646451627',
                'devicetype': 'android-22',
                'version': '26060135',
                'lang': 'zh_CN',
                'pass_ticket': 'Kzq7aEg6TFlxtxmgP8J2GtNB1M3eJCQjgid+yS5z1X200bRuv+WSFJ3n/a/b1tb7',
                'wap_sid2': 'CKvL9u0JElw2M2Y1bkFkWm50eUl3YXFBVkJXd2dOLW5ZQTN1WFI3QVBqUi1WNmNZLVVsRG5WRXVEcUkyak0wZFBNdjh1czl4RVNHaFBkd2lZT2tOOXoySWYzeTNnN01EQUFBfjD4gI3VBTgNQJVO'
            },
            callback=self.parse
        )

    def parse(self, response):
        # 文章详情
        data = json.loads(response.body.decode('utf-8'))
        next_offset = data['next_offset']
        yield scrapy.Request(
            url='https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3MjEzNDYxMg==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=Kzq7aEg6TFlxtxmgP8J2GtNB1M3eJCQjgid%2ByS5z1X200bRuv%2BWSFJ3n%2Fa%2Fb1tb7&wxtoken=&appmsg_token=947_UQlptWVopI1WO1wrcqG-MtrArs-t2L3HagUn6w~~&x5=0&f=json'.format(next_offset),
            callback=self.parse
        )
        content_url_list = []
        results = eval(data['general_msg_list'].strip('\\'))['list']

        for result in results:
            try:
                result_info = result['app_msg_ext_info']
            except KeyError as e:
                # 个别app_msg_ext_info 改为 image_msg_ext_info
                print('key_error is :', e)
            else:
                content_url = result_info['content_url']
                content_url_list.append(content_url)
                next_result_info= result_info['multi_app_msg_item_list']
                for next_result in next_result_info:
                    next_content_url = next_result['content_url']
                    content_url_list.append(next_content_url)
        for url in content_url_list:
            pattern = re.compile(r'\\', re.S)
            detail_url = pattern.sub('', url)
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={'content_url':detail_url}
            )

    def parse_detail(self, response):
        results = response.xpath('.//div[@id="img-content"]')
        for result in results:
            title = result.xpath('.//h2/text()').extract_first('').strip()
            date = result.xpath('.//div/em/text()').extract_first('')
            public_name = result.xpath('.//div/a/text()').extract_first('')
            content_url = response.meta['content_url']
            print(content_url)
            # 'http://mp.weixin.qq.com/s?__biz=MzA3MjEzNDYxMg==&amp;mid=2650300286&amp;idx=1&amp;sn=22f70aef506eaac2db131e64cf848b16&amp;chksm=872e05c5b0598cd38ee8dd70b297b2c69b48ae26fbdf47042f2b1dc9a6b8197a3887daf11531&amp;scene=27#wechat_redirect'
            # 返回点赞数和阅读量信息 获取多篇文章修改 mid sn idx
            # 特殊字符？前必须加转义字符\
            pattern = re.compile(
                r'http://mp.weixin.qq.com/s\?__biz=MzA3MjEzNDYxMg==&amp;mid=(.*?)&amp;idx=(.*?)&amp;sn=(.*?)&amp',
                re.S)
            pattern_result = pattern.search(content_url)
            mid = pattern_result.group(1)
            idx = pattern_result.group(2)
            sn = pattern_result.group(3)
            yield scrapy.FormRequest(
                url='https://mp.weixin.qq.com/mp/getappmsgext',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-N9108V Build/LMY47X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN'},
                #
                cookies={
                    'pvid': '7494844460',
                    'rewardsn': '',
                    'wxtokenkey': 'da229eae8f4a1b4d14d1a2d0cce1f758e49572d3177f9bf4f46f8eed173fa6e7',
                    'wxuin': '2646451627',
                    'devicetype': 'android-22',
                    'version': '26060135',
                    'lang': 'zh_CN',
                    'pass_ticket': 'Kzq7aEg6TFlxtxmgP8J2GtNB1M3eJCQjgid+yS5z1X200bRuv+WSFJ3n/a/b1tb7',
                    'wap_sid2': 'CKvL9u0JElw2M2Y1bkFkWm50eUl3YXFBVkJXd2dOLW5ZQTN1WFI3QVBqUi1WNmNZLVVsRG5WRXVEcUkyak0wZFBNdjh1czl4RVNHaFBkd2lZT2tOOXoySWYzeTNnN01EQUFBfjD4gI3VBTgNQJVO'
                },
                formdata={
                    "__biz": 'MzA3MjEzNDYxMg==',
                    "mid": mid,
                    "sn": sn,
                    "idx": idx,
                    "key": '777',
                    "pass_ticket": 'Kzq7aEg6TFlxtxmgP8J2GtNB1M3eJCQjgid%252ByS5z1X200bRuv%252BWSFJ3n%252Fa%252Fb1tb7',
                    "appmsg_token": '947_D5xfpofn5DtJ7dIgGEZAMolJoiH2v6ll7V96BuIBP-vlF27T3VoX5Z7R2tIdG4d0FY6GI1SCvKtKmwB3',
                    "is_only_read": "1",
                    "req_id": '1010VgcilwxKuB1maUk6OVTy',
                    "is_temp_url": "0"
                },
                method='POST',
                callback=self.parse_info,
                meta={'title': title, 'date': date, 'public_name': public_name, 'content_url': content_url}
            )

    def parse_info(self, response):
        data = json.loads(response.body.decode('utf-8'))
        like_num = data["appmsgstat"]["like_num"]
        read_num = data["appmsgstat"]["read_num"]
        history = HistoryItem()
        result = response.meta
        history['title'] = result['title']
        history['date'] = result['date']
        history['public_name'] = result['public_name']
        history['content_url'] = result['content_url']
        history['like_num'] = like_num
        history['read_num'] = read_num
        yield history






