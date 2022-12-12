import requests
import pandas as pd
import geopandas as gpd


class GooglePlacesAPI:

    def __init__(self, api_key):
        self.api_key = api_key

    def determineOptimalDistVal(self, iterateStep):
        """ Takes a step amount in dd (˚) and calculates the optimal amount
        of overlap that can be used as a value for the radius param in the
        searchGoogle function. Output value is in meters."""
        stepMeters = 111139 * iterateStep
        roundedVal = round(stepMeters, -3)

        if roundedVal < stepMeters:
            roundedVal += 1000

        return int(roundedVal)

    def searchToJSON(self, lat, long, radius, keyword):
        # Getting Parameters Configured
        location = str(lat) + "%2C" + str(long)

        payload = {"location": location, "radius": str(radius), "keyword": keyword, "key": self.api_key}

        # Getting request
        response = requests.request("GET", "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)

        # Note: Not an actual JSON - can keep to use Python list/dist methods for parsing
        json_response = response.json()

        return json_response["results"]

    def searchToDF(self, lat, long, radius, keyword):
        # Getting Parameters Configured
        location = str(lat) + "%2C" + str(long)

        payload = {"location": location, "radius": str(radius), "keyword": keyword, "key": self.api_key}

        # Getting request
        response = requests.request("GET", "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)

        # Note: Not an actual JSON - can keep to use Python list/dist methods for parsing
        json_response = response.json()

        json_input = json_response["results"]

        # Create DF with column names
        df = pd.DataFrame(columns=("Name", "Latitude", "Longitude", "Address", "Icon_URL"))
        
        # Loop through the JSON and add all features to the DF
        for i in range(len(json_input)):
            name = [json_input[i]["name"]]
            lat = [json_input[i]["geometry"]["location"]["lat"]]
            lng = [json_input[i]["geometry"]["location"]["lng"]]
            address = [json_input[i]["vicinity"]]
            icon = [json_input[i]["icon"]]
            
            df.loc[i] = name + lat + lng + address + icon
        
        # Convert DF to GDF, set CRS, and return
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
        
        gdf.set_crs("EPSG:4326")
            
        return gdf

    def iterateSearch(self, xMin, xMax, yMin, yMax, step, keyword):

        rad = str(determineOptimalDistVal(self, step))

        final_df = pd.DataFrame(columns=("Name", "Latitude", "Longitude", "Address", "Icon_URL"))
        
        for i in np.arange(xMin, xMax, step):
            for j in np.arange(yMin, yMax, step):
                query = searchToDF(j, i, rad, keyword)
                final_df = pd.concat([query, final_df], axis = 0)
                
        return final_df
