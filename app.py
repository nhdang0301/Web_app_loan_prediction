import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import matplotlib as plt
from flask import Flask, render_template, redirect, url_for, request, flash
from flask import session, jsonify


# Loan Prediction App
app = Flask(__name__)
app.secret_key = "NGUYENHAIDANG"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zbhyszrxtobmsu:2c02c1585c00f8bcbd33c90797f0234643ce135688a1b296372c0087badcf788@ec2-52-6-117-96.compute-1.amazonaws.com:5432/deohkrnac3mloe'
db = SQLAlchemy(app)


# SQLALCHEMY
class all_users(db.Model):
    __tablename__ = 'all_users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        user = all_users(username=request.form['username'],
                         email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = all_users.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            # User is authenticated, proceed to log them in
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    # Reading the Excel file
    filepath = 'E:\Web_app_loan_prediction\data\Raw_data.csv'
    df = pd.read_csv(filepath, nrows=50)

    # Converting the dataframe to a dictionary for easier processing in the template
    data = df.to_dict(orient='records')

    # Rendering the HTML template
    return render_template('dashboard.html', data=data)


@app.route('/users')
def show_users():
    users = all_users.query.all()
    return render_template('users.html', users=users)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Xóa trạng thái đăng nhập khỏi session
    return redirect(url_for('login'))


@app.route('/predict')
def predict():
    return render_template('predict.html')
# API để cung cấp dữ liệu cho biểu đồ


@app.route('/data')
def data():
    # Lấy dữ liệu từ cơ sở dữ liệu hoặc nơi khác
    data = [10, 20, 30, 40, 50]
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
