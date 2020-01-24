#!/usr/bin/env python3

import speech_recognition as sr
import time
import requests

cont = True

def stop_recognition(result) :
    global cont
    print("Stopping")
    cont = False

def show_time(result) :
    print(time.strftime("%c"))

def show_weather(result) :
    local_weather_api_str = "https://api.weather.gov/gridpoints/BOX/68,78/forecast"

    r = requests.get(local_weather_api_str)
    periods = r.json()['properties']['periods']

    print("{prd_1}: {cast_1}\n\n{prd_2}: {cast_2}".format(prd_1=periods[0]['name'], cast_1=periods[0]['detailedForecast'], prd_2=periods[1]['name'], cast_2=periods[1]['detailedForecast']))


action_words = {
    "cancel"    : stop_recognition,
    "off"       : stop_recognition,
    "stop"      : stop_recognition,

    "time"      : show_time,

    "weather"   : show_weather,
    "whether"   : show_weather      # Because sphinx isnt perfect at all
    }

def run_recognition() :
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening")
        audio = recog.listen(source)

    try:
        result = recog.recognize_sphinx(audio)
        print("Sphinx heard " + result)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print(e)

    for word in result.split(" ") :
        if word in action_words.keys() :
            action_words[word](result)

def main() :
    while(cont) :
        run_recognition()

if __name__ == '__main__':
    main()
