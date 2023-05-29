from  sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
import psycopg2 as pc2
import pandas.io.sql as psql

class WoolworthDb:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connection(self):
        engine = create_engine(self.connection_string)
        engine.connect()
        return engine

woolDB = WoolworthDb('postgresql://postgres:root@localhost:5432/woolworths').connection()
print(woolDB)

# for csv_file in os.listdir('woolworth_product'):
file_path = f'woolworth_product/MASTER_PRODUCTS_20230519.csv'
# create a df
df = pd.read_csv(file_path,index_col=False)
# send dataframe to sql
df.to_sql('woolworthsmaster', woolDB, if_exists='append',index=False)
# print(f'{csv_file} inserted')
print('done')