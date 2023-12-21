import requests
import datetime
import pandas as pd


def get_weather():
    cities = ['New York', 'London', 'Paris', 'Vienna', 'Madrid'] 
    api_key = WEATHER_API_KEY
    def get_weather_from_api(cities, api_key):
        total_data = []
        for city in cities:
            r = requests.get('http://api.weatherstack.com/current?access_key='+ api_key +'&query='+ city +'')
            data = r.json()
            total_data.append(data)
        return total_data
            
    total_data = get_weather_from_api(cities, api_key)

    
    def flatten_data(data):
        total_data_flat = []
        for data_ in data:
            data_flat = {**data_['request'], **data_['location'], **data_['current']}
            total_data_flat.append(data_flat)
        return total_data_flat

    total_data_flat = flatten_data(total_data)

    df_all = pd.DataFrame(total_data_flat)

    df_input = df_all.drop(['type', 'language', 'unit', 'country', 'region', 'lat', 'lon', 'timezone_id',
                            'localtime_epoch', 'utc_offset', 'observation_time', 'weather_code', 'weather_icons',
                        'wind_degree', 'wind_dir', 'pressure', 'humidity'], axis=1)

    df_input['localtime'] = pd.to_datetime(df_input['localtime'])
    df_input['time'] = df_input['localtime'].apply(lambda x: x.time())
    df_input['date'] = df_input['localtime'].apply(lambda x: x.date())
    df_input = df_input.drop("localtime", axis=1)

    df_input = df_input.drop(["date","query","time"],axis=1)
    return df_input
