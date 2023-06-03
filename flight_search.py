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

    def find_deals(self, fly_from, fly_to, date_from, date_to, price_limit, currency="USD", sort_by="price"):
        search_params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "price_to": price_limit,
            "curr": currency,
            "sort": sort_by
        }

        search_res = r.get(url=f"{self.FLIGHT_URL}v2/search", headers=self.flight_headers, params=search_params)
        search_res.raise_for_status()
        search_data = search_res.json()
        return search_data