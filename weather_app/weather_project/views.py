import datetime
import requests
from django.shortcuts import render

class InvalidApiKey(Exception):
    def __init__(self, message="Invalid API Key"):
        self.message = message
        super().__init__(self.message)

def index(request):
    API_KEY = "YOUR_API_KEY"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    if request.method == "POST":
        city1 = request.POST["city1"]
        city2 = request.POST.get("city2", None)

        try:
            weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)
            if city2:
                weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
            else:
                weather_data2, daily_forecasts2 = None, None
        except InvalidApiKey:
            return render(request, "weather_app/index.html", {'error_message': "We couldn't get weather info."})
        except KeyError:
            return render(request, "weather_app/index.html")

        context = {
            "weather_data1" : weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2" : weather_data2,
            "daily_forecasts2": daily_forecasts2
        }

        return render(request, "weather_app/index.html", context)

    else:
        return render(request, "weather_app/index.html")


def fetch_weather_and_forecast(city, API_KEY, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, API_KEY)).json()
    if response['cod'] == 401:
        raise InvalidApiKey

    lat, lon = response['coord']['lat'], response['coord']['lon']

    forecast_response = requests.get(forecast_url.format(lat, lon, API_KEY)).json()

    weather_data = {
        "city": city,
        "temperature": round(response["main"]["temp"] - 273.15, 2),
        "desc": response["weather"][0]["description"],
        "icon": response["weather"][0]["icon"]
    }

    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
            "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
            "desc": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon']
        })

    return weather_data, daily_forecasts