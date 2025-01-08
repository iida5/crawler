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
        
def parse(file):

    responses = []
    room_count = 0
    plan_count = 0

    try:
        file_path = './data/{}'.format(file)
        f = open(file_path, 'r')
        data = f.read()
        f.close()
        rooms_raw = json.loads(r'{}'.format(data))
    except Exception as e:
        traceback.print_exc()
        return False
    
    totalCount = rooms_raw['data']['accommodation']['searchRooms2']['rooms']['totalCount']
    if totalCount == 0:
        return 'success'

    rooms = rooms_raw['data']['accommodation']['searchRooms2']['rooms']['edges']

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

    files = os.listdir('data')

    for file in files:
        if file == 'success':
            continue
        try:
            result = parse(file)
        except Exception as e:
            print('error')
            print(file)

        if result == 'success':
            print("{}: success {}".format(file, 'count is 0'))
            # os.rename('data/{}'.format(file), 'data/success/{}'.format(file))
        elif len(result) > 0:
            d = result[0]
            print("{}: success {},{},{},{},{}".format(file, d['plan_name'], d['room_id'], d['room_type_code'], d['room_smoking'], d['plan_meal']))
            # os.rename('data/{}'.format(file), 'data/success/{}'.format(file))
        else:
            print("{}: fail".format(file))

    print("scraping end")

if __name__ == "__main__":
    main()