import os

files = os.listdir('data/success')

for file in files:
    os.remove('data/success/{}'.format(file))

files = os.listdir('data')

for file in files:
    try:
        os.remove('data/{}'.format(file))
    except:
        pass
