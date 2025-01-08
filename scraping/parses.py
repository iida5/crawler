from bs4 import BeautifulSoup
import re
import sys
import math
import os
import pprint
import copy
import time
import json
from pprint import pprint
import traceback

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
    

    def html(self, base_date, file):

        responses = []
        room_count = 0
        plan_count = 0

        try:
            file_path = '../data/{}/file/{}'.format(base_date, file)
            f = open(file_path, 'r')
            data = f.read()
            f.close()
            rooms = json.loads(r'{}'.format(data))
        except Exception as e:
            traceback.print_exc()
            return False
        
        # rooms = json.load(json_file)

        f = file.replace('.json', '')
        hotel_id, ci, ppc = f.split('_')

        b = {
            'date': base_date,
            'file': file,
            'checkin': ci,
            'ppc': int(ppc)
        }
        h = self.hotel_datas[hotel_id]
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
                alls.append(b | h | m | p)
                p = {}
            m = {}

        return alls