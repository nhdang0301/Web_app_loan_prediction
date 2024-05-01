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
from datetime import timedelta

# Loan Prediction App
app = Flask(__name__)
app.secret_key = "NGUYENHAIDANG"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://loan_prediction_app_user:lrBo8SP9GfQUVJjnl9taM8XQFbKISXqI@dpg-cooruf779t8c73fbptbg-a.oregon-postgres.render.com/loan_prediction_app'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    minutes=20)  # Set session lifetime to 1 minute

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
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # Thêm cột mới

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


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Lấy thông tin từ form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Kiểm tra xem email đã tồn tại trong cơ sở dữ liệu chưa
        existing_user = all_users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('home'))

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)

        # Tạo một bản ghi mới trong cơ sở dữ liệu
        new_user = all_users(username=username, email=email,
                             password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Fetch user from the database
        user = all_users.query.filter_by(email=email).first()

        # Check if the user exists and verify the password
        if user and check_password_hash(user.password, password):
            # Authentication successful
            # Initialize session
            session['user'] = user.username
            # flash('You have successfully logged in.', 'success')
            return redirect(url_for('predict_page'))
            # return render_template("predict.html", username=user.username)

        # If no user matches or password is incorrect
        flash('Login Unsuccessful. Please check email and password', 'danger')

    return redirect(url_for('home'))


@app.route('/logout', methods=['POST'])
@login_required
def logout_user():
    logout()
    return redirect(url_for('home'))


# @app.route('/dashboard')
# @login_required
# def dashboard():
#     # Reading the Excel file
#     filepath = 'E:\Web_app_loan_prediction\data\Raw_data.csv'
#     df = pd.read_csv(filepath, nrows=50)

#     # Converting the dataframe to a dictionary for easier processing in the template
#     data = df.to_dict(orient='records')

#     # Rendering the HTML template
#     return render_template('dashboard.html', data=data, user=current_user)


@app.route('/users')
def show_users():
    users = all_users.query.all()
    return render_template('users.html', users=users)


# @app.route('/predict')
# @login_required
# def predict():
#     return render_template('predict.html')
# # API để cung cấp dữ liệu cho biểu đồ

@login_required
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
