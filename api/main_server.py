# インポート
from bottle import route, run, HTTPResponse, request
import api_busy
import api_price
import json
import os
import time
import datetime
import requests
import sys

sys.path.append('../config')
from config import Config

@route('/hello')
def hello():
    body = {"status": "OK", "message": "hello world"}
    res = HTTPResponse(status=200, body=body)
    res.set_header("Content-Type", "application/json")
    return res

@route('/busy')
def busy():
    if request.query.reload != '1':
        body = json.load(open('cache/busy.json', 'r'))
    else:
        body = api_busy.main()
        json_file = open('cache/busy.json', mode="w")
        json.dump(body, json_file, ensure_ascii=False)
        json_file.close()

    res = HTTPResponse(status=200, body=body)
    res.set_header("Content-Type", "application/json")
    return res

@route('/price')
def price():

    if request.query.reload != '1':
        body = json.load(open('cache/price.json', 'r'))
    else:
        body = api_price.main(request.query.start_date, request.query.end_date, request.query.target_percent)
        json_file = open('cache/price.json', mode="w")
        json.dump(body, json_file, ensure_ascii=False)
        json_file.close()

    res = HTTPResponse(status=200, body=body)
    res.set_header("Content-Type", "application/json")
    return res

run(host='0.0.0.0', port=8000, debug=True, reloader=True)