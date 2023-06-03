from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

TOMMORROW = datetime.now() + timedelta(1)
SIX_MONTHS = datetime.now() + relativedelta(months=+6)
MY_LOCATION = "ATL"

flightSearch = FlightSearch()
dataManager = DataManager()
notificationManager = NotificationManager()

codes = flightSearch.find_IATAs(dataManager.cities)
dataManager.update_IATAs(codes)

for i in range(len(dataManager.cities)):
    search_params = {
            "fly_from": MY_LOCATION,
            "fly_to": codes[i],
            "date_from": TOMMORROW.strftime('%d/%m/%Y'),
            "date_to": SIX_MONTHS.strftime('%d/%m/%Y'),
            "price_to": int(dataManager.prices[i]),
            "curr": "USD",
            "sort": "price"
        }
    search_data = flightSearch.find_deals(search_params)
    if search_data["_results"] > 0:
        
        cheapest_flight = search_data["data"][0]
        
        price = cheapest_flight["price"]
        city_from = cheapest_flight["cityFrom"]
        code_from = cheapest_flight["cityCodeFrom"]
        city_to = cheapest_flight["cityTo"]
        code_to = cheapest_flight["cityCodeTo"]
        departure = datetime.strptime(f"{cheapest_flight['utc_departure'].replace('.000Z', '')}", "%Y-%m-%dT%H:%M:%S").strftime("%Y/%m/%d")
        arrival = datetime.strptime(f"{cheapest_flight['utc_arrival'].replace('.000Z', '')}", "%Y-%m-%dT%H:%M:%S").strftime("%Y/%m/%d")
        link = cheapest_flight["deep_link"]
        subject = f"GREAT FLIGHT DEAL FOR {city_to}!"
        body = f"Only ${price} to fly from {city_from}-{code_from} to {city_to}-{code_to}, from {departure} to {arrival}!\n This is the link: \n{link}"
        notificationManager.send_notification(subject=subject, body=body)
    
