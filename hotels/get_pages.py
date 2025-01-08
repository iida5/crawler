import requests
import sys
import time

for i in range(1, 75):
    link = 'https://www.ikyu.com/area/ma000000/p{}/?accommodation_types=HOTEL,RESORT_HOTEL&adc=1&lc=1&per_page=20&pn=1&ppc=2&rc=1&si=6'.format(i)
    page = requests.get(link)
    with open('pages/{}.html'.format(i), 'wb') as f:
        f.write(page.content)
    time.sleep(1)
