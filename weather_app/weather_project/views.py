import datetime
import requests
from django.shortcuts import render


def index(request):
    API_KEY = open("API_KEY", "r").read()
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST.get["city1"]
        city2 = request.get["city2", None]
    else:
        return render(request, "weather_app/index.html")

def fetch_weather_forecast(city, API_KEY, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, API_KEY)).json()
    lat, long = response["coord"]["lat"], response["coord"]["lon"]
    forecast_response = requests.get(forecast_url.format(lat, long, API_KEY)).json()

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15 * 9 / 5 + 32, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
    }

    # Forecast for the next 5 days
    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            "min_temp": round(daily_data['temp']['min'] - 273.15 * 9 / 5 + 32, 2),
            "max_temp": round(daily_data['temp']['max'] - 273.15 * 9 / 5 + 32, 2),
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts