import datetime
import logging
import os
import pathlib
import random
import sys
import threading
import time
import traceback
from datetime import date, datetime, timedelta
from pprint import pprint
import glob
import graphql
import requests
import json

sys.path.append('../config')
from config import Config

class Crawler:
        
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger('crawler')
        self.proxy = []
        self.request_count = 0

        self.headers = requests.utils.default_headers()
        self.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            }
        )

    def get_proxy(self):
        if len(self.proxy) > 0:
            return self.proxy.pop()
        self.proxy = self.config.proxy_servers.copy()
        return self.proxy.pop()

    def req(self, param):
        today = datetime.today().strftime("%Y-%m-%d")
        proxy = self.get_proxy() 
        hotel_id = param[0]
        checkin = param[1]
        ppc = param[2]
        query = graphql.query
        query = query.replace('{hotel_id}', hotel_id)
        query = query.replace('{checkin}', checkin)
        query = query.replace('{ppc}', ppc)
        query = query.replace('{plan_count}', '30')
        query = query.replace('{room_count}', '30')
            
        response = requests.post(
            "https://www.ikyu.com/graphql",
            data=query,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            },
            proxies={'http': proxy, 'https': proxy},
            timeout=(5, 10)
        )

        file_path_tmp1 = './output1.json'
        file_path_tmp2 = './output2.json'
        file_path_tmp3 = './output3.json'

        response.encoding = 'UTF-8'
        # r = json.loads(response.content)

        r = json.loads(response.content)

        # print(r['data']['accommodation']['searchRooms2'])
        # print(r['data']['accommodation']['searchRooms2']['rooms']['edges'])
        # pprint(r['data']['accommodation']['searchRooms2']['facet']['roomAttributes'])
        # sys.exit

        try:
            with open(file_path_tmp1, 'w') as f:
                data = response.content.decode("utf-8")
                f.write(data)
            with open(file_path_tmp2, 'w') as f:
                r = json.loads(response.content)
                json.dump(r, f, ensure_ascii=False, indent=2)
            with open(file_path_tmp3, 'w') as f:
                r = json.loads(response.content)
                json.dump(r['data']['accommodation']['searchRooms2']['rooms']['edges'], f, ensure_ascii=False, indent=2)
                # f.write(data)
            return data
        except Exception as e:
            print(file_path_tmp1)
            traceback.print_exc()
        
        time.sleep(0.01)
        
class Parse:

    def __init__(self):
        self.hotel_datas = {}
        with open('../config/hotels.csv', 'r') as f:
            rows = f.read().split('\n')
        for row in rows:
            row_split = row.split(',')
            if len(row_split) == 1:
                continue
            # print(row_split)
            self.hotel_datas[row_split[0]] = {
                'hotel_id': row_split[0],
                'hotel_name': row_split[1],
                'hotel_address': row_split[5],
                'hotel_area': row_split[2],
                'area_class': row_split[9]
            }

    def init_response(self, base_date, file):
        response = {
            'id': '',
            'hotel_name': '',
            'address': '',
            'area': '',
            'area_class': '',
            'date': '',
            'hotel_id': '',
            'checkin': '',
            'ppc': '',
            'room_id': '',
            'room_name': '',
            'room_type_code': '',
            'room_smonking': '',
            'plan_id': '',
            'plan_name': '',
            'plan_discount_price': '',
            'link': '',
            'file': '',
            'full_text': '',
            'store': '',
            'modified': '',
            'created': ''
        }

        file_split = file.replace('.html', '').split('_')
        
        response['input_date'] = base_date
        response['input_hotel_id'] = file_split[0]
        response['input_checkin'] = file_split[1]
        response['input_ppc'] = file_split[2]

        response['link'] = 'https://www.ikyu.com/{}/?adc=1&cid={}&cod={}&lc=1&ppc={}&rc=1&si=1&st=1'.format(
            response['input_hotel_id'], 
            response['input_checkin'].replace('-', ''), 
            response['input_checkout'].replace('-', ''), 
            response['input_ppc']
        )

        return response
    

    def html(self):

        responses = []
        room_count = 0
        plan_count = 0

        try:
            file_path = './output3.json'
            f = open(file_path, 'r')
            data = f.read()
            f.close()
            rooms = json.loads(r'{}'.format(data))
        except Exception as e:
            traceback.print_exc()
            return False
        
        alls = []
        m = {}
        p = {}
        for room in rooms:
            m['room_id'] = room['node']['roomId']
            m['room_name'] = room_name =  room['node']['name']
            m['room_type_code'] = room['node']['type']['code']

            m['room_smoking'] = 0
            if room['node']['attributes']:
                for att in room['node']['attributes']:
                    if (att['value'] == '31'):
                        m['room_smoking'] =  1
                        break

            if room['node']['amounts'] is None:
                continue
            
            plans = room['node']['amounts']['edges']
            for plan in plans:
                p['plan_id'] =  plan['node']['plan']['planId']
                p['plan_name'] = plan['node']['plan']['name']
                p['plan_price'] = plan['node']['amount']
                p['plan_discount_price'] = plan['node']['discountAmount']
                p['room_inventory'] = plan['node']['inventory']
                p['plan_meal'] = plan['node']['plan']['meal']['code']
                # p['full_text'] = '{} {} {}'.format(h['hotel_name'], h['hotel_area'], h['hotel_address'])
                p['full_text'] = ''
                alls.append(m | p)
                p = {}
            m = {}

        return alls

def main():

    config = Config()    

    param = [
        '00000946', #hotel_id = param[0]
        '2024-09-27', #checkin = param[1]
        '2', #ppc = param[2]
    ]

    # crawl
    crawler = Crawler()
    data = crawler.req(param)
    
    # sys.exit()
    # print(data)
    
    # scraping
    parse = Parse()
    parsed_data = parse.html()

    pprint(parsed_data)

    file_path_tmp4 = 'output4.json'
    with open(file_path_tmp4, 'w') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()