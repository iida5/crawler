import mysql.connector
from pprint import pprint
import json
from pprint import pprint
import datetime
import sys
import math

sys.path.append('../config')
from config import Config

hotels = [
    '00000198',
    '00002764',
    '00000192',
    '00000201',
    '00002643',
    '00000152',
    '00001562',
    '00001229',
    '00000071',
    '00001331',
]

hotels_str = ','.join(hotels)

def main(start_date='', end_date='', target_percent=''):

    if target_percent == '':
        target = 80 # percent 上位何%を比較対象とするか
    else:
        target = int(target_percent)

    if start_date == '':
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')

    if end_date == '':
        end_date = (datetime.datetime.today() + datetime.timedelta(days=60)).strftime('%Y-%m-%d')

    t_start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    t_end   = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # days = 60 # 比較する日数の範囲

    config = Config()
    conn = mysql.connector.connect(
        host=config.mysql_host,
        port=config.mysql_port,
        user=config.mysql_user,
        password=config.mysql_password,
        database=config.mysql_database
    )
    cursor = conn.cursor()

    date_prices = []
    for i in range((t_end - t_start).days + 1):
        date = t_start + datetime.timedelta(i)
        date_str = date.strftime("%Y-%m-%d")

        sql = """
        select 
            avg(plan_discount_price) as a,
            count(id) as c
        from
            plans_search
        where
            ppc = 2
            and checkin = %s
            and hotel_id in ({})
        group by
            checkin
        """.format(hotels_str)
        cursor.execute(sql, (date,))
        r = cursor.fetchone()
        if r:
            date_prices.append([date_str, int(r[0]), r[1]])
    
    # date_prices = [['2024-04-06', 197107, 73], ['2024-04-07', 187515, 154], ['2024-04-08', 201709, 190], ['2024-04-09', 235119, 167], ['2024-04-10', 246113, 139], ['2024-04-11', 275716, 160], ['2024-04-12', 272036, 140], ['2024-04-13', 312501, 52], ['2024-04-14', 212780, 192], ['2024-04-15', 209146, 173], ['2024-04-16', 239876, 107], ['2024-04-17', 255851, 119], ['2024-04-18', 211293, 216], ['2024-04-19', 245577, 181], ['2024-04-20', 280658, 114], ['2024-04-21', 184394, 312], ['2024-04-22', 179263, 269], ['2024-04-23', 200723, 221], ['2024-04-24', 182636, 291], ['2024-04-25', 188889, 299], ['2024-04-26', 193136, 287], ['2024-04-27', 225422, 203], ['2024-04-28', 196097, 161], ['2024-04-29', 156544, 312], ['2024-04-30', 143597, 364], ['2024-05-01', 142950, 390], ['2024-05-02', 161342, 322], ['2024-05-03', 215569, 174], ['2024-05-04', 223526, 169], ['2024-05-05', 185275, 279], ['2024-05-06', 132869, 432], ['2024-05-07', 124379, 443], ['2024-05-08', 125678, 469], ['2024-05-09', 144485, 322], ['2024-05-10', 153429, 295], ['2024-05-11', 183026, 254], ['2024-05-12', 155977, 334], ['2024-05-13', 153332, 321], ['2024-05-14', 151174, 263], ['2024-05-15', 179087, 233], ['2024-05-16', 170875, 285], ['2024-05-17', 182184, 279], ['2024-05-18', 213187, 205], ['2024-05-19', 160172, 402], ['2024-05-20', 134527, 339], ['2024-05-21', 153318, 289], ['2024-05-22', 150534, 318], ['2024-05-23', 148702, 310], ['2024-05-24', 171465, 278], ['2024-05-25', 192166, 266], ['2024-05-26', 147174, 425], ['2024-05-27', 145039, 425], ['2024-05-28', 146308, 469], ['2024-05-29', 144620, 469], ['2024-05-30', 141199, 472], ['2024-05-31', 149080, 414], ['2024-06-01', 168865, 338], ['2024-06-02', 135050, 483], ['2024-06-03', 136555, 475]]

    date_prices = sorted(date_prices, key=lambda x: x[2])
    date_prices.reverse()

    cnt = math.floor(len(date_prices) * target / 100)
    date_prices = date_prices[0:cnt]

    date_prices = sorted(date_prices, key=lambda x: x[1])
    
    low_price_date = date_prices[0][0]
    high_price_date = date_prices[-1][0]

    print(low_price_date, high_price_date)

    sql = """
        select
            plan_discount_price
        from
            plans_search
        where
            hotel_id = %s
            and ppc = %s
            and checkin = %s
        order by
            plan_discount_price asc
        limit 1
    """
    results = {}
    for hotel_id in hotels:
        for i in range(1, 3):
            cursor.execute(sql, (hotel_id, i, low_price_date))
            r = cursor.fetchone()
            if hotel_id not in results:
                results[hotel_id] = []
            if r:
                results[hotel_id].append([i, r[0]])
            else:
                results[hotel_id].append([i, '-'])
    low_price_results = results

    results = {}
    for hotel_id in hotels:
        for i in range(1, 3):
            cursor.execute(sql, (hotel_id, i, high_price_date))
            r = cursor.fetchone()
            if hotel_id not in results:
                results[hotel_id] = []
            if r:
                results[hotel_id].append([i, r[0]])
            else:
                results[hotel_id].append([i, '-'])
    high_price_results = results

    # pprint(low_price_date)
    # pprint(low_price_results)

    # pprint(high_price_date)
    # pprint(high_price_results)

    hotel_info = []
    for hotel_id in hotels:
        cursor.execute('select hotel_id, hotel_name from plans_search where hotel_id = %s limit 1', (hotel_id,))
        r = cursor.fetchone()
        hotel_info.append([r[0], r[1]])

    ret = {}
    ret['hotels'] = hotel_info
    ret['dates']= {'low': low_price_date, 'high': high_price_date}
    ret['low'] = low_price_results
    ret['high'] = high_price_results

    return json.dumps(ret, ensure_ascii=False)

if __name__ == "__main__":
    r = main()
    print(r)
