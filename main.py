import requests
import csv
import datetime as dt

'''station is bgm (avoca area)'''
base_url = 'https://www.ncei.noaa.gov/access/services/data/v1?'
start_date= dt.date.fromisoformat("2024-03-01")
end_date = dt.date.fromisoformat("2024-03-31")

s = requests.Session()

headers = {
    'Token' : 'uRaFEaZsYIOyjgUqrtVWpjybZhFLZpIt'
}
params = {
    'datasetid': 'daily_summaries',
    'stationid': 'GHCND:USW00004725',  # Replace with your station ID
    'startdate': start_date,
    'enddate': end_date,
    'datatypeid': ['TMAX', 'TMIN', 'PRCP'],  # Adjust based on needed data types
    'units': 'standard',
    'limit': 1000,
}

def get_date_ISO():
    '''
    This requires no input, but will prompt a use for an ISO date format
    Output: date object in ISO 8601 date format
    '''
    input_date = input("Input date in ISO format (YYYY-MM-DD): ")
    return dt.date.fromisoformat(input_date)

def query_date(ISO_date):
    '''
    This will take in one ISO date format and use the other information provided to query the API
    input: 
    date object with ISO date
    output:
    probably a custom object with all the fields, im deciding atm
    '''

def build_url(dataset='daily_summaries', stationId='USW00004725', startDate='2024-03-01', endDate='2024-03-31', dataTypes=''):
    '''
    this function will take all of our variables used in seperate locations
    to make our url with all of the proper arguments
    input:
    dataset (string): a string that contains the name of the dataset we'll be querying on the website
    stationId (string): a string that has the station ID of the station we'll be querying

    output:
    string: a string that is the full url with all arguments filled out
    '''
    dataset_string = f'dataset={dataset}'
    station_string = f'stations={stationId}'
    start_string = f'startDate={startDate}'
    end_string = f'endDate={endDate}'
    data_types_string = f'dataTypes={dataTypes}'

    url = f'{base_url}{dataset_string}&{station_string}&{start_string}&{end_string}&{data_types_string}'
    return url




def main():
    url = build_url()    
    resp = s.get(url, headers=headers)
    print(resp.text)

if __name__ == '__main__':
    main()