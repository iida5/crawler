import logging
import os
import re
import sys
import time
import traceback
from datetime import datetime
from pprint import pprint
from config import Config
import json
import shutil

from parses import Parse
import mysql.connector

sys.path.append('../config')
from config import Config

def init_logger(base_date):
    logger = logging.getLogger('crawler')
    logger.setLevel(logging.DEBUG)

    if len(logger.handlers):
        logger.handlers.clear()
        
    formatter = logging.Formatter('%(asctime)s %(funcName)4s:%(lineno)d %(message)s')

    fh = logging.FileHandler('logs/{}.log'.format(base_date))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # fh = logging.StreamHandler()
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    return logger

class DB:

    def connect(self):
        config = Config()
        self.conn = mysql.connector.connect(
            host=config.mysql_host,
            port=config.mysql_port,
            user=config.mysql_user,
            password=config.mysql_password,
            database=config.mysql_database
        )
        return self.conn

    def create_sql(self, table):
        sql = """
        INSERT INTO {} (
                hotel_name,
                hotel_address,
                hotel_area,
                area_class,
                date,
                hotel_id,
                checkin,
                ppc,
                room_id,
                room_name,
                room_type_code,
                room_smoking,
                room_inventory,
                plan_id,
                plan_name,
                plan_price,
                plan_discount_price,
                plan_meal,
                file,
                full_text,
                modified,
                created
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
        """.format(table)

        return sql

def file_log(file, logfile='scraping.log'):
    today = datetime.today().strftime("%Y-%m-%d")
    with open('../data/{}/{}'.format(today, logfile), 'a') as f:
        f.write('{}\n'.format(file))

def main():
    try:
        config = Config()
        start = time.time()
        is_first = True
        db = DB()
        conn = db.connect()
        cursor = conn.cursor()
        loop_count = 0
        total_execute_time = 0
        total_execute_count = 0
        parse = Parse()
        sql = db.create_sql('plans')
        insert_count = 0
        pre_db_connect = 0

        while True:
            try:
                loop_count += 1
                parse_count = 0
                while_start = time.time()

                base_date = datetime.today().strftime("%Y-%m-%d")
                logger = init_logger(base_date)

                if is_first:
                    logger.debug('-' * 30)
                    logger.debug('scraping {}'.format(base_date))
                    logger.debug('-' * 30)
                    is_first = False

                if not os.path.exists('../data/{}/file'.format(base_date)):
                    os.makedirs('../data/{}/file'.format(base_date))

                crawled_files = os.listdir('../data/{}/file'.format(base_date))
                if len(crawled_files) > 0:
                    
                    if time.time() - pre_db_connect > 3600:
                        pre_db_connect = time.time()
                        try:
                            cursor.close()
                            conn.close()
                        except:
                            pass
                        conn = db.connect()
                        cursor = conn.cursor()

                    logger.debug('[start]')
                    logger.debug('loop: {}'.format(loop_count))
                    logger.debug('file_count: {}'.format(len(crawled_files)))
                    logger.debug('[scraping]')
                    crawled_files = sorted(crawled_files)
                    insert_params = []
                    for file in crawled_files:
                        try:
                            cursor.execute("delete from plans where file = %s", (file,))
                            params = parse.html(base_date, file)
                            if params == False:
                                raise Exception('parse error')
                            for param in params:
                                param['modified'] = None
                                param['created'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                                insert_params.append((
                                    param['hotel_name'],
                                    param['hotel_address'],
                                    param['hotel_area'],
                                    param['area_class'],
                                    param['date'],
                                    param['hotel_id'],
                                    param['checkin'],
                                    param['ppc'],
                                    param['room_id'],
                                    param['room_name'],
                                    param['room_type_code'],
                                    param['room_smoking'],
                                    param['room_inventory'],
                                    param['plan_id'],
                                    param['plan_name'],
                                    param['plan_price'],
                                    param['plan_discount_price'],
                                    param['plan_meal'],
                                    param['file'],
                                    param['full_text'],
                                    param['modified'],
                                    param['created']
                                ))
                                file_log('{} {}'.format(param['created'], param['plan_name']), 'insert.log')

                        except Exception as e:
                            logger.debug('fail: {}'.format(file))
                            logger.debug('parse exception: '.format(file))
                            logger.debug(e)
                            traceback.print_exc()
                            shutil.move('../data/{}/file/{}'.format(base_date, file), '../data_failed/{}'.format(file))
                            parse_count += 1
                            file_log(file)
                            file_log(file, 'error.log')
                            continue

                        logger.debug('{}'.format(file))
                        os.remove('../data/{}/file/{}'.format(base_date, file))  
                        parse_count += 1
                        file_log(file)

                    try:
                        insert_count = len(insert_params)
                        cursor.executemany(sql, insert_params)
                        conn.commit()
                    except mysql.connector.Error as err:
                        print("sql error: {}".format(err))
                        conn = db.connect()
                        cursor = conn.cursor()
                        time.sleep(1)

                    logger.debug('[end]')
                    logger.debug('parse_count: {}'.format(parse_count))
                    logger.debug('insert_count: {}'.format(insert_count))
                    logger.debug('execute_time: {}'.format(round(time.time() - while_start, 3)))
                    time_per_file = (time.time() - while_start) / parse_count
                    logger.debug('time_per_file: {}'.format(round(time_per_file, 3)))
                    total_execute_time += time.time() - while_start
                    total_execute_count += parse_count
                    logger.debug('page average: {}'.format(round((total_execute_time / total_execute_count), 3)))

                    cursor = db.conn.cursor()
                    cursor.execute('select count(id) from plans')
                    plans_count = cursor.fetchone()
                    db.conn.commit()
                    logger.debug('db count: {}'.format(plans_count[0]))

                    load1, load5, load15 = os.getloadavg() 
                    logger.debug('load average {} {} {}'.format(load1, load5, load15))

                    logger.debug('-' * 30)

                time.sleep(1)
            
            except Exception as e:
                print(datetime.now())
                traceback.print_exc()
                # logger.debug('exception')
                # logger.debug('{}'.format(e))
                # logger.debug('{}'.format(traceback.print_exc()))
                time.sleep(1)

    except KeyboardInterrupt:
        logger.debug('keyboard stop')

if __name__ == "__main__":
    main()