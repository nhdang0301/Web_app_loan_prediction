import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib as plt
from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "NGUYENHAIDANG"
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "E:\Web_app_loan_prediction\data\excel-database-404404-57bd0373f71a.json", scopes=scopes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
        user = User(username=request.form['username'],
                    email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            # User is authenticated, proceed to log them in
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('home')


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
    users = User.query.all()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
