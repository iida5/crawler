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

def init_logger(base_date):
    logger = logging.getLogger('crawler')
    logger.setLevel(logging.DEBUG)

    if len(logger.handlers):
        logger.handlers.clear()
        
    # formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s:%(lineno)d %(message)s')
    formatter = logging.Formatter('%(asctime)s %(funcName)4s:%(lineno)d %(message)s')

    fh = logging.FileHandler('logs/{}.log'.format(base_date))
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # fh = logging.StreamHandler()
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    return logger

def init_dir(base_date):
    if not os.path.exists('../data/{}/file'.format(base_date)):
        os.makedirs('../data/{}/file'.format(base_date))

    if not os.path.exists('../data/{}/tmp'.format(base_date)):
        os.makedirs('../data/{}/tmp'.format(base_date))

def init_crawler(base_date):
    pathlib.Path('../data/{}/crawler.log'.format(base_date)).touch()
    init_files = []
    with open('../data/{}/crawler.log'.format(base_date), 'r') as f:
        files = f.readlines()
        for file in files:
            init_files.append(file.rstrip("\n"))

    return init_files

def init_scraping(base_date):
    pathlib.Path('../data/{}/scraping.log'.format(base_date)).touch()
    init_files = []
    with open('../data/{}/scraping.log'.format(base_date), 'r') as f:
        files = f.readlines()
        for file in files:
            init_files.append(file.rstrip("\n"))

    return init_files

def log_output(file, logfile='crawler.log'):
    today = datetime.today().strftime("%Y-%m-%d")
    with open('../data/{}/{}'.format(today, logfile), 'a') as f:
        f.write('{}\n'.format(file))

def init_hotel_ids():
    config = Config()    
    hotel_ids = []
    with open('../config/hotels.csv', 'r') as f:
        rows = f.read().split('\n')
    for row in rows:
        row_split = row.split(',')
        if row_split[0]:
            hotel_ids.append(row_split[0])
    return hotel_ids[0:config.hotel_limit]

