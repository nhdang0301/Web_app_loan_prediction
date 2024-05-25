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
from sqlalchemy import func


# Loan Prediction App
app = Flask(__name__)
app.secret_key = "NGUYENHAIDANG"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://loan_prediction_app_user:lrBo8SP9GfQUVJjnl9taM8XQFbKISXqI@dpg-cooruf779t8c73fbptbg-a.oregon-postgres.render.com/loan_prediction_app'
app.config['SQLALCHEMY_BINDS'] = {
    'db2': 'postgresql://loan_prediction_app_2_user:eXmGXUedIIQ43ezT9LaTD3UmuXwBI5wV@dpg-cp8nnmv109ks739trfag-a.oregon-postgres.render.com/loan_prediction_app_2'
}
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


class loan_data_preprocessed(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'loan_data_preprocessed'
    id = db.Column(db.Integer, primary_key=True)
    loan_amnt = db.Column(db.Float, nullable=False)
    term = db.Column(db.String(10), nullable=False)
    int_rate = db.Column(db.Float, nullable=False)
    installment = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    sub_grade = db.Column(db.String(3), nullable=False)
    emp_length = db.Column(db.String(20), nullable=False)
    home_ownership = db.Column(db.String(100), nullable=False)
    annual_inc = db.Column(db.Float, nullable=False)
    verification_status = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    dti = db.Column(db.Float, nullable=False)
    application_type = db.Column(db.String(100), nullable=False)
    addr_state = db.Column(db.String(100), nullable=False)
    loan_status = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"loan_data_preprocessed('{self.loan_amnt}', '{self.term}', '{self.int_rate}', '{self.installment}', '{self.grade}', '{self.sub_grade}', '{self.emp_length}', '{self.home_ownership}', '{self.annual_inc}', '{self.verification_status}', '{self.purpose}', '{self.dti}', '{self.application_type}', '{self.addr_state}', '{self.loan_status}')"


class expectedloss(db.Model):
    __tablename__ = 'expectedloss'
    id = db.Column(db.Integer, primary_key=True)
    funded_amnt = db.Column(db.Float, nullable=False)
    pd = db.Column(db.Float, nullable=False)
    lgd = db.Column(db.Float, nullable=False)
    ead = db.Column(db.Float, nullable=False)
    el = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"ExpectedLoss('{self.funded_amnt}', '{self.pd}', '{self.lgd}', '{self.ead}', '{self.el}')"


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
            return redirect(url_for('dashboard_page'))
        # If no user matches or password is incorrect
        flash('Login Unsuccessful. Please check email and password', 'danger')

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    # Xóa session user
    session.pop('user', None)
    # Chuyển hướng người dùng về trang đăng nhập (hoặc trang chủ, tùy bạn)
    return redirect(url_for('login'))


@app.route('/users')
def show_users():
    users = expectedloss.query.all()
    return render_template('users.html', users=users)


@login_required
@app.route('/dashboard')
def dashboard_page():
    if 'user' not in session:
        flash("Please log in to access this page", "info")
        return redirect(url_for('login'))
    # Tổng số tiền được tài trợ
    total_funded_amnt = db.session.query(
        func.sum(expectedloss.funded_amnt)).scalar() or 0
    formatted_total_funded_amnt = format(int(total_funded_amnt), ',')
    # Tổng số khách hàng
    total_customers = db.session.query(func.count(expectedloss.id)).scalar()
    formatted_total_customers = format(
        total_customers, ',')
    # AVG PD
    avg_pd = db.session.query(func.avg(expectedloss.pd)).scalar() or 0
    formatted_avg_pd = format(avg_pd * 100, '.2f') + '%'
    # Tổng tổn thất dự kiến
    total_expectedloss = db.session.query(
        func.sum(expectedloss.el)).scalar() or 0
    formatted_total_expectedloss = format(int(total_expectedloss), ',')
    # In ra bảng ghi
    expectedlosses = expectedloss.query.limit(10).all()

    return render_template("dashboard.html", username=session['user'], expectedlosses=expectedlosses, total_funded_amnt=formatted_total_funded_amnt, total_customers=formatted_total_customers, avg_pd=formatted_avg_pd, total_expectedloss=formatted_total_expectedloss)


@app.route('/total-data')
def total_data():
    total_funded = db.session.query(db.func.sum(
        expectedloss.funded_amnt)).scalar() or 0
    total_expected_loss = db.session.query(
        db.func.sum(expectedloss.el)).scalar() or 0
    return jsonify({
        # Nhãn cho mỗi cột
        "labels": ["Total Funded Amount", "Total Expected Loss"],
        "totals": [total_funded, total_expected_loss]
    })


@app.route('/scatter-data')
def scatter_data():
    results = expectedloss.query.all()  # Fetch your data here
    data = [{
        "ProbabilityOfDefault": r.pd,
        "ExpectedLoss": r.el
    } for r in results]
    return jsonify(data)


@app.route('/search')
def search_customer():
    customer_id = request.args.get('customer_id')
    customer = expectedloss.query.get(customer_id)
    if customer:
        return jsonify({
            'success': True,
            'funded_amnt': customer.funded_amnt,
            'pd': customer.pd,
            'lgd': customer.lgd,
            'ead': customer.ead,
            'el': customer.el
        })
    else:
        return jsonify({'success': False})


@app.route('/term-data')
def term_data():
    term_counts = db.session.query(loan_data_preprocessed.term, db.func.count(
        loan_data_preprocessed.term)).group_by(loan_data_preprocessed.term).all()
    terms = [term[0] for term in term_counts]
    counts = [count[1] for count in term_counts]
    return jsonify({
        "labels": terms,
        "values": counts
    })


if __name__ == '__main__':
    app.run(debug=True)
