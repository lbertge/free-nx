from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import json

def scrape(event, context):
    method()
    time.sleep(10) # sleep in case we're too fast
    method()

def method():
    with requests.Session() as session:
        with open('data/example.json') as f:
            data = json.load(f)
        post = session.post(data['loginPage'], data=data['credentials'])

        try_times = []
        for page in data['postLogin']:
            for i in range(4):
                vote = session.post(page, data={'toplist': i})
                content = BeautifulSoup(vote.content, 'html.parser')

                try:
                    get_time = re.search('\d:\d+:\d+', str(content.find('p'))).group(0)
                    try_times.append((datetime.strptime(get_time, '%H:%M:%S')-datetime(1900,1,1)).total_seconds())
                except AttributeError:
                    pass

        if len(try_times) > 0:
            max_try_time = max(try_times)
            print("Retrying in", max_try_time, "seconds")
