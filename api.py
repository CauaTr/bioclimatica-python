import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
import funcoes as fc

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": -23.5325,
	"longitude": -46.7917,
	"daily": ["temperature_2m_max", "temperature_2m_min"],
	"hourly": "rain",
	"timezone": "America/Sao_Paulo",
}
responses = openmeteo.weather_api(url, params = params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_rain = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}

hourly_data["rain"] = hourly_rain

hourly_dataframe = pd.DataFrame(data = hourly_data)
#print("\nHourly data\n", hourly_dataframe)
# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()

daily_data = {
	"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}

daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min

daily_dataframe = pd.DataFrame(data = daily_data)

temperatura_maxima = 30
temperatura_minima = 15

lista_temperaturas = []
for c, i in enumerate(daily_dataframe['date']):
		lista_temperaturas.append(fc.analisar_temperatura(temperatura_minima, temperatura_maxima, daily_dataframe, c))

print(lista_temperaturas)

'''lista = []
lista_rain = []
numeros = []
data = ''
contador = 0
for c, i in enumerate(hourly_dataframe['date']):
    if c == 0:
        data = str(i)[0:10]
    if str(i)[0:10] != data:
        data = str(i)[0:10]
    if data not in lista:
        lista.append(data)
    if lista[contador] in str(i) and c != len(hourly_dataframe['date'])-1:
        if len(lista_rain) == 0:
            lista_rain.append(str(hourly_dataframe['date'][c])) 
            lista_rain.append(float(str(hourly_dataframe['rain'][c])))
        else:
            if float(str(hourly_dataframe['rain'][c])) > lista_rain[1]:
                lista_rain[0] = str(i)[11:19]
                lista_rain[1] = float(str(hourly_dataframe['rain'][c]))
    else:
        numeros.append(list(lista_rain))
        lista_rain.clear()
        contador += 1
        lista_rain.append(str(hourly_dataframe['date'][c])[11:19])
        lista_rain.append(float(str(hourly_dataframe['rain'][c])))

print("Lista de Datas: ", lista)
print("lista de Numeros: ", numeros)'''
    
        
        
		

"""magos = hourly_dataframe['date'][1]
print(magos)
print(type(str(magos)))
print('2026-11-13' in str(magos))"""