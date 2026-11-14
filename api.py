import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

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
	"hourly": ["temperature_2m", "rain"],
	"timezone": "America/Sao_Paulo",
}
responses = openmeteo.weather_api(url, params = params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_rain = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["rain"] = hourly_rain

hourly_dataframe = pd.DataFrame(data = hourly_data)
#print("\nHourly data\n", hourly_dataframe)

temperatura_max = 20
temperatura_min = 15
normal = []
acima = []
abaixo = []
for c, i in enumerate(hourly_dataframe['temperature_2m']):
    if i > temperatura_max:
        acima.append(str(hourly_dataframe['date'][c])[0:10])
        acima.append(str(hourly_dataframe['temperature_2m'][c]))
    elif i < temperatura_min:
        abaixo.append(str(hourly_dataframe['date'][c])[0:10])
        abaixo.append(str(hourly_dataframe['temperature_2m'][c]))
    else:
        normal.append(str(hourly_dataframe['date'][c])[0:10])
        normal.append(str(hourly_dataframe['temperature_2m'][c]))

print(normal)
print(acima)
print(abaixo)
"""magos = hourly_dataframe['date'][1]
print(magos)
print(type(str(magos)))
print('2026-11-13' in str(magos))"""