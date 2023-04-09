from flask import Flask, request, send_from_directory, render_template
from flask_cors import CORS
from table import *
from create_xlsx import *

app = Flask(__name__)
load_dotenv()


@app.route('/')
def main():
    return render_template('index.html')
