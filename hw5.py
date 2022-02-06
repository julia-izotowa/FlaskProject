
import csv
import json
import requests
import main

from json2html import *

from faker import Faker

from flask import Flask, request, jsonify, Response


from webargs import validate, fields
from webargs.flaskparser import use_kwargs


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, Mykhailo!</p>"

@app.route('/bitcoin-rate')
def get_bitcoin_value():

    currency_name = request.args.get('currency', 'USD')
    if currency_name.isdigit():
        return Response("ERROR: Wrong symbols in currency name")

    currency_value = bitcoin_exchange_value(currency_name)
    currency_sign = get_currency_sign(currency_name)

    return ''.join(f'Currency exchange rate BTC to {currency_name}: {currency_value}  {currency_sign}')


def bitcoin_exchange_value(currency_name):

    currency_value = requests.get(f"https://bitpay.com/api/rates/{currency_name}")
    result = currency_value.json()

    return result["rate"]


def get_currency_sign(currency_name):

    request_data = requests.get("https://bitpay.com/currencies")
    result = request_data.json()["data"]
    currency_data = list(filter(lambda x: x['code'] == currency_name, result))

    return currency_data[0]['symbol']


@app.route('/generate-students')
@use_kwargs(
    {
        "number": fields.Int(
            missing=20,
            validate=[validate.Range(min=1, max=1000)]
        ),
    },
    location="query")
def generate_students(number):

    fake = Faker("uk_UA")
    list_of_students = []
    for i in range(number):
        list_of_students.append({"first_name": fake.first_name().replace("ʼ", "'"),
                                 "last_name": fake.last_name().replace("ʼ", "'"),
                                 "email": fake.email(),
                                 "password": main.generate_password(),
                                 "birthday": str(fake.date_of_birth(minimum_age=17, maximum_age=25))})

    with open('students_demo.csv', "w", newline="") as file:
        columns = list_of_students[0].keys()
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(list_of_students)

    return json2html.convert(json.dumps(list_of_students, ensure_ascii=False))


app.run(port=4567, debug=True)
