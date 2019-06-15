import requests
from datetime import datetime


url = 'https://etherscan.io/uncles?p='
data = dict()


def get_fork_page(url):
    content = requests.get(url).text
    uncles = content.split("href='/uncle/")[1:]
    for each in uncles:
        hash = each.split("'")[0]
        time = each.split("title='")[2].split("'")[0]
        time = datetime.strptime(time, '%b-%d-%Y %I:%M:%S %p').strftime("%Y-%m-%d")
        data[hash] = time


def prepare_hist():
    counts = dict()
    with open('./forks.csv', 'a') as f:
        for hash, time in data.items():
            f.write(f"{hash},{time}\n")
            counts[time] = 1 if time not in counts else counts[time] + 1
    for k, v in counts.items():
        print(f"{k}: {v}")


for i in range(3801, 10000):
    print(f"{url}{i}")
    get_fork_page(f"{url}{i}")
    if i % 100 == 0:
        prepare_hist()
        data = dict()
