import requests
import json
import pprint
from datetime import datetime, timedelta


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

def get_daily_info(given_date="2024-04-01", sid="AVPthr 9"):
    data = {
        'params': json.dumps({
            "elems": [
                {"name": "maxt"}, {"name": "mint"}, {"name": "avgt"}, {"name": "pcpn"},
                {"name": "snow"}
            ],
            "sid": sid,
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

def get_record_info(start_date="1901-04-01", end_date="2024-04-01", sid="AVPthr 9"):
    data = {
        'params': json.dumps({
            "elems": [
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
                },
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
            ],
            "sid": sid,
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
        "high_maxt" : weather_data['smry'][0][0][0],
        "low_maxt" : weather_data['smry'][0][1][0],
        "high_mint" : weather_data['smry'][1][0][0],
        "low_mint" : weather_data['smry'][1][1][0],
        "high_precip" : weather_data['smry'][2][0][0],
        "low_precip" : weather_data['smry'][2][1][0],
        "high_snow" : weather_data['smry'][3][0][0],
        "low_snow" : weather_data['smry'][3][1][0],
    }

    return record_info

def get_normal_info(given_date="2024-04-01", sid="AVPthr 9"):
    data = {
        'params': json.dumps({
            "elems": [
                {"name": "maxt", "duration": "dly", "normal": "91", "prec": 1},
                {"name": "mint", "duration": "dly", "normal": "91", "prec": 1},
                {"name": "avgt", "duration": "dly", "normal": "91"},
                {"name": "pcpn", "duration": "dly", "normal": "91"},
                {"name": "snow", "duration": "dly", "normal": "91"},
            ],
            "sid": sid,
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

def get_info(given_date="2024-04-01", sid="AVPthr 9"):

    #add something here to ensure valid date format

    start_date = f'1901-{given_date[-5:]}'
    daily_info = get_daily_info(given_date, sid)
    normal_info = get_normal_info(given_date, sid)
    record_info = get_record_info(start_date, given_date, sid)

    """print(f'daily = {daily_info}\n\n'
          f'normal = {normal_info}\n\n'
          f'record = {record_info}\n\n')"""
    
    full_info = {
        'date' : daily_info['date'],
        'daily_maxt' : daily_info['maxt'],
        'daily_mint' : daily_info['mint'],
        'daily_avgt' : daily_info['avgt'],
        'daily_precip' : daily_info['precip'],
        'daily_snow' : daily_info['snow'],
        #normal info
        'normal_maxt' : normal_info['maxt'],
        'normal_mint' : normal_info['mint'],
        'normal_avgt' : normal_info['avgt'],
        'normal_precip' : normal_info['precip'],
        'normal_snow' : normal_info['snow'],
        #record info
        'record_high_maxt' : record_info['high_maxt'],
        'record_low_maxt' : record_info['low_maxt'],
        'record_high_mint' : record_info['high_mint'],
        'record_low_mint' : record_info['high_mint'],
        'record_high_precip' : record_info['high_precip'],
        'record_low_precip' : record_info['low_precip'],
        'record_high_snow' : record_info['high_snow'],
        'record_low_snow' : record_info['low_snow'],
    }

    return full_info

def get_info_range(start_date = "2024-03-01", end_date="2024-03-07", sid="AVPthr 9"):
    

    try:
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        final_date = datetime.strptime(end_date, '%Y-%m-%d')
    except TypeError as e:
        print("Invalid date format or type. \nError: ", e)
        return
    except ValueError as e:
        print("Improper date input, likely out of range. \nError: ", e)
        return
    except Exception as e:
        print("you did something wrong and im not sure what. \nError: ", e)
        return

    while current_date <= final_date:
        curr_data = get_info(current_date.strftime('%Y-%m-%d'))
        print(curr_data)
        current_date += timedelta(days=1)



get_info_range("2024-04-01", "2024-04-08")
