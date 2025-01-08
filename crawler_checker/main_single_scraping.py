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
    
    rooms = rooms_raw['data']['accommodation']['searchRooms2']['rooms']['edges']

    alls = []
    m = {}
    p = {}
    for room in rooms:
        m['room_id'] = room['node']['roomId']
        m['room_name'] = room_name =  room['node']['name']
        m['room_type_code'] = room['node']['type']['code']
        if room['node']['attributes'] and '20' in room['node']['attributes']:
            m['room_smoking'] =  1
        else:
            m['room_smoking'] = 0

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

    file = files[0]
    
    result = parse(file)
    if len(result) > 0:
        print("{}: success {}".format(file, result[0]['plan_name']))
        # pprint(result[0])
        # pprint(result[1])
    else:
        print("{}: fail".format(file))
        pprint(result)

    print("scraping end")

if __name__ == "__main__":
    main()