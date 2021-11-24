from flask import Flask, render_template, request, Response
import requests
import os
import json

app = Flask(__name__)

# api.weather.com api key
API_KEY = os.environ.get("API_KEY")


@app.route('/', methods=['GET', 'POST'])
def index():
    # default values for Location Services data
    loc_type = 'postcode'
    search_term = '87048'

    # get Location search form input
    if request.method == 'POST':
        if request.form['search'] and request.form['loc_type']:
            search_term = request.form['search']
            # limit search type to 'postcode' for now...
            # loc_type = request.form['loc_type']

    # GET Location Services dataset
    search_data = get_locale(loc_type, search_term)

    # extract lat/long from first record from full Location Services dataset
    geocode = get_geocode(search_data)
    lat = geocode['lat']
    long = geocode['long']

    # GET Currents on Demand dataset for location, using lat/long
    weather_data = get_weather(lat, long)

    # GET Power Disruption Index dataset for location, using lat/long
    power_disruption = get_power_disruption(lat, long)

    # render output to template
    return render_template(
        'index.html',
        data=weather_data,
        locale=search_data,
        power=power_disruption
    )


# Location Services (Search)
#
# - https://weather.com/swagger-docs/ui/sun/v3/sunV3LocationSearch.json
#
# The Location Search API provides the ability to pass location search input parameters from users, applications or
# other systems and retrieve a set of locations from the TWC Location Parent database.
#
# Base URL: api.weather.com/v3/
# Endpoint: /search
def get_locale(location_type, query):
    headers = {'Accept': 'application/json'}
    url = f'https://api.weather.com/v3/location/search?query={query}&locationType={location_type}&language=en' \
          f'-US&format=json&apiKey={API_KEY}'
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


# Currents on Demand
#
# - https://weather.com/swagger-docs/ui/sun/v3/sunV3CurrentsOnDemand.json
#
# The API provides information on temperature, precipitation, wind, barometric pressure,
# visibility, ultraviolet (UV) radiation, and other related weather observations elements
# as well as date/time, weather icon codes and phrases. The COD is gridded across the globe
# at a 4KM geocode resolution.
#
# Base URL: api.weather.com/v3/
# Endpoint: /wx/observations/current
def get_weather(lat, long):
    headers = {'Accept': 'application/json'}
    url = f'https://api.weather.com/v3/wx/observations/current?geocode={lat}%2C{long}&units=e&language=en-US&format' \
          f'=json&apiKey={API_KEY}'
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


# Severe Weather Power Disruption Index 15 Day
#
# - https://weather.com/swagger-docs/ui/sun/v2/SUNv2SevereWeatherPowerDisruptionIndex.json
#
# The Power Disruption index provides indices indicating the potential for power
# disruptions due to weather.
#
# Base URL: api.weather.com/v2
# Endpoint: /indices/powerDisruption/daypart/15day
def get_power_disruption(lat, long):
    headers = {'Accept': 'application/json'}
    url = f'https://api.weather.com/v2/indices/powerDisruption/daypart/15day?geocode={lat}%2C{long}&format=json' \
          f'&language=en-US&apiKey={API_KEY}'
    r = requests.get(url, headers=headers)
    data = r.json()
    return data


# Get Geocode
#
# Helper function to extract latitude and longitude data from the full Location Services dataset.
def get_geocode(data):
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
