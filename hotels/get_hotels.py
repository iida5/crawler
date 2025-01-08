import requests
import sys
import time

f = open('hotel_lists.txt', 'r')
hotels = f.read().splitlines()

for hotel in hotels:
    hotel_id = hotel.split('/')[1]
    link = 'https://www.ikyu.com/{}'.format(hotel)
    page = requests.get(link)
    with open('hotels/{}.html'.format(hotel_id), 'wb') as f:
        f.write(page.content)

    time.sleep(1)
