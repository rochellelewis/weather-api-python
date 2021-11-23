from flask import Flask, render_template, request
import os

app = Flask(__name__)

# api.weather.com api key
API_KEY = os.environ.get("API_KEY")


@app.route('/')
def index():
    return render_template('index.html')
