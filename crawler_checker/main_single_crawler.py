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

        file_path_tmp = './data/{}.json'.format(hotel_id)

        response.encoding = 'UTF-8'
        # r = json.loads(response.content)

        data = response.content.decode("utf-8")
        try:
            with open(file_path_tmp, 'w') as f:
                # json.dump(r['data']['accommodation']['searchRooms2']['rooms']['edges'], f, ensure_ascii=False, indent=2)
                f.write(data)
            print("{} {}".format(file_path_tmp, round(os.path.getsize(file_path_tmp) / 1024, 2)))
        except Exception as e:
            print(file_path_tmp)
            traceback.print_exc()
            
        time.sleep(0.01)
        
def main():

    config = Config()    

    param = [
        '00000946', #hotel_id = param[0]
        '2024-08-27', #checkin = param[1]
        '2', #ppc = param[2]
    ]

    crawler = Crawler()
    crawler.req(param)
    
    print("crawler end")

if __name__ == "__main__":
    main()