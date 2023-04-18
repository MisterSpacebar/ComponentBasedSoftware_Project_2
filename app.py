from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import NumberRange
import main_functions
import historical
import requests
import json
import os

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.urandom(16).hex()


def get_autocomplete_items():
    data = main_functions.read_from_file("item_data.json")
    autocomplete_items = []
    for item in data["data"]:
        autocomplete_items.append(item["name"])
    return autocomplete_items


def get_id_by_name(name):
    data = main_functions.read_from_file("item_data.json")
    for obj in data['data']:
        if obj["name"] == name:
            return obj["id"]
    return None  # name not found in data


@app.route('/')
def index():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        return redirect(url_for('results'))
    return render_template('index.html')


# returns data for autocomplete
@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    items = get_autocomplete_items()
    # query = request.form['query']
    # results = [item for item in items if query.lower() in item.lower()]
    # return jsonify(results)
    return items


@app.route('/search', methods=['POST'])
def search():
    name = session.get('name')
    query = request.form.get('item_name')
    print(query)
    # Match item to item_id
    item_id = get_id_by_name(query)
    print(item_id)
    session['item_id'] = item_id
    item_data = historical.get_item_data(item_id)
    return render_template('results.html', name=name, item_data=item_data)


@app.route('/chart')
def chart():
    item_id = session['item_id']
    data = historical.amalgamated_historical_data(item_id)

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
