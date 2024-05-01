import psycopg2
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import matplotlib as plt
from flask import Flask, render_template, redirect, url_for, request, flash
from flask import session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import logout_user as logout
import gspread
from google.oauth2.service_account import Credentials
import bcrypt
import base64
# Loan Prediction App
app = Flask(__name__)
app.secret_key = "NGUYENHAIDANG1"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://loan_prediction_app_user:lrBo8SP9GfQUVJjnl9taM8XQFbKISXqI@dpg-cooruf779t8c73fbptbg-a.oregon-postgres.render.com/loan_prediction_app'
db = SQLAlchemy(app)

# Query to select a table from the database

with app.app_context():
    class customers(db.Model):
        __tablename__ = 'customers'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))

with app.app_context():
    all_customers = customers.query.all()

# Print all rows
for customer in all_customers:
    print(customer.id, customer.name)
