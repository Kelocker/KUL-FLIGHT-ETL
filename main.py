import requests
import os
from dotenv import load_dotenv
import pandas as pd
import sqlite3


load_dotenv()
API_key = os.getenv('API_KEY')
Base_URL = 'http://api.aviationstack.com/v1/flights'
db_file = sqlite3.connect('flight.db')

query_params = {
    'access_key': API_key,
    'dep_iata': 'KUL',
    'limit': 10,
}

response = requests.get(Base_URL, params=query_params)
if response.status_code == 200:
    print('Success')
    data = response.json()
    df = pd.json_normalize(data['data'])

    df['departure.scheduled'] = pd.to_datetime(df['departure.scheduled'])
    df['myt_time'] = df['departure.scheduled'].dt.tz_convert('Asia/Kuala_Lumpur')
    df['TIME'] = df['myt_time'].dt.strftime('%H:%M')
    
    selected_data = {
        'TIME': 'TIME',
        'airline.name': 'AIRLINE',
        'flight.iata': 'FLIGHT',
        'arrival.iata': 'DESTINATION',
        'flight_status': 'REMARKS'
    }

    df_clean = df[list(selected_data.keys())].rename(columns=selected_data)
    df_clean = df_clean.astype(str).apply(lambda x: x.str.upper())
    df_clean.to_sql('flights', db_file, if_exists='replace', index=False)
    db_file.close()


else:
    print(f'Failed with status code:{response.status_code}')
    print(response.json())
