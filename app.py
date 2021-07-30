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

@app.route("/utilization")
def utilization():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html")

@app.route("/percapita")
def percapita():
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index_2.html")

@app.route('/volumes', methods=['GET'])
def volumes():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient', con=engine)
    data_grouped = data_head.groupby(['Service_Line', 'Year']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['discharges']

    return d

@app.route('/volumes-2018', methods=['GET'])
def volumes_2018():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2018', con=engine)
    data_grouped = data_head.groupby(['Service_Line']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['discharges']

    return d

@app.route('/volumes-2017', methods=['GET'])
def volumes_2017():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2017', con=engine)
    data_grouped = data_head.groupby(['Service_Line']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['discharges']

    return d

@app.route('/volumes-2016', methods=['GET'])
def volumes_2016():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2016', con=engine)
    data_grouped = data_head.groupby(['Service_Line']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['discharges']

    return d

@app.route('/percapita-2018', methods=['GET'])
def percapita_2018():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2018', con=engine)
    data_grouped = data_head.groupby(['Service_Line']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped['per_capita'] = data_grouped['discharges']/52352000
    data_grouped = data_grouped.drop(['discharges'],axis=1)
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['per_capita']

    return d

@app.route('/percapita-2017', methods=['GET'])
def percapita_2017():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2017', con=engine)
    data_grouped = data_head.groupby(['Service_Line']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped['per_capita'] = data_grouped['discharges']/50127169
    data_grouped = data_grouped.drop(['discharges'],axis=1)
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['per_capita']

    return d

@app.route('/percapita-2016', methods=['GET'])
def percapita_2016():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2016', con=engine)
    data_grouped = data_head.groupby(['Service_Line']).agg({'Total_Discharges': ['sum']})
    data_grouped.columns = ['discharges']
    data_grouped['per_capita'] = data_grouped['discharges']/48e6
    data_grouped = data_grouped.drop(['discharges'],axis=1)
    data_grouped = data_grouped.reset_index()

    d = {}
    for idx, row in data_grouped.iterrows():
        d[row['Service_Line']] = row['per_capita']

    return d

if __name__ == "__main__":
    app.run(debug=True)
