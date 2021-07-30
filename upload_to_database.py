# Dependencies
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Float

# load files
medicare_2018 = pd.read_excel(f'data/Medicare_Provider_Charge_Inpatient_DRGALL_FY2018.xlsx', header=5)
medicare_2018['Year'] = 2018
medicare_2017 = pd.read_excel(f'data/Medicare_Provider_Charge_Inpatient_DRGALL_FY2017.xlsx', header=5)
medicare_2017['Year'] = 2017
medicare_2016 = pd.read_excel(f'data/Medicare_Provider_Charge_Inpatient_DRGALL_FY2016.xlsx', header=5)
medicare_2016['Year'] = 2016

# concatenate
medicare_16_17_18 = pd.concat([medicare_2018, medicare_2017, medicare_2016],axis=0)

# create MSDRG column
medicare_16_17_18['MSDRG'] = medicare_16_17_18['DRG Definition'].apply(lambda x: str(x)[:3]).astype(int)

# load and clean MSDRG crosswalk
msdrg = pd.read_excel(f'data/msdrg.xlsx', header=0)
msdrg.rename({'MSDRG ': 'MSDRG'}, axis=1, inplace=True)

# merge dataframes
medicare_data = medicare_16_17_18.merge(msdrg, how='left', on='MSDRG')

# clean merged dataframe
medicare_data.columns = medicare_data.columns.str.replace(' ','_')
medicare_data = medicare_data.rename({'Hospital_Referral_Region_(HRR)_Description':'HRR'}, axis = 1)
medicare_data = medicare_data.rename({'Service_Lines_(10)':'Service_Line'}, axis = 1)
medicare_data = medicare_data.rename({'Service_Lines_(20)':'Service_Line_20'}, axis = 1)

columns_to_keep = [
    'MSDRG',
    'Provider_Id',
    'Service_Line',
    'Product_Lines_',
    'Geometric_mean_LOS',
    'Arithmetic_mean_LOS',
    'Total_Discharges',
    'Year'
]

medicare_upload_data = medicare_data[columns_to_keep]

# Create database connection
connection_string = "postgres:postgres@localhost:5432/medicare_drg"
engine = create_engine(f'postgresql://{connection_string}')

# create table for this data
meta = MetaData()

inpatient = Table(
   'inpatient', meta,
    Column('MSDRG', Integer),
    Column('Provider_Id', String),
    Column('Service_Line', String),
    Column('Product_Lines_', String),
    Column('Geometric_mean_LOS',Float),
    Column('Arithmetic_mean_LOS',Float),
    Column('Total_Discharges',Integer),
    Column('Year',Integer)

)

meta.create_all(engine)

# Check table names
engine.table_names()

# Load dataframes into database
medicare_upload_data.to_sql(name='inpatient', con=engine, if_exists='append', index=False)

# Check to see if data loaded
print("First three rows of the data frame:")
print(pd.read_sql_query('select * from inpatient limit 3', con=engine))
