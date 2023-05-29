import os

import pandas as pd
df_list = []
for csv_file in os.listdir(f'woolworth_product'):
    file_path  = f'woolworth_product/{csv_file}'
    df = pd.read_csv(file_path)
    df_list.append(df)
df_master = pd.concat(df_list)
# remove duplicates based on product barcode
print(df_master.columns)
df_master = df_master.drop(columns=['Unnamed: 0'])
print(df_master.columns)
df_master.to_csv(f'woolworth_product/MASTER_PRODUCTS_20230519_redo.csv', index=False)