from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# api.weather.com api key
API_KEY = os.environ.get("API_KEY")


@app.route('/')
def index():
    return render_template('index.html')


def get_locale(location_type, query):
    headers = {'Accept': 'application/json'}
    url = f'https://api.weather.com/v3/location/search?query={query}&locationType={location_type}&language=en' \
          f'-US&format=json&apiKey={API_KEY}'
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


def get_weather(lat, long):
    headers = {'Accept': 'application/json'}
    url = f'https://api.weather.com/v3/wx/observations/current?geocode={lat}%2C{long}&units=e&language=en-US&format' \
          f'=json&apiKey={API_KEY}'
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')
