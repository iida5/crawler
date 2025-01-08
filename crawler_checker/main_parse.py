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

def main():
    
    try:
        # file_path = './data/00001515.json'
        file_path = './data/00000946.json'
        f = open(file_path, 'r')
        data = f.read()
        f.close()
        rooms_raw = json.loads(r'{}'.format(data))
    except Exception as e:
        traceback.print_exc()
        return False

    # pprint(rooms_raw)
    with open("output.json", "w") as f:
        pprint(rooms_raw, stream=f)

    print("output.json end")

    totalCount = rooms_raw['data']['accommodation']['searchRooms2']['rooms']['totalCount']
    print(totalCount)
    pprint(rooms_raw['data']['accommodation']['searchRooms2']['rooms'])

if __name__ == "__main__":
    main()