# Import libraries
import json
import pandas as pd
import http.client

class SkyscannerAPI:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("skyscanner80.p.rapidapi.com")
        self.header = {
            'x-rapidapi-key': "bbd500e575msh8b6216281c62aacp12709bjsn4475a6e25ce1",
            'x-rapidapi-host': "skyscanner80.p.rapidapi.com"
        }
    
    # Convert json to df
    def json_to_df(self, json_data):
        
        parsed_json = json.loads(json_data.decode("utf-8"))
        data = parsed_json["data"]
        df = pd.DataFrame(data)
        
        return df
    
    # Return price column
    def extract_nested_name(json_obj):
        return json_obj['raw']
    
    # Filter json column
    def filter_json_column(self, row, key, value):
        return row.get(key) == value
        

    # Get country data
    def get_country(self):
        self.conn.request("GET", "/api/v1/get-config", headers=self.header)
        res = self.conn.getresponse()
        data = res.read()
        df = self.json_to_df(data)
        
        return df
    
    # Get airport data
    def get_airport(self, input_airport, market, locale, country):
        self.conn.request("GET", f"/api/v1/flights/auto-complete?query={input_airport}&market={market}&locale={locale}", headers=self.header)
        res = self.conn.getresponse()
        data = res.read()
        df = self.json_to_df(data)
        df = df[df['presentation'].apply(self.filter_json_column, key='subtitle', value=country)]
        
        return df
    
    # Get flights
    def get_flight(self, origin_id, dest_id,  dep_date, ret_date, country, currency, market, locale):
        self.conn.request("GET", f"/api/v1/flights/search-roundtrip?fromId={origin_id}&toId={dest_id}&departDate={dep_date}&returnDate={ret_date}&adults=1&cabinClass=economy&currency={currency}&market={market}&locale={locale}", headers=self.header)

        res = self.conn.getresponse()
        data = res.read()
        parsed_json = json.loads(data.decode("utf-8"))
        data = parsed_json["data"]["itineraries"]
        df = pd.DataFrame(data)
        
        df[f'price_{currency}'] = df.price.str['raw'].replace('.','').replace('.',',')
        ##.apply(self.extract_nested_name)
        df = df.drop(columns=['price'])
        
        return df