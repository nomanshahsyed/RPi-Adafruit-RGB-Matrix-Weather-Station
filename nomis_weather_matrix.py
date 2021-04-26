import schedule
import time
import datetime
import json
import requests
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from board import *
import busio
import adafruit_mcp9808  #i2c Temp sensor
import RPi.GPIO as GPIO
import random

GPIO.setwarnings(False)
GPIO.setup(25, GPIO.IN)  # Used for PIR sensor
#Sensitivity of PIR set for 1 minute. After each detection the display will be on for about 1 minute.

location = '632453'  # Location Code for Vantaa
appid = ''  # Get APP ID from https://openweathermap.org/api

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2  # 2 32x32 Matrices
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
matrix = RGBMatrix(options=options)

font_numbers = graphics.Font()
font_numbers.LoadFont("fonts/6x9.bdf")

font_text = graphics.Font()
font_text.LoadFont("fonts/5x7.bdf")

t = adafruit_mcp9808.MCP9808(busio.I2C(SCL, SDA))
data = {}
pos = 0  # For scrolling the text

seconds_tick = False
textcolor = graphics.Color(200, 200, 200)


def display_data():

    matrix.Clear()

    global data
    global pos
    global seconds_tick
    global textcolor

    i = GPIO.input(25)

    main = data['main']
    temp = main['temp']
    temp = temp - 273.15
    temp = int(round(temp))

    humidity = main['humidity']
    humidity = int(round(humidity))

    real_feel = main['feels_like']
    real_feel = real_feel - 273.15
    real_feel = int(round(real_feel))

    temp_min = main['temp_min']
    temp_min = temp_min - 273.15
    temp_min = int(round(temp_min))

    temp_max = main['temp_max']
    temp_max = temp_max - 273.15
    temp_max = int(round(temp_max))

    wind = data['wind']['speed']

    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    timezone = data['timezone']

    sunrise = datetime.datetime.fromtimestamp(sunrise).strftime('%H:%M')
    sunset = datetime.datetime.fromtimestamp(sunset).strftime('%H:%M')

    weather = data['weather'][0]['main']
    weather = weather + " Min:" + str(temp_min) + " Max:" + str(
        temp_max) + " Wind:" + str(wind) + " Sunrise:" + str(
            sunrise) + " Sunset:" + str(sunset)
    if (pos - 64 + len(weather) * 6 + 6 < 0):
        # Width of matrix is 64 LEDs. Width of single char is 6 LEDs. The Scrolling happenns till last character of weather string.
        pos = 0
    else:
        pos = pos - 6

    # Sets Temperature Color
    if temp <= 0:
        temp_color = graphics.Color(200, 200, 200)
    elif temp > 0 and temp <= 10:
        temp_color = graphics.Color(200, 0, 200)
    elif temp > 10 and temp <= 25:
        temp_color = graphics.Color(200, 200, 0)
    elif temp > 25:
        temp_color = graphics.Color(200, 0, 0)

    r = random.randrange(100, 200)
    g = random.randrange(100, 200)
    b = random.randrange(100, 200)

    textcolor = graphics.Color(r, g, b)

    if seconds_tick:
        seconds_tick = False
        time = datetime.datetime.now().strftime("%H:%M")
    else:
        seconds_tick = True
        time = datetime.datetime.now().strftime("%H %M")

    date = datetime.datetime.now().strftime("%d-%m")

    character_position = 1

    if i == 1:  # PIR detects a person

        graphics.DrawText(matrix, font_numbers, 1, 7,
                          graphics.Color(200, 0, 0), time)
        graphics.DrawText(matrix, font_numbers, 33, 7,
                          graphics.Color(0, 200, 0), date)
        if temp >= 0 and temp < 10:
            text = "Temp"
        else:
            text = "T°C"

        graphics.DrawText(matrix, font_numbers, character_position, 14,
                          textcolor, text)

        character_position = character_position + len(text) * 6

        graphics.DrawText(matrix, font_numbers, character_position, 15,
                          temp_color, str(temp))

        character_position = character_position + len(str(temp)) * 6

        if real_feel >= 0 and real_feel < 10:
            text = "Feel"
        else:
            text = "RF°"

        graphics.DrawText(matrix, font_numbers, character_position, 15,
                          textcolor, text)

        character_position = character_position + len(text) * 6

        graphics.DrawText(matrix, font_numbers, character_position, 15,
                          temp_color, str(real_feel))

        character_position = 1

        graphics.DrawText(matrix, font_numbers, character_position, 23,
                          textcolor, "In")

        character_position = character_position + len("In°") * 6

        graphics.DrawText(matrix, font_numbers, character_position, 23,
                          graphics.Color(200, 0, 200), str(int(t.temperature)))

        character_position = character_position + len(str(int(
            t.temperature))) * 6

        graphics.DrawText(matrix, font_numbers, character_position, 23,
                          graphics.Color(200, 200, 200), str(humidity))

        character_position = character_position + len(str(humidity)) * 6 + 6

        graphics.DrawText(matrix, font_numbers, character_position, 23,
                          textcolor, "%H")

        graphics.DrawText(matrix, font_numbers, pos, 31, textcolor,
                          str(weather))


def fetch_weather_data():
    global data
    try:
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?id=' + location +
            '&mode=json&cnt=10&appid=' + appid)
        data = json.loads(response.text)

    except requests.exceptions.RequestException as e:
        print('Err.')


fetch_weather_data()
display_data()
schedule.every(5).minutes.do(fetch_weather_data)
schedule.every(1).seconds.do(display_data)

while True:
    schedule.run_pending()