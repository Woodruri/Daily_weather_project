import requests
import json
import pprint
import datetime


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

def get_daily_info(given_date="2024-04-01"):
    data = {
        'params': json.dumps({
            "elems": [
                {"name": "maxt"}, {"name": "mint"}, {"name": "avgt"}, {"name": "pcpn"},
                {"name": "snow"}
            ],
            "sid": "AVPthr 9",
            "date": given_date,
            "meta": ["name", "state", "sids"]
        }),
        'output': 'json'
    }

    resp = s.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        print("error occured while getting daily data")
        return 

    weather_data = json.loads(resp.text)
    #pprint.pprint(weather_data)
    daily_data = {
        "date" : weather_data['data'][0][0],
        "maxt" : weather_data['data'][0][1],
        "mint" : weather_data['data'][0][2],
        "avgt" : weather_data['data'][0][3],
        "precip" : weather_data['data'][0][4],
        "snow" : weather_data['data'][0][5]
    }
    return daily_data


def get_record_info(start_date="1901-04-01", end_date="2024-04-01"):
    data = {
        'params': json.dumps({
            "elems": [
                #record snowfall
                {
                    "name": "snow",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                #max temperature
                {
                    "name": "maxt",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                #min temp
                {
                    "name": "mint",
                    "interval": [1, 0, 0],
                    "smry": [
                        {"reduce": "max", "add": "date"},
                        {"reduce": "min", "add": "date"}
                    ],
                    "smry_only": 1
                },
                #max/min precipitation
                {
                    "name":"pcpn"
                    ,"interval":[1,0,0],
                    "smry": [
                        {"reduce":"max","add":"date"},
                        {"reduce":"min","add":"date"}],
                        "smry_only":1
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
        print("error occured while getting historic data")
        return 

    weather_data = json.loads(resp.text)
    #pprint.pprint(weather_data)
    
    record_info = {
        "record_high_snow" : weather_data['smry'][0][0][0],
        "record_low_snow" : weather_data['smry'][0][1][0],
        "record_high_high_temp" : weather_data['smry'][1][0][0],
        "record_low_high_temp" : weather_data['smry'][1][1][0],
        "record_high_low_temp" : weather_data['smry'][2][0][0],
        "record_low_low_temp" : weather_data['smry'][2][1][0],
        "record_high_precip" : weather_data['smry'][3][0][0],
        "record_low_precip" : weather_data['smry'][3][1][0]
    }

    return record_info

def get_normal_info(given_date="2024-04-01"):
    data = {
        'params': json.dumps({
            "elems": [
                {"name": "maxt", "duration": "dly", "normal": "91", "prec": 1},
                {"name": "mint", "duration": "dly", "normal": "91", "prec": 1},
                {"name": "avgt", "duration": "dly", "normal": "91"},
                {"name": "pcpn", "duration": "dly", "normal": "91"},
                {"name": "snow", "duration": "dly", "normal": "91"},
            ],
            "sid": "AVPthr 9",
            "meta": [],
            "date": given_date
        }),
        'output': 'json'
    }
    resp = s.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        print("error occured while getting historic data")
        return 

    weather_data = json.loads(resp.text)
    #pprint.pprint(weather_data)
    normal_info = {
        "maxt" : weather_data['data'][0][0],
        "mint" : weather_data['data'][0][1],
        "avgt" : weather_data['data'][0][2],
        "precip" : weather_data['data'][0][3],
        "snow" : weather_data['data'][0][4]
    }
    return normal_info

def get_info():
    get_daily_info()
    get_normal_info()
    get_record_info()