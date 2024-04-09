import requests
import json
import pprint
import datetime
import urllib


s = requests.Session()

url = "https://data.rcc-acis.org/StnData"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://nowdata.rcc-acis.org',
    'Connection': 'keep-alive',
    'Referer': 'https://nowdata.rcc-acis.org/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}

def get_snow(start_date="1901-04-01", end_date="2024-04-01"):
    data = {
        'params': json.dumps({
            "elems": [
                {
                    "name": "snow",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                {
                    "name": "snow",
                    "duration": "mtd",
                    "reduce": "sum",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                {
                    "name": "snow",
                    "duration": "std",
                    "reduce": "sum",
                    "season_start": "07-01",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                }
            ],
            "sid": "AVPthr 9",
            "meta": [],
            "sDate": start_date,
            "eDate": end_date
        }),
        'output': 'json'
    }

    resp = s.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        print("error occured while getting snow data")
        return

    weather_data = json.loads(resp.text)
    record_high = weather_data['smry'][0][0][0]
    record_low = weather_data['smry'][0][1][0]

    print(f'record high = {record_high}\nrecord low = {record_low}')

def get_max_temp(start_date="1901-04-01", end_date="2024-04-01"):
    data = {
        'params': json.dumps({
            "elems": [
                {
                    "name": "snow",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                {
                    "name": "snow",
                    "duration": "mtd",
                    "reduce": "sum",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                {
                    "name": "snow",
                    "duration": "std",
                    "reduce": "sum",
                    "season_start": "07-01",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                }
            ],
            "sid": "AVPthr 9",
            "meta": [],
            "sDate": start_date,
            "eDate": end_date
        }),
        'output': 'json'
    }

    resp = s.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        print("error occured while getting snow data")
        return

    weather_data = json.loads(resp.text)
    record_high = weather_data['smry'][0][0][0]
    record_low = weather_data['smry'][0][1][0]

    print(f'record high = {record_high}\nrecord low = {record_low}')

get_snow()