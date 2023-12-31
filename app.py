import os
from flask import Flask, render_template, request, redirect, url_for
from venmo_bot import VenmoBot
from utils import process_transactions, float_to_currency, get_date_range_str

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/results", methods=["POST"])
def results():
    venmo_email = request.form['venmo-email']
    venmo_password = request.form['venmo-password']
    start_date = request.form['start-date']
    end_date = request.form['end-date']

    bot = VenmoBot()
    bot.login(venmo_email, venmo_password)
    transactions = bot.scrape_transactions(start_date, end_date)
    payments_to_me, total_income, tithing = process_transactions(transactions)

    date_range_str = get_date_range_str(start_date, end_date)
    return render_template(
        'results.html',
        venmo_email=venmo_email,
        date_range_str=date_range_str,
        payments_to_me=payments_to_me,
        total_income=float_to_currency(total_income),
        tithing=float_to_currency(tithing)
    )