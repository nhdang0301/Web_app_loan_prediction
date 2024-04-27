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
app.secret_key = "NGUYENHAIDANG"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zbhyszrxtobmsu:2c02c1585c00f8bcbd33c90797f0234643ce135688a1b296372c0087badcf788@ec2-52-6-117-96.compute-1.amazonaws.com:5432/deohkrnac3mloe'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# SQLALCHEMY
# Setup
gc = gspread.service_account(filename="creds.json")
# Replace "test" with the actual name of your sheet
sh = gc.open("test").sheet1


class all_users(UserMixin, db.Model):
    __tablename__ = 'all_users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @property
    def is_active(self):
        return True

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id):
    return all_users.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/signup', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         hashed_password = generate_password_hash(request.form['password'])
#         user = all_users(username=request.form['username'],
#                          email=request.form['email'], password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created!', 'success')
#         return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Tạo timestamp hiện tại
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if email already exists in the sheet
        records = sh.get_all_records()
        for record in records:
            if record['email'] == email:
                flash('Email already registered. Please use a different email.', 'error')
                return redirect(url_for('home'))

        # Hash the password and encode it to Base64
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_b64 = base64.b64encode(hashed_password).decode('utf-8')

        # Append new user data to the sheet
        sh.append_row([username, email, hashed_password_b64, timestamp])
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = all_users.query.filter_by(email=request.form['email']).first()
#         if user and check_password_hash(user.password, request.form['password']):
#             # User is authenticated, proceed to log them in
#             login_user(user)
#             # flash('You have successfully logged in.', 'success')
#             return render_template("predict.html", username=user)
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch all records from the sheet
        records = sh.get_all_records()

        # Check if the user exists and verify the password
        for record in records:
            if record['email'] == email:
                # Decode the hashed password from Base64
                stored_password_b64 = record['password']
                stored_password = base64.b64decode(stored_password_b64)

                # Check the provided password against the stored hash
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Authentication successful
                    # Simple session example
                    session['user'] = record['username']
                    # flash('You have successfully logged in.', 'success')
                    return redirect(url_for('predict_page'))
                    # return render_template("predict.html", username=record['username'])

        # If no record matches or password is incorrect
        flash('Login Unsuccessful. Please check email and password', 'danger')

    return redirect(url_for('home'))


@app.route('/logout', methods=['POST'])
@login_required
def logout_user():
    logout()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    # Reading the Excel file
    filepath = 'E:\Web_app_loan_prediction\data\Raw_data.csv'
    df = pd.read_csv(filepath, nrows=50)

    # Converting the dataframe to a dictionary for easier processing in the template
    data = df.to_dict(orient='records')

    # Rendering the HTML template
    return render_template('dashboard.html', data=data, user=current_user)


@app.route('/users')
def show_users():
    users = all_users.query.all()
    return render_template('users.html', users=users)


# @app.route('/predict')
# @login_required
# def predict():
#     return render_template('predict.html')
# # API để cung cấp dữ liệu cho biểu đồ


@app.route('/predict')
def predict_page():
    if 'user' not in session:
        flash("Please log in to access this page", "info")
        return redirect(url_for('login'))
    return render_template("predict.html", username=session['user'])


@app.route('/data')
def data():
    # # Lấy dữ liệu từ cơ sở dữ liệu hoặc nơi khác
    # data = np.random.rand(5).tolist()
    # return jsonify(data)
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=50,
                          freq='D').strftime("%Y-%m-%d").tolist()
    prices = np.random.normal(100, 15, size=20).cumsum().tolist()
    return jsonify({'dates': dates, 'prices': prices})


if __name__ == '__main__':
    app.run(debug=True)
