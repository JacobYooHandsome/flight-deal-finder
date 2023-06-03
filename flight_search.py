import requests as r
import os
from dotenv import load_dotenv

load_dotenv()

class FlightSearch:
    def __init__(self):
        self.FLIGHT_URL = "https://api.tequila.kiwi.com/"
        self.flight_headers = {
            "apikey": os.getenv("FLIGHT_APIKEY")
        }

    def find_IATAs(self, cities):
        IATA_array = []
        for city in cities:
            flight_params = {
                    "term": city,
                    "limit": 1,
                    "location_types": "airport"
                }
            location_res = r.get(url=f"{self.FLIGHT_URL}locations/query", headers=self.flight_headers, params=flight_params)
            location_res.raise_for_status()
            
            IATA_array.append(location_res.json()["locations"][0]["city"]["code"])
        return IATA_array

    def find_deals(self, deal_params):
        search_res = r.get(url=f"{self.FLIGHT_URL}v2/search", headers=self.flight_headers, params=deal_params)
        search_res.raise_for_status()
        search_data = search_res.json()
        return search_data
        # try:
        #     with open("response.json", "r") as json_file:
        #         data = json.load(json_file)
        #         data.update(search_data)
        # except:
        #     with open("response.json", "w") as json_file:
        #         json.dump(search_data, json_file, indent=4)
        # else:
        #     with open("response.json", "w") as json_file:
        #         json.dump(search_data, json_file, indent=4)

# for result in search_data, find the lowest price
# price = search_data["data"][0]["price"]

# city_from = search_data["data"][0]["cityFrom"]
# code_from = search_data["data"][0]["cityCodeFrom"]

# city_to = search_data["data"][0]["cityTo"]
# code_to = search_data["data"][0]["cityCodeTo"]
