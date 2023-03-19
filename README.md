# Telegram Weather Forecast Bot

Telegram Weather Forecast Bot is a Python script that fetches weather forecast data from OpenWeatherMap and sends it to the user via a Telegram bot. The script provides a detailed forecast for the current day, including temperature, wind speed, and weather conditions. It also reminds the user to bring an umbrella if the forecast indicates rain, thunderstorms, or drizzles.

## Requirements

This script requires the following Python libraries to be installed:

* `requests`
* `python-dotenv`

You can install these libraries in a conda environment or any Python environment using the following command:

```bash
conda install -c anaconda requests python-dotenv
```

Or with pip:

```bash
pip install requests python-dotenv
```

## Installation and Usage

### 1. Set up the OpenWeatherMap API

To use this script, you first need to obtain an API key from OpenWeatherMap. You can get one by creating an account and following the instructions here: [How to start](https://openweathermap.org/appid).

### 2. Set up the Telegram Bot

Next, you need to create a Telegram bot and obtain its API key. Follow the instructions in the [Telegram Bots documentation](https://core.telegram.org/bots) to create a bot and get its API key.

### 3. Find your Telegram Chat ID

You'll also need your Telegram Chat ID to receive messages from the bot. This [Alphr article](https://www.alphr.com/find-chat-id-telegram/) explains how to find your Chat ID.

### 4. Create the .env file

Create a file named ".env" in the same directory as the script. Set the following environment variables in the file:

```bash
OPENWEATHER_API_KEY=your_openweathermap_api_key
OPENWEATHER_CITY=your_city_name
BOT_API_KEY=your_telegram_bot_api_key
CHAT_ID=your_telegram_chat_id
USERNAME=your_name
```
Replace the placeholders with your actual API keys, chat ID, city name, and your name.
### 5. Run the script

With the .env file set up, you can now run the script:
```bash
python3 weather_bot.py
```

If everything is set up correctly, you will receive the weather forecast for your specified city in the Telegram chat.

## Automating the Script on Linux

The best way to receive a daily weather forecast is to automate the script on, for example, your server.

To automate this script on Linux, follow these step-by-step instructions to create a cron job that runs the script at your preferred time.

### Step 1: Make the Script Executable

1.  Open a terminal.
2.  Navigate to the folder where the `weather_bot.py` script is located. For example:
```bash
cd /home/YourUsername/Documents
```
3. Make the script executable by running the following command:
```bash
chmod +x weather_bot.py
```
### Step 2: Create a Cron Job

1.  Open a terminal, if not already open.
2.  Type `crontab -e` and press `Enter` to open your user's cron table for editing.
3.  Choose your preferred editor, if prompted (e.g., nano, vim, or emacs).
4.  Add a new line at the end of the file with the following format:
```
* * * * * conda activate <your_env>; python3 /path/to/script/weather_bot.py; conda deactivate
```
Replace the <your_env> placeholder with the name of environment where you installed the required libraries.

This guide assumes that you are using a conda environment, hence the environment is activated with the `conda` command.

The five asterisks represent minutes (0-59), hours (0-23), days of the month (1-31), months (1-12), and days of the week (0-7, where both 0 and 7 represent Sunday). Adjust these values to set the desired schedule. For example, to run the script every day at 7 AM, use:
```
0 7 * * * conda activate <your_env>; python3 /path/to/script/weather_bot.py; conda deactivate
```
5. Save the file and exit the editor. The cron job will be installed automatically.

The script will now run automatically according to the schedule you set.

## License
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
