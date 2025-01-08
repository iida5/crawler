import mysql.connector
from pprint import pprint
import json
import sys

sys.path.append('../config')
from config import Config

def main():
    sql = """
    select
        area_class,
        checkin,
        sum(room_inventory) as cnt
    from (
        select
            distinct(room_id), 
            area_class, 
            checkin, 
            room_inventory
        from
            plans_search
        where ppc = 2
    ) as area 
    group by
        area_class, 
        checkin 
    order by 
        checkin asc
    """

    config = Config()
    conn = mysql.connector.connect(
        host=config.mysql_host,
        port=config.mysql_port,
        user=config.mysql_user,
        password=config.mysql_password,
        database=config.mysql_database
    )

    cursor = conn.cursor()

    ret = cursor.execute(sql)
    rows = cursor.fetchall()


    # areas = ['札幌', '仙台', '金沢', 'ディズニー', '東京', '箱根', '京都', '名古屋', '大阪', '福岡', '沖縄']

    areas = [
        '札幌・北海道',
        '仙台・東北',
        '北陸',
        '長野・軽井沢',
        '東京',
        '横浜',
        '箱根',
        '舞浜・東京ベイサイド',
        '名古屋',
        '京都',
        '伊勢志摩',
        '大阪',
        '神戸',
        '広島',
        '四国',
        '福岡',
        '九州その他',
        '沖縄・宮古島',
    ]


    datas = {}
    for area in areas:
        datas[area] = []

    a_datas = {}
    for area in areas:
        a_datas[area] = []

    for row in rows:
        area = row[0]
        checkin = row[1].strftime('%Y-%m-%d')
        inventory = int(row[2])
        datas[area].append([checkin, inventory])


    for k, data in datas.items():
        max_inventory = 0
        for row in data:
            if row[1] > max_inventory:
                max_inventory = row[1]
        for row in data:
            inventory_per = int(row[1]) / max_inventory
            if inventory_per < 0.3:
                row.append('LOW')
            elif inventory_per < 0.7:
                row.append('MIDDLE')
            else:
                row.append('HIGH')

            a_datas[k].append(row)

    return json.dumps(a_datas, ensure_ascii=False)

if __name__ == "__main__":
    r = main()
    print(r)