from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# setup sql connection
conn = "postgres:postgres@localhost:5432/medicare_drg"
engine = create_engine(f'postgresql://{conn}')

@app.route("/")
def index():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_1.html")

@app.route("/temperature")
def temperature():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html")

@app.route("/humidity")
def humidity():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_2.html")

@app.route('/cloudiness')
def cloudiness():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_3.html")

@app.route("/wind")
def wind():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_4.html")

@app.route("/comparison")
def comparison():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_5.html")

@app.route("/data")
def data():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_6.html")

if __name__ == "__main__":
    app.run(debug=True)
