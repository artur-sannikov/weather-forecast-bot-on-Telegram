import requests as rq
from datetime import datetime as dt
from dotenv import load_dotenv
import os
import logging

# Create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up logging handlers
file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.WARNING)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Set logging format and set format for handlers
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(log_format)
console_handler.setFormatter(log_format)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Load environment variables
load_dotenv()

def get_weather_forecast():
    """
    Get weather forecast data for a city from OpenWeatherMap API.

    Returns
    -------
    requests.Response
        The API response containing the weather forecast data.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/forecast" # 5 day weather forecast
    city = os.getenv("OPENWEATHER_CITY")
    payload = {"q": city, "appid": api_key, "units": "metric"}

    return rq.get(base_url, params=payload)

def send_message(message):
    """
    Send a message to a specified Telegram chat.

    Parameters
    ----------
    message : str
        The message text to be sent.
    """
    bot_key = os.getenv("BOT_API_KEY")
    url =  "https://api.telegram.org/bot" + bot_key
    chat_id = os.getenv("CHAT_ID")
    rq.get(url + "/sendMessage", params={"chat_id": chat_id, "text": message})

def build_message(forecast):
    """
    Build a formatted weather forecast message.

    Parameters
    ----------
    forecast : list
        A list of weather data dictionaries for the current day.

    Returns
    -------
    str
        A formatted message containing the weather forecast.
    """
    # Read user's name
    username = os.getenv("USERNAME")

    # Build the message
    message_parts = [f"Morning {username},\n\nToday's forecast is:\n"]
    for weather in forecast:
        time_dt = dt.strptime(weather["dt_txt"], "%Y-%m-%d %H:%M:%S")
        message_parts.append(f"\nTime: {time_dt.strftime('%H:%M')}\n"
                             f"Weather: {weather['weather'][0]['description']}\n"
                             f"Temperature: {int(round(weather['main']['temp'], 0))}°C\n"
                             f"Feels like: {int(round(weather['main']['feels_like'], 0))}°C\n"
                             f"Wind speed: {int(round(weather['wind']['speed'], 0)) * 3.6} Km/h\n") # Convert m/sec to km/h
    # Search for 'bad' weather and add a reminder to bring an umbrella if found                         
    if any(x in w["weather"][0]["description"] for w in forecast for x in ["rain", "thunderstorm", "drizzle"]):
        message_parts.append("\nDon't forget to bring your umbrella" + u"\U00002614")
    return ''.join(message_parts)
    
def main():
    """
    Retrieve weather forecast data and send it via Telegram.
    
    Attempts to fetch weather forecast data up to 10 times.
    If successful, sends a formatted message to the specified chat.
    """
    for attempt in range(10):
        try:
            forecast = get_weather_forecast().json()["list"][0:7]
            break
        except KeyError:
            logger.warning(f"Attempt {attempt + 1}: Failed to fetch weather forecast.")
            continue
        else:
            logger.error("Failed to fetch weather forecast after 10 attempts.")
            return
    message = build_message(forecast)
    send_message(message)
    logger.info("Weather forecast message sent successfully.")
        
if __name__ == "__main__":
    main()