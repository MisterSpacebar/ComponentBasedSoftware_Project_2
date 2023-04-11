from flask import Flask, request, render_template
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
