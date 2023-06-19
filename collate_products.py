import os
import pandas as pd
df_list = []
for csv_file in os.listdir(f'woolworth_product/2023613'):
    print(csv_file)
    file_path  = f'woolworth_product/2023613/{csv_file}'
    try:
        df = pd.read_csv(file_path)
        df_list.append(df)
    except Exception as e:
        print(f"{csv_file} - {e}")
        # print(e)
df_master = pd.concat(df_list)
# remove duplicates based on product barcode
print(df_master.columns)
df_master = df_master.drop_duplicates(subset=['barcode'])
print(df_master.columns)
df_master.to_csv(f'woolworth_product/2023613/MASTER_PRODUCTS_2023613.csv', index=False)