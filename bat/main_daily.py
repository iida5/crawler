import logging
import os
import re
import sys
import time
import traceback
from datetime import datetime
from pprint import pprint
import json
import shutil
import subprocess
import pathlib

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

# def file_log(file, logfile='scraping.log'):
#     today = datetime.today().strftime("%Y-%m-%d")
#     with open('../data/{}/{}'.format(today, logfile), 'a') as f:
#         f.write('{}\n'.format(file))

def main():
    config = Config()

    base_date = datetime.today().strftime("%Y-%m-%d")

    logger = init_logger(base_date)

    if os.path.isfile("../data/{}/bat.log".format(base_date)):
        sys.exit()

    logger.debug("[pre] start")

    if not os.path.isfile("../data/{}/crawler.log".format(base_date)):
        logger.debug("[pre] end no pass check crawler.log")
        sys.exit()

    if not os.path.isfile("../data/{}/scraping.log".format(base_date)):
        logger.debug("[pre] end no pass check scraping.log")
        sys.exit()

    t_crawler = os.path.getmtime("../data/{}/crawler.log".format(base_date))
    rest_t_crawler = round(time.time() - t_crawler)
    if rest_t_crawler < 600:
        logger.debug("[pre] end wait {} crawler.log".format(rest_t_crawler))
        sys.exit()

    t_scraping = os.path.getmtime("../data/{}/scraping.log".format(base_date))
    rest_t_scraping = round(time.time() - t_scraping)
    if rest_t_scraping < 600:
        logger.debug("[pre] end wait {} scraping.log".format(rest_t_scraping))
        sys.exit()

    logger.debug("[pre] end pass")

    pathlib.Path('../data/{}/bat.log'.format(base_date)).touch()

    db = DB()
    conn = db.connect()
    cursor = conn.cursor()

    # dump
    logger.debug('[start] dump')

    dir = os.path.dirname(__file__)
    dump_path = '{}/files/{}.sql.gz'.format(dir, base_date)

    subprocess.run(f"mysqldump -u {config.mysql_user} -p{config.mysql_password} {config.mysql_database} plans --skip-add-drop-table -t | gzip > {dump_path}", shell=True)

    logger.debug("[end] dump")

    logger.debug('[start] all')
    
    # insert all
    try:
        sql = """
        INSERT IGNORE INTO plans_all
        SELECT * FROM plans
        WHERE date = %s
        """
        cursor.execute(sql, (base_date, ))
        conn.commit()
    except mysql.connector.Error as err:
        logger("sql error: {}".format(err))
        conn = db.connect()
        cursor = conn.cursor()

    logger.debug('[end] all')

    logger.debug('[start] search')

    # insert search
    try:
        cursor.execute("truncate plans_search")
        conn.commit()

        sql = """
        INSERT IGNORE INTO plans_search
        SELECT * FROM plans
        WHERE date = %s
        """
        cursor.execute(sql, (base_date, ))
        conn.commit()

        sql = """
        UPDATE plans_search SET 
        full_text = concat(
            hotel_name, 
            ' ', 
            hotel_address, 
            ' ', 
            hotel_area, 
            ' ', 
            room_name, 
            ' ', 
            plan_name)
        """
        cursor.execute(sql)
        conn.commit()

        cursor.execute("delete from plans")
        conn.commit()

    except mysql.connector.Error as err:
        logger("sql error: {}".format(err))
        conn = db.connect()
        cursor = conn.cursor()

    logger.debug('[end] search')

    # delete 

if __name__ == "__main__":
    main()