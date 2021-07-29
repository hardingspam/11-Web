#dependencies
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Float

#load medicare data, append year
dfs = []
for year in range(2016, 2019):
    print(f'Loading {year}...')
    df = pd.read_excel(f'data/Medicare_Provider_Charge_Inpatient_DRGALL_FY{year}.xlsx', header=5)
    df['Year'] = year
    dfs.append(df)
medicare_data = pd.concat(dfs, axis=0)

#rename columns for sql use
medicare_data.columns = medicare_data.columns.str.replace(' ','_')
medicare_data = medicare_data.rename({'Hospital_Referral_Region_(HRR)_Description':'HRR'}, axis = 1)

#connect to postgres database via sqlalchemy
connection_string = "postgres:postgres@localhost:5432/medicare_drg"
engine = create_engine(f'postgresql://{connection_string}')

#create skeleton framework
meta = MetaData()
inpatient = Table(
   'inpatient', meta,
    Column('DRG_Definition', String),
    Column('Provider_Id', Integer),
    Column('Provider_Name', String),
    Column('Provider_Street_Address', String),
    Column('Provider_City', String),
    Column('Provider_State', String),
    Column('Provider_Zip_Code', Integer),
    Column('HRR', String),
    Column('Total_Discharges', Integer),
    Column('Average_Covered_Charges', Float),
    Column('Average_Total_Payments', Float),
    Column('Average_Medicare_Payments', Float),
    Column('Year', Integer)
)
meta.create_all(engine)

# Check table names
print(engine.table_names())

# Load dataframes into database
medicare_data.to_sql(name='inpatient', con=engine, if_exists='append', index=False)

# Check to see if data loaded in
print(pd.read_sql_query('select * from inpatient limit 5', con=engine))
