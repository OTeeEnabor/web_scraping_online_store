from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
import psycopg2 as pc2
import pandas.io.sql as psql
import re

def weight_extract_convert(weight_string):
    # combination regular expression
    # combination regular expression
    combination_weight_re = "[0-9]+ x [0-9]+ (g|kg|ml|L) | [0-9]+ x [0-9]+.[0-9]+ (g|kg|ml|L) "
    # singular regular expression
    singular_weight_re = "[0-9]+ (g|kg|ml|L) | [0-9]+.[0-9]+ (g|kg|ml|L)"

    # check for combination string
    if re.search(combination_weight_re, weight_string):
        # split the string into list - [num units , weigh_per_unit]
        combination_split = re.search(combination_weight_re, weight_string).group().split(' x ')
        # num_units
        num_units = int(combination_split[0])
        # unit_string - [g,kg,ml, l]
        weight_unit_string = combination_split[1]
        # check if weight unit is grammes
        if (" g" in weight_unit_string):
            # remove the gramme unit, convert string to float
            weight = float(weight_unit_string.replace(" g", ""))
            # divide weight by 1000 to convert to kg
            weight = weight / 1000 * num_units
        # check if weight unit is mil litres
        elif (" ml" in weight_unit_string):
            # remove the ml unit, convert string to float
            weight = float(weight_unit_string.replace(" ml", ""))
            # divide wight by 1000 to L - 1l -kg
            weight = weight / 1000 * num_units
        # check if kg unit in string
        elif " kg" in weight_unit_string:
            # remove the kg unit in string, convert string to float
            weight = float(weight_unit_string.replace(" kg", "")) * num_units
        else:
            # remove L unit in string, convert string to float
            weight = float(weight_unit_string.replace(" L", "")) * num_units

    elif re.search(singular_weight_re, weight_string):
        # singular algorithm
        weight_string_singular = re.search(singular_weight_re, weight_string).group()
        if " g" in weight_string_singular:
            weight = float(weight_string_singular.replace(" g", "")) / 1000
        elif " ml" in weight_string_singular:
            weight = float(weight_string_singular.replace(" ml", "")) / 1000
        elif " kg" in weight_string_singular:
            weight = float(weight_string_singular.replace(" kg", ""))
        else:
            weight = float(weight_string_singular.replace(" L", ""))
    else:
        weight = None
    try:
        return round(weight, 2)
    except:
        return None

def update_weight(product_weight,product_barcode):
    """update the weight value based on product barcode"""
    sql = """ UPDATE woolworthsmaster
                SET weight = %s
                WHERE barcode = %s
    """
    conn_ = None
    updated_rows = 0
    try:
        # connect to the PostgreSQL database
        conn_ = pc2.connect('postgresql://postgres:root@localhost:5432/woolworths')
        # create a cursor
        cur_ = conn_.cursor()
        # execute the UPDATE statement
        cur_.execute(sql,(product_barcode,product_weight))
        # get number of updated rows
        updated_rows  = cur_.rowcount
        # Commit the changes to the database
        conn_.commit()
        # close communication with the PostgreSQL database
        cur_.close()
    except (Exception, pc2.DatabaseError) as error:
        print(error)
    finally:
        if conn_ is not None:
            conn_.close()
    return updated_rows
# connect to database
try:
    conn = pc2.connect('postgresql://postgres:root@localhost:5432/woolworths')

    # create a cursor
    cur = conn.cursor()
    # execure the SQL query statement
    cur.execute("SELECT barcode, name from woolworthsmaster")
    barcode_tuples = cur.fetchall()
    # close
    cur.close()
except (Exception, pc2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()
barcode_list = []
name_list = []
for barcode,name in barcode_tuples:
    barcode_list.append(barcode)
    name_list.append(name)

# for i in range(len(barcode_list)):
#     print(f"{barcode_list[i]} --- {name_list[i]}")
# create new weight list
weight_list = []
for index in range(len(name_list)):
    try:
        updated_weight = weight_extract_convert(name_list[index])
        # update_weight(updated_weight,barcode_list[index])
        print(f"{barcode_list[index]} --{name_list[index]} -- {updated_weight}")
    except Exception as error:
        print(f"{error} -- barcodode:{barcode_list[index]}")

# weight_list = [weight_extract_convert(name) for name in name_list]
# print(len(weight_list), len(barcode_list))






