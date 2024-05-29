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
    'pressureSensor': argv[1],
    'levelSensor': argv[2],
    'timer': argv[3],
    'thermometer': argv[4]
}

MIN_INTERVAL = int(config['TIMER']['MIN_INTERVAL'])
MAX_INTERVAL = int(config['TIMER']['MAX_INTERVAL'])
INTERVAL = randint(MIN_INTERVAL, MAX_INTERVAL)

MIN_START_TIME = int(config['TELEMETRY.TIMER']['MIN_START_TIME'])
MAX_START_TIME = int(config['TELEMETRY.TIMER']['MAX_START_TIME'])
MIN_DURATION = int(config['TELEMETRY.TIMER']['MIN_DURATION'])
MAX_DURATION = int(config['TELEMETRY.TIMER']['MAX_DURATION'])

MIN_TEMPERATURE = int(config['TELEMETRY.TEMPERATURE']['MIN_TEMPERATURE'])
MAX_TEMPERATURE = int(config['TELEMETRY.TEMPERATURE']['MAX_TEMPERATURE'])

MIN_PRESSURE_VALUE = int(config['TELEMETRY.PRESSURE']['MIN_PRESSURE_VALUE'])
MAX_PRESSURE_VALUE = int(config['TELEMETRY.PRESSURE']['MAX_PRESSURE_VALUE'])

MIN_LEVEL = int(config['TELEMETRY.LEVEL']['MIN_LEVEL'])
MAX_LEVEL = int(config['TELEMETRY.LEVEL']['MAX_LEVEL'])

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
    hour_falling = randint(MIN_START_TIME, MAX_START_TIME)
    if (hour_falling > 23):
        day -= 1
        hour_falling %= 24

    time_falling = (datetime.now() - timedelta(days=day)).replace(hour=hour_falling)

    duration = randint(MIN_DURATION, MAX_DURATION)

    post(TOKENS['timer'], {
        'start_time': time_falling.isoformat(),
        'duration': duration,
    })

    temperature = randint(MIN_TEMPERATURE, MAX_TEMPERATURE)

    post(TOKENS['thermometer'], {
        'temperature': temperature
    })

    pressure = randint(MIN_PRESSURE_VALUE, MAX_PRESSURE_VALUE)

    post(TOKENS['pressureSensor'], {
        'pressureSensor': pressure
    })

    level = randint(MIN_LEVEL, MAX_LEVEL)

    post(TOKENS['levelSensor'], {
        'levelSensor': level
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