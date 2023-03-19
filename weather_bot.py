# Imports
import requests as rq
from datetime import datetime as dt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Return response from OpenWeather for your city
def get_weather_forecast():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/forecast" # 5 day weather forecast
    city = os.getenv("OPEN_WEATHER_CITY")
    payload = {"q": city, "appid": api_key, "units": "metric"}

    return rq.get(base_url, params=payload)

# Function to send custom message to Weather Channel
def send_message(message):
    bot_key = os.getenv("BOT_API_KEY")
    url =  "https://api.telegram.org/bot" + bot_key
    chat_id = os.getenv("CHAT_ID")
    rq.get(url + "/sendMessage", params={"chat_id": chat_id, "text": message})

def build_message(forecast):
    message_parts = [f"Morning Artur,\n\nToday's forecast is:\n"]
    for weather in forecast:
        time_dt = dt.strptime(weather["dt_txt"], "%Y-%m-%d %H:%M:%S")
        message_parts.append(f"\nTime: {time_dt.strftime('%H:%M')}\n"
                             f"Weather: {weather['weather'][0]['description']}\n"
                             f"Temperature: {int(round(weather['main']['temp'], 0))}°C\n"
                             f"Feels like: {int(round(weather['main']['feels_like'], 0))}°C\n"
                             f"Wind speed: {int(round(weather['wind']['speed'], 0)) * 3.6} Km/h\n") # Convert from m/sec to km/h
    if any(x in w["weather"][0]["description"] for w in forecast for x in ["rain", "thunderstorm", "drizzle"]):
        message_parts.append("\nDon't forget to bring your umbrella" + u"\U00002614")
    return ''.join(message_parts)
    
# Main function
def main():
    for _ in range(10):
        try:
            forecast = get_weather_forecast().json()["list"][0:7]
            break
        except KeyError:
            continue
    message = build_message(forecast)
    send_message(message)
        
if __name__ == "__main__":
    main()