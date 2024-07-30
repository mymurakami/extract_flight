'''
    Improvements:
        -Use txt file as list of input to be executed
        -Reuse metadata files that have been extracted on this month
        -Create a docker
        -Create a job to run daily
        -Create notification if fails
        -Frontend to show the results and some metrics
        -Clean codes and review
        -Save the daily results to apply the ML
        -Power BI for these analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
'''

# Import libraries
import json
import os
import pandas as pd
import http.client
from datetime import datetime

# Instantiate the class
from skyscanner_api import SkyscannerAPI
api = SkyscannerAPI()

# Get the current date and time
now = datetime.now()

# Format the date and time as 'yyyymmdd_hhmmss'
formatted_time = now.strftime('%Y%m%d_%H%M%S')
formatted_ym = now.strftime('%Y%m')

# Get countries data
df_country = api.get_country()

# Export DataFrame to CSV file
csv_file_path = f'metadata/{formatted_ym}/countries_{formatted_time}.csv'
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
df_country.to_csv(csv_file_path, sep=';', index=False)

# ------------ Origin Airport ----------------

# User input for filtering
input_value = 'PT'#input("Enter the origin country abreviation to filter by: ")

# Filter the DataFrame by the input value in the 'country' column
df_origin = df_country[df_country['market'] == input_value]

# Check if there is any matching row
if not df_origin.empty:
    # Extract values from the two specified columns
    origin_market = df_origin['market'].values[0]
    origin_currency = df_origin['currency'].values[0]
    origin_locale = df_origin['locale'].values[0]
    origin_country = df_origin['country'].values[0]
    
     # Print the extracted values
    print(f"Market: {origin_market}, Currency: {origin_currency}, Locale {origin_locale}")
else:
    print("No matching country found.")
    
# User input for filtering
input_airport = 'Porto'#input("Enter the origin airport to be filter by: ")

# Get airport data
df_airport_origin = api.get_airport(input_airport, origin_market, origin_locale, origin_country)

# Export DataFrame to CSV file
csv_file_path = f'./metadata/{formatted_ym}/{input_airport}_airport_{formatted_time}.csv'
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
df_airport_origin.to_csv(csv_file_path, sep=';', index=False)

# ------------ Destination Airport ----------------

# User input for filtering
input_value = input("Enter the destination country abreviation to filter by: ")

# Filter the DataFrame by the input value in the 'country' column
df_dest = df_country[df_country['market'] == input_value]

# Check if there is any matching row
if not df_dest.empty:
    # Extract values from the two specified columns
    dest_market = df_dest['market'].values[0]
    dest_currency = df_dest['currency'].values[0]
    dest_locale = df_dest['locale'].values[0]
    dest_country = df_dest['country'].values[0]
    
     # Print the extracted values
    print(f"Market: {dest_market}, Currency: {dest_currency}, Locale {dest_locale}")
else:
    print("No matching country found.")
    
# User input for filtering
input_airport = input("Enter the destination airport to be filter by: ")

# Get airport data
df_airport_dest = api.get_airport(input_airport, dest_market, dest_locale, dest_country)

# Export DataFrame to CSV file
csv_file_path = f'./metadata/{formatted_ym}/{input_airport}_airport_{formatted_time}.csv'
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
df_airport_dest.to_csv(csv_file_path, sep=';', index=False)

# ------------ Get input dates ----------------
dep_date = input("Enter the depart date (yyyy-mm-dd): ")
ret_date = input("Enter the return date (yyyy-mm-dd): ")

origin_id = df_airport_origin['id'].values[0]
dest_id   = df_airport_dest['id'].values[0]

df_flight = api.get_flight(origin_id, dest_id,  dep_date, ret_date, origin_country, origin_currency, origin_market, origin_locale)


# Export DataFrame to CSV file
csv_file_path = f'./results/{formatted_ym}/flight_{origin_market}_{dest_market}_{dep_date.replace("-","")}_{ret_date.replace("-","")}_{formatted_time}.csv'
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
df_flight.to_csv(csv_file_path, sep=';', index=False)