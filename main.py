
import pandas as pd
import random
import string

from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/generate-password")
def generate_password():
    """
    from 10 to 25 chars
    upper and lower case
    """

    return ''.join(random.choices(string.ascii_letters, k=random.randint(10, 25)))


@app.route("/calculate-average")
def calculate_average():
    """
    csv file with students
    1.calculate average high
    2.calculate average weight
    csv - use lib
    *pandas - use pandas for calculating
    """

    df = pd.read_csv('hw.csv')

    return f'Average height: {round(df[" Height(Inches)"].mean(), 2)} inches <br>' \
           f'Average weight: {round(df[" Weight(Pounds)"].mean(), 2)} pounds'


app.run(port=5001, debug=True)
