# Hello da fix

import os
import pandas as pd
import matplotlib as plt
from flask import Flask, render_template, redirect, url_for, request, flash
app = Flask(__name__)
app.secret_key = "NGUYENHAIDANG"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Giả sử đây là thông tin đăng nhập chính xác cho mục đích minh họa
    if email == "user@example.com" and password == "password123":
        flash('Đăng nhập thành công!')
        return redirect(url_for('dashboard'))

    else:
        flash('Email hoặc mật khẩu không chính xác. Vui lòng thử lại.')
        return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    # Reading the Excel file
    filepath = 'E:\Webapp\mywebapp\data\Raw_data.csv'
    df = pd.read_csv(filepath, nrows=50)

    # Converting the dataframe to a dictionary for easier processing in the template
    data = df.to_dict(orient='records')

    # Rendering the HTML template
    return render_template('dashboard.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
