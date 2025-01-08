import requests
import sys
import time
import os
import re

files = os.listdir('pages')

links = []
for file in files:
    f = open('pages/{}'.format(file), 'r', encoding='UTF-8')
    data = f.read()
    f.close()

    result_grep = re.findall(r'a href="(/\d+/)\?accommodation_types=', data)
    result_set = set(result_grep)
    results = list(result_set)

    for result in results:
        links.append(result)

with open('hotel_lists.txt', 'w') as f:
    for link in links:
        f.write('{}\n'.format(link))

print(len(links))