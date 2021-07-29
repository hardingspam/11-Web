from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# setup sql connection
conn = "postgres:postgres@localhost:5432/medicare_drg"
engine = create_engine(f'postgresql://{conn}')

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient limit 5', con=engine)
    cases = data_head.to_dict('records')

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", cases=cases)

@app.route('/cases2', methods=['GET'])
def cases2():
    # write a statement that finds all the items in the db and sets it to a variable
    data_head = pd.read_sql_query('select * from inpatient where "Year" = 2018 limit 5', con=engine)
    cases = data_head.to_json(orient='records')

    print(cases)
    return cases


if __name__ == "__main__":
    app.run(debug=True)
