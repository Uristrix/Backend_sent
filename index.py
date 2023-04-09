from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from table import *
from create_xlsx import *

app = Flask(__name__)
load_dotenv()

@app.route('/')
def home():
    return 'Home Page Route'


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/contact')
def contact():
    return 'Contact Page Route'
