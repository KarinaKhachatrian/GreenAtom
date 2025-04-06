import pandas as pd
import streamlit as st

df = pd.read_csv('flight.csv')

df = df.dropna(subset=['latitude', 'longitude'])
st.title('Отображение полётов на карте')

icao_codes = ['Все'] + sorted(df['icao_code'].dropna().unique().tolist())
selected_icao = st.selectbox('Выберите ICAO код авиакомпании:', icao_codes)

if selected_icao != 'Все':
    filtered_df = df[df['icao_code'] == selected_icao]
else:
    filtered_df = df

st.map(filtered_df[['latitude', 'longitude']])