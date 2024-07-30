import json
import pandas as pd

import http.client

conn = http.client.HTTPSConnection("skyscanner80.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "bbd500e575msh8b6216281c62aacp12709bjsn4475a6e25ce1",
    'x-rapidapi-host': "skyscanner80.p.rapidapi.com"
}

# Get country data
conn.request("GET", "/api/v1/get-config", headers=headers)

res = conn.getresponse()
data = res.read()

# Parse the JSON data
parsed_json = json.loads(data.decode("utf-8"))

# Extract the "data" part
data = parsed_json["data"]

# Convert to DataFrame
df = pd.DataFrame(data)

# Export DataFrame to CSV file
csv_file_path = 'countries_data.csv'
df.to_csv(csv_file_path, index=False)

# User input for filtering
input_value = input("Enter the origin country abreviation to filter by: ")

# Filter the DataFrame by the input value in the 'country' column
filtered_df = df[df['market'] == input_value]

# Check if there is any matching row
if not filtered_df.empty:
    # Extract values from the two specified columns
    market = filtered_df['market'].values[0]
    currency = filtered_df['currency'].values[0]
    locale = filtered_df['locale'].values[0]
    
     # Print the extracted values
    print(f"Market: {market}, Currency: {currency}, Locale {locale}")
else:
    print("No matching country found.")

# User input for filtering
input_airport = input("Enter the origin airport to be filter by: ")

# Get airport data
conn.request("GET", f"/api/v1/flights/auto-complete?query={input_airport}&market={market}&locale={locale}", headers=headers)

res = conn.getresponse()
data = res.read()

# Parse the JSON data
parsed_json = json.loads(data.decode("utf-8"))

# Extract the "data" part
data = parsed_json["data"]

# Convert to DataFrame
df = pd.DataFrame(data)

# Export DataFrame to CSV file
csv_file_path = 'airport_data.csv'
df.to_csv(csv_file_path, index=False)

# Define a function to filter the DataFrame based on the JSON content
def filter_json_column(row, key, value):
    return row.get(key) == value

# Apply the filter to the DataFrame
filtered_df = df[df['presentation'].apply(filter_json_column, key='title', value=input_airport)]

# Display the filtered DataFrame
print(filtered_df)