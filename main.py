import requests
import csv
import datetime as dt



def get_date_ISO():
    '''
    This requires no input, but will prompt a use for an ISO date format
    Output: date object in ISO 8601 date format
    '''
    input_date = input("Input date in ISO format (YYYY-MM-DD): ")
    return dt.date.fromisoformat(input_date)

def query_date(ISO_date):
    pass

params = {
    'start_date': dt.date.fromisoformat("2024-03-01"),
    'end_date' : dt.date.fromisoformat("2024-03-31"),
    'base_link' : "https://www.ncei.noaa.gov/access/services/data/v1",
    'dataset' :'',
    'station':'BGM',
    'station_url' : f'',
    'datatypes' : ['TMAX', 'TMIN', 'PRCP'],
    'units' : 'standard',

}