def init_params(base_date, crawler_files, scraping_files):
    logger = logging.getLogger('crawler')
    config = Config()

    hotel_ids = init_hotel_ids()
    today_obj = datetime.strptime(base_date, '%Y-%m-%d')

    person_limit_range = config.person_limit + 1
    params = []

    dates = []
    for date_diff in range(config.date_limit):
        checkin = datetime.strftime(today_obj + timedelta(date_diff), '%Y-%m-%d')
        checkout = datetime.strftime(today_obj + timedelta(date_diff + 1), '%Y-%m-%d')
        dates.append([checkin, checkout])
    
    persons = range(1, person_limit_range);

    set_params = []
    for hotel_id in hotel_ids:
        for checkin, checkout in dates:
            for person in persons:
                set_params.append('{}_{}_{}'.format(hotel_id, checkin, person))

    files_params = []
    files = crawler_files + scraping_files
    for file in files:
        hotel_id, checkin, person = file.split('_')
        person = person.replace('.json', '')
        files_params.append('{}_{}_{}'.format(hotel_id, checkin, person))
    
    diffs = set(set_params) - set(files_params)

    params = []
    diffs = list(diffs)
    for diff in diffs:
        hotel_id, checkin, person = diff.split('_')
        params.append([hotel_id, checkin, person])

    return params

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

        if self.config.is_enable_proxy:
            
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
        else:
            response = requests.post(
                "https://www.ikyu.com/graphql",
                data=query,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                },
                timeout=(5, 10)
            )

        file = '{}_{}_{}.json'.format(param[0], param[1], param[2])
        file_path = '../data/{}/file/{}'.format(today, file)
        file_path_tmp = '../data/{}/tmp/{}'.format(today, file)

        response.encoding = 'UTF-8'
        r = json.loads(response.content)

        try:
            with open(file_path_tmp, 'w') as f:
                json.dump(r['data']['accommodation']['searchRooms2']['rooms']['edges'], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(file_path_tmp, file_path)
            traceback.print_exc()
            
        os.rename(file_path_tmp, file_path)
                  
        filesize = str(round(len(response.content) / 1024))+ "KB"
        proxy_no =self.config.proxy_servers.index(proxy)
        self.logger.debug('{} {} {}'.format(file, proxy_no, filesize))

        log_output(file)
        
def main():
    try:
        start = time.time()
        config = Config()

        base_date = ''
        loop_count = 0
        total_execute_time = 0
        total_execute_count = 0
        while True:
            try:
                if base_date != datetime.today().strftime("%Y-%m-%d"):
                    base_date = base_date = datetime.today().strftime("%Y-%m-%d")
                    logger = init_logger(base_date)

                    logger.debug('-' * 30)
                    logger.debug('crawler {}'.format(base_date))
                    logger.debug('-' * 30)

                    init_dir(base_date)
                    crawler_files = init_crawler(base_date)
                    scraping_files = init_scraping(base_date)
                    crawl_params = init_params(base_date, scraping_files, crawler_files)

                    crawl_count = len(crawl_params)
                    crawled_count = len(crawler_files)
                    scraping_count = len(scraping_files)

                    logger.debug('[status]')
                    logger.debug('target: {}'.format(crawl_count + crawled_count + scraping_count))
                    logger.debug('remaining:  {}'.format(crawl_count))
                    logger.debug('completed: {}'.format(crawled_count))
                    logger.debug('scraping: {}'.format(scraping_count))
                    logger.debug('-' * 30)

                    time.sleep(1)
                    
                    random.shuffle(crawl_params)

                    crawler = Crawler()
                    loop_count = 0
                    while len(crawl_params) > 0:
                        while_start = time.time()
                        loop_count += 1
                        if base_date != datetime.today().strftime("%Y-%m-%d"):
                            logger.debug('[date]')
                            logger.debug('base_date: {}'.format(base_date))
                            logger.debug('today: {}'.format(datetime.today().strftime("%Y-%m-%d")))
                            break

                        logger.debug('[start]')
                        logger.debug('loop: {}'.format(loop_count))
                        logger.debug('file_count: {}'.format(config.thread_limit))
                        logger.debug('[crawle]')

                        for l in range(config.thread_limit):
                            if len(crawl_params) == 0:
                                break
                            param = crawl_params.pop()
                            t = threading.Thread(target=crawler.req, args=(param,))
                            t.start()

                        thread_list = threading.enumerate()
                        thread_list.remove(threading.main_thread())
                        thread_count = 0
                        for thread in thread_list:
                            thread.join()
                            crawler.request_count += 1
                            thread_count += 1

                        logger.debug('[end]')
                        logger.debug('complete: {}'.format(crawler.request_count))
                        logger.debug('remaining: {}'.format(crawl_count - crawler.request_count))
                        logger.debug('execute_time: {}'.format(round((time.time() - while_start), 3)))
                        time_per_file = ((time.time() - while_start) / thread_count)
                        logger.debug('file_count: {}'.format(thread_count))
                        logger.debug('time_per_file: {}'.format(round(time_per_file, 3)))

                        dir_files = len(glob.glob('../data/{}/file/*'.format(base_date)))
                        logger.debug('dir files: {}'.format(dir_files))

                        total_execute_time += time.time() - while_start
                        total_execute_count += thread_count
                        logger.debug('crawle average: {}'.format(round((total_execute_time / total_execute_count), 3)))

                        load1, load5, load15 = os.getloadavg() 
                        logger.debug('load average {} {} {}'.format(load1, load5, load15))

                        logger.debug('-' * 30)
                        
                        time.sleep(config.thread_wait)
             
                    if crawl_count - crawler.request_count == 0:
                        logger.debug('finished')
                        
                time.sleep(config.thread_wait)
            
            except Exception as e:
                print(datetime.now())
                traceback.print_exc()
                time.sleep(60)

            time.sleep(0.01)

    except KeyboardInterrupt:
        print('keyboard stop')
        
if __name__ == "__main__":
    main()