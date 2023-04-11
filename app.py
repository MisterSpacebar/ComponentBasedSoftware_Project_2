from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import NumberRange
import main_functions
import historical
import requests
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(16).hex()

def get_autocomplete_items():
    data = main_functions.read_from_file("item_data.json")
    return data["data"]

@app.route('/')
def index():
    return render_template('index.html')

# returns data for autocomplete
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    items = get_autocomplete_items()
    query = request.form['query']
    results = [item for item in items if query.lower() in item.lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run()