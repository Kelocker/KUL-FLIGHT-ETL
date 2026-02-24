import requests
import os
from dotenv import load_dotenv
import datetime
import pandas as pd
import sqlite3

today = datetime.datetime.now().strftime("%Y-%m-%d")
db_file = sqlite3.connect('flight.db')

load_dotenv()
API_key = os.getenv('API_KEY')
Base_URL = 'http://api.aviationstack.com/v1/flights'

query_params = {
    'access_key': API_key,
    'dep_iata': 'KUL',
    'limit': 5,
}

response = requests.get(Base_URL, params=query_params)
if response.status_code == 200:
    print('Success')
    data = response.json()

    first_flight = data['data']
    df = pd.json_normalize(first_flight)

    selected_data = [
        'flight_date', 
        'flight_status', 
        'airline.name', 
        'flight.iata', 
        'departure.iata', 
        'arrival.iata', 
        'departure.scheduled',
        'departure.delay'
    ]

    df_clean = df[selected_data]
    
    df_clean = df_clean.rename(columns={
        'airline.name': 'airline_name',
        'flight.iata': 'flight_number',
        'departure.iata': 'dep_airport',
        'arrival.iata': 'arr_airport',
        'departure.scheduled': 'scheduled_departure',
        'departure.delay': 'delay_minutes'
    })

    df_clean['delay_minutes'] = df_clean['delay_minutes'].fillna(0).astype(float)
    df_clean.to_sql('flights', db_file, if_exists='append', index=False)


else:
    print(f'Failed with status code:{response.status_code}')
    print(response.json())
