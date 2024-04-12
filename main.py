import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import csv
import pprint
from bs4 import BeautifulSoup
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

'''
I don't wnat to get rid of this, but it's got too much stuff I need to do to make it happen xd
def get_sid():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    climate_url = "https://www.weather.gov/wrh/Climate"

    resp = s.get(climate_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    map_stuff = soup.find('map', {'name' : 'cwa'})
    locations = map_stuff.find_all('area')

    for area in locations:
        name = area['name']
        url = area['href']
        print(name)
        print(url)
        print()
    
    selection = input("Enter the 3 character string at the end of the URL to show the areas and their sids: ")
    area_url = f"https://www.weather.gov/wrh/Climate?wfo={selection}"


    driver.get(area_url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    station_list = soup.find(name='station')
    print(type(station_list))
 

    if resp.status_code != 200:
        print("incorrect code entered")
        return
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    print(soup)
    station_list = soup.find({'name': 'station'})
    print(type(station_list))
    
    driver.quit()
    '''

def is_valid_date(date):
    try:
        test_date = datetime.strptime(date, '%Y-%m-%d')
    except TypeError as e:
        print("Invalid date format or type. \nError: ", e)
        return False
    except ValueError as e:
        print("Improper date input, likely out of range. \nError: ", e)
        return False
    except Exception as e:
        print("you did something wrong and im not sure what. \nError: ", e)
        return False
    return True

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
        "state" : weather_data['meta']['state'],
        "stationId" : weather_data['meta']['sids'][0],
        "area" : weather_data['meta']['name'],
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

    output_dict = []    

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

    #this is naive, I could async or multiprocess to do it much faster, you'd jut have to sort by date afterwards
    while current_date <= final_date:
        curr_data = get_info(current_date.strftime('%Y-%m-%d'))
        output_dict.append(curr_data)
        current_date += timedelta(days=1)
    
    # Writing to CSV
    if output_dict:
        keys = output_dict[0].keys()  # Getting the column names from the first item
        with open('data.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(output_dict)
        print("Data written to data.csv")
    else:
        print("No data to write.")

def prompt_info():
    print("Welcome to Riley's Weather Daily info Automator")
    print("For this you will need to enter your dates in the format (YYYY-MM-DD)")
    print("You will also need your station ID for the area you need, Riley can show you how to get this")
    print("The general idea is that you will go here: https://www.weather.gov/wrh/Climate")
    print("Find your region and then the area that you need info from")
    print("Open up your browser's network analyzer and have it start recording")
    print("Select the daily almanac and query for any date")
    print("inside of any of the StnData packets under the request section will be a value called 'sid'")
    print("the value stored inside of sid will have your station's id, copy that and that will be your sid")
    print("AVPthr 9")

    begin_date = input("Input your begin date: ")
    if not is_valid_date(begin_date):
        print(f'{begin_date} is not a valid date')
        return

    end_date = input("Input your final date: ")
    if not is_valid_date(end_date):
        print(f'{end_date} is not a valid date')
        return
    
    sid = input("Enter your sid, please ensure that this is correct because I'm not doing error checking for it: ")

    get_info_range(begin_date, end_date, sid)

def main():
    prompt_info()

if __name__ == '__main__':
    main()