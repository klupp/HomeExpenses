import pandas as pd
import numpy as np
import requests
from datetime import date, timedelta, datetime


location = {
    'lat': 50.774051,
    'lon': 6.075709,
    'city': 'Aachen',
    'zip': 52064,
    'data_loc': '/home/aleks/Documents/my_documents/home/Aachen/Utilities/aachen_weather.csv',
    'hour_data_loc': '/home/aleks/Documents/my_documents/home/Aachen/Utilities/aachen_hourly_weather.csv'
}


def update_weather():
    weather_df = pd.read_csv(location['data_loc'])
    weather_df['date'] = pd.to_datetime(weather_df['date'])

    hourly_weather_df = pd.read_csv(location['hour_data_loc'])
    hourly_weather_df['datetime'] = pd.to_datetime(hourly_weather_df['datetime'])

    today = date.today()
    end_date = today - timedelta(days=1)
    last_stored_date = weather_df.loc[weather_df.shape[0] - 1, 'date'].date()

    if last_stored_date is None:
        start_date = today - timedelta(days=4)
    else:
        start_date = last_stored_date + timedelta(days=1)

    while (start_date <= end_date):
        requested_date = datetime(year=start_date.year, month=start_date.month, day=start_date.day)
        dt = int(requested_date.timestamp())

        url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"

        querystring = {"lat":str(location['lat']),"lon":str(location['lon']),"dt":str(dt)}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "5726c8221dmsh68d4b0b272e8055p1dc4c5jsn6e9d7d0b1d6f"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        result = response.json()

        kelvins = np.array([hour['temp'] for hour in result['hourly']])
        celsius = np.around(kelvins - 273.15, 2)
        weather_df = weather_df.append({
            'city': location['city'], 
            'zip': location['zip'], 
            'lat': location['lat'], 
            'lon': location['lon'], 
            'date': requested_date,
            'low_temp': min(celsius),
            'high_temp': max(celsius),
            'data': str(result)}, ignore_index=True);

        start_date = start_date + timedelta(days=1)

        for hour in result['hourly']:
            celsius = np.around(hour['temp'] - 273.15, 2)
            hour_time = datetime.fromtimestamp(hour['dt'])
            hourly_weather_df = hourly_weather_df.append({
            'city': location['city'], 
            'zip': location['zip'], 
            'lat': location['lat'], 
            'lon': location['lon'], 
            'datetime': hour_time,
            'temp': celsius,
            'data': str(hour)}, ignore_index=True);


    weather_df.to_csv(location['data_loc'], index=False)
    hourly_weather_df.to_csv(location['hour_data_loc'], index=False)
    

if __name__ == "__main__":
    update_weather()