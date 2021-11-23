from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# api.weather.com api key
API_KEY = os.environ.get("API_KEY")


@app.route('/')
def index():
    # default values for Location Services data
    loc_type = 'postcode'
    search_term = '87048'
    err = ''

    # get Location search form input
    if request.method == 'POST':
        search_term = request.form['search']
        loc_type = request.form['loc_type']

    # GET Location Services dataset
    search_data = get_locale(loc_type, search_term)

    # extract lat/long from first record from full Location Services dataset
    geocode = get_geocode(search_data)
    lat = geocode['lat']
    long = geocode['long']

    # GET Currents on Demand dataset for location, using lat/long
    weather_data = get_weather(lat, long)

    # render output to template
    return render_template(
        'index.html',
        data=weather_data,
        locale=search_data,
        err=err
    )


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


def get_geocode(data):
    # extract latitude and longitude from full location dataset
    lat = data["location"]["latitude"][0]
    long = data["location"]["longitude"][0]
    geocode = {
        'lat': lat,
        'long': long,
    }
    return geocode


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')
