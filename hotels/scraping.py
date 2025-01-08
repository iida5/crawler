import bs4
import os
import sys
import re

hotels = os.listdir('hotels')

f = open('hotels.txt', 'w')

for hotel in hotels:
    print(hotel)
    soup = bs4.BeautifulSoup(open('hotels/{}'.format(hotel), 'r'), 'lxml')

    title = soup.select_one(r'#__nuxt > div > div.min-h-screen > main > div.pc-guide-xl\:flex.w-screen-xl.mx-auto.justify-between > div.w-screen-pc-guide.pc-guide-xl\:mx-0.mx-auto > div:nth-child(1) > div.mx-auto.mt-3.flex.items-start.justify-between > div > div > h1').get_text(strip=True)
    area = soup.select_one(r'#__nuxt > div > div.min-h-screen > main > div.pc-guide-xl\:flex.w-screen-xl.mx-auto.justify-between > div.w-screen-pc-guide.pc-guide-xl\:mx-0.mx-auto > div:nth-child(1) > div.mx-auto.mt-3.flex.items-start.justify-between > div > div > a').get_text(strip=True)
    room_count = soup.select_one(r'#__nuxt > div > div.min-h-screen > main > div.pc-guide-xl\:flex.w-screen-xl.mx-auto.justify-between > div.w-screen-pc-guide.pc-guide-xl\:mx-0.mx-auto > div.flex.w-full.justify-between > div.mr-8.w-\[585px\] > section:nth-child(3) > table > tbody > tr:nth-child(3) > td').get_text(strip=True)
    # for i in range(13, 17):
        if soup.select_one(r'#__nuxt > div > div.min-h-screen > main > div.pc-guide-xl\:flex.w-screen-xl.mx-auto.justify-between > div.w-screen-pc-guide.pc-guide-xl\:mx-0.mx-auto > section:nth-child({}) > div.bg-gray-100.rounded-md.p-3.text-md > span:nth-child(2)'.format(i)):
            tag = '#__nuxt > div > div.min-h-screen > main > div.pc-guide-xl\:flex.w-screen-xl.mx-auto.justify-between > div.w-screen-pc-guide.pc-guide-xl\:mx-0.mx-auto > section:nth-child({})'.format(i)

    postal_code = soup.select_one(r'{} > div.bg-gray-100.rounded-md.p-3.text-md > span:nth-child(2)'.format(tag)).get_text(strip=True)
    pref = soup.select_one(r'{} > div.bg-gray-100.rounded-md.p-3.text-md > span:nth-child(4)'.format(tag)).get_text(strip=True)
    address = soup.select_one(r'{} > div.bg-gray-100.rounded-md.p-3.text-md > span:nth-child(5)'.format(tag)).get_text(strip=True)
    iframe_src = soup.select_one(r'{} > iframe'.format(tag)).get('src')
    
    print(title)
    print(area)
    print(room_count)
    print(postal_code)
    print(pref)
    print(address)

    sys.exit()

    title = title.replace(',','.')
    
    r = re.search('q=(.*?),(.*?)&', iframe_src).groups()
    lat = r[0]
    lon = r[1]
    hotel_id = hotel.replace('.html', '')
    print(1, hotel_id, title, area, room_count, postal_code, pref, address, lat, lon)
    # sys.exit()
    f.write('{},{},{},{},{},{},{},{},{},{},\n'.format(1, hotel_id, title, area, room_count, postal_code, pref, address, lat, lon))
print('end')
# print(hotels)
