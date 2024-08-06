'''
    Improvements:
        -Connect to github - OK
        -Use txt file as list of input to be executed - OK
        -Reuse metadata files that have been extracted on this month
            -Add for country OK
                -Test
            -Add for airport origin and dest
                -Test
        -Create a docker
        -Create a job to run daily
        -Add logging
        -Create notification if fails
        -Frontend to show the results and some metrics
        -Clean codes and review
        -Save the daily results to apply the ML
        -Power BI for these analysis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
'''

# Import libraries
import json
import os
from pickle import TRUE
import pandas as pd
import http.client
from datetime import datetime

# Instantiate the class
from skyscanner_api import SkyscannerAPI
from file_utils import FileUtils
api        = SkyscannerAPI()
file_utils = FileUtils()

# Get the current date and time
now = datetime.now()

# Format the date and time as 'yyyymmdd_hhmmss'
formatted_time = now.strftime('%Y%m%d_%H%M%S')
formatted_ym   = now.strftime('%Y%m')

# Read input file
input_file = file_utils.read_input_file('./input.txt')

folder_check = file_utils.folder_exists(f'metadata/{formatted_ym}')
latest_file = file_utils.get_latest_file(f'metadata/{formatted_ym}','countries_')

# Check if the folder was created and there is a country file
if folder_check == True and latest_file != None:
    # Read the file on ym folder
    latest_file = file_utils.get_latest_file(f'metadata/{formatted_ym}','countries_')
    df_country = pd.read_csv(latest_file)

else:
    # Get countries data
    df_country = api.get_country()

    # Export DataFrame to CSV file 
    csv_file_path = f'metadata/{formatted_ym}/countries_{formatted_time}.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    df_country.to_csv(csv_file_path, sep=';', index=False)


for section in input_file.sections():
    flight         = input_file[section]
    origin_country = flight['origin_country']
    dest_country   = flight['dest_country']
    origin_airport = flight['origin_airport']
    dest_airport   = flight['dest_airport']
    origin_date    = flight['origin_date']
    dest_date      = flight['dest_date']

    # ------------ Origin Airport ----------------

    # Filter the DataFrame by the input value in the 'country' column
    df_origin = df_country[df_country['market'] == origin_country]

    # Check if there is any matching row
    if not df_origin.empty:
        # Extract values from the two specified columns
        origin_market   = df_origin['market'].values[0]
        origin_currency = df_origin['currency'].values[0]
        origin_locale   = df_origin['locale'].values[0]
        origin_country  = df_origin['country'].values[0]
    
         # Print the extracted values
        print(f"Market: {origin_market}, Currency: {origin_currency}, Locale {origin_locale}")
    else:
        print("No matching country found.")

    # Get airport data
    df_airport_origin = api.get_airport(origin_airport, origin_market, origin_locale, origin_country)

    # Export DataFrame to CSV file
    csv_file_path = f'./metadata/{formatted_ym}/{origin_airport}_airport_{formatted_time}.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    df_airport_origin.to_csv(csv_file_path, sep=';', index=False)

    # ------------ Destination Airport ----------------

    # Filter the DataFrame by the input value in the 'country' column
    df_dest = df_country[df_country['market'] == dest_country]

    # Check if there is any matching row
    if not df_dest.empty:
        # Extract values from the two specified columns
        dest_market   = df_dest['market'].values[0]
        dest_currency = df_dest['currency'].values[0]
        dest_locale   = df_dest['locale'].values[0]
        dest_country  = df_dest['country'].values[0]
    
         # Print the extracted values
        print(f"Market: {dest_market}, Currency: {dest_currency}, Locale {dest_locale}")
    else:
        print("No matching country found.")

    # Get airport data
    df_airport_dest = api.get_airport(dest_airport, dest_market, dest_locale, dest_country)

    # Export DataFrame to CSV file
    csv_file_path = f'./metadata/{formatted_ym}/{dest_airport}_airport_{formatted_time}.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    df_airport_dest.to_csv(csv_file_path, sep=';', index=False)

    # Get origin and dest id
    origin_id = df_airport_origin['id'].values[0]
    dest_id   = df_airport_dest['id'].values[0]

    df_flight = api.get_flight(origin_id, dest_id,  origin_date, dest_date, origin_country, origin_currency, origin_market, origin_locale)


    # Export DataFrame to CSV file
    csv_file_path = f'./results/{formatted_ym}/flight_{origin_market}_{dest_market}_{origin_date.replace("-","")}_{dest_date.replace("-","")}_{formatted_time}.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    df_flight.to_csv(csv_file_path, sep=';', index=False)