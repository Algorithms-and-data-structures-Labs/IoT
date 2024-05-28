from sys import argv
import os.path
from threading import Timer
from random import randint, uniform
from requests import post as rq_post
from datetime import datetime, timedelta
from configparser import ConfigParser

config = ConfigParser()
path = os.path.dirname(os.path.abspath(argv[0]))
config.read(path + r'\bot.ini')

TOKENS = {
    'noise': argv[1],
    'watch': argv[2],
    'humidity': argv[3],
    'thermometer': argv[4]
}

MIN_INTERVAL = int(config['TIMER']['MIN_INTERVAL'])
MAX_INTERVAL = int(config['TIMER']['MAX_INTERVAL'])
INTERVAL = randint(MIN_INTERVAL, MAX_INTERVAL)

MIN_HOUR_FALLING = int(config['TELEMETRY.TIMESLEEP']['MIN_HOUR_FALLING'])
MAX_HOUR_FALLING = int(config['TELEMETRY.TIMESLEEP']['MAX_HOUR_FALLING'])
MIN_SLEEP_DURATION = int(config['TELEMETRY.TIMESLEEP']['MIN_SLEEP_DURATION'])
MAX_SLEEP_DURATION = int(config['TELEMETRY.TIMESLEEP']['MAX_SLEEP_DURATION'])

MIN_ROOM_TEMPERATURE = int(config['TELEMETRY.TEMPERATURE']['MIN_ROOM_TEMPERATURE'])
MAX_ROOM_TEMPERATURE = int(config['TELEMETRY.TEMPERATURE']['MAX_ROOM_TEMPERATURE'])

MIN_NOISE_VALUE = int(config['TELEMETRY.NOISE']['MIN_NOISE_VALUE'])
MAX_NOISE_VALUE = int(config['TELEMETRY.NOISE']['MAX_NOISE_VALUE'])

MIN_HUMIDITY = int(config['TELEMETRY.HUMIDITY']['MIN_HUMIDITY'])
MAX_HUMIDITY = int(config['TELEMETRY.HUMIDITY']['MAX_HUMIDITY'])

MIN_AVERAGE_HEART_RATE = int(config['TELEMETRY.PHYSIOLOGICAL']['MIN_AVERAGE_HEART_RATE'])
MAX_AVERAGE_HEART_RATE = int(config['TELEMETRY.PHYSIOLOGICAL']['MAX_AVERAGE_HEART_RATE'])
MIN_AVERAGE_SLEEP_HEART_RATE = int(config['TELEMETRY.PHYSIOLOGICAL']['MIN_AVERAGE_SLEEP_HEART_RATE'])
MAX_AVERAGE_SLEEP_HEART_RATE = int(config['TELEMETRY.PHYSIOLOGICAL']['MAX_AVERAGE_SLEEP_HEART_RATE'])

URL = config["WEB"]["URL"]

TIMER = -1

def post(token, value):
    if (token == "-"):
        return
    
    try:
        respose = rq_post(URL, params={'token' : token}, json=value)
        print(f"POST /?token={token} {value.items()} responce code: {respose.status_code}")
    except Exception as e:
        print(e)
        print("\nAn error occurred while sending POST. The program has been stopped")
        global TIMER
        TIMER.cancel()
        exit()

def post_values():
    day = 1
    hour_falling = randint(MIN_HOUR_FALLING, MAX_HOUR_FALLING) 
    if (hour_falling > 23):
        day -= 1
        hour_falling %= 24

    time_falling = (datetime.now() - timedelta(days=day)).replace(hour=hour_falling)

    duration = randint(MIN_SLEEP_DURATION, MAX_SLEEP_DURATION)
    heart_rate = randint(MIN_AVERAGE_HEART_RATE, MAX_AVERAGE_HEART_RATE)
    sleep_heart_rate = randint(MIN_AVERAGE_SLEEP_HEART_RATE, MAX_AVERAGE_SLEEP_HEART_RATE)

    post(TOKENS['watch'], {
        'time_falling_sleep': time_falling.isoformat(),
        'duration': duration,
        'average_day_heart_rate': heart_rate,
        'average_sleep_heart_rate': sleep_heart_rate,
    })

    temperature = randint(MIN_ROOM_TEMPERATURE, MAX_ROOM_TEMPERATURE)

    post(TOKENS['thermometer'], {
        'temperature': temperature
    })

    noise = randint(MIN_NOISE_VALUE, MAX_NOISE_VALUE)

    post(TOKENS['noise'], {
        'noise': noise
    })

    humidity = randint(MIN_HUMIDITY, MAX_HUMIDITY)

    post(TOKENS['humidity'], {
        'humidity': humidity
    })

def repeater(interval, function):
    global TIMER
    TIMER = Timer(interval, repeater, [interval, function])
    TIMER.start()
    function()

def main():
    repeater(INTERVAL, post_values)

if __name__  == '__main__':
    main()