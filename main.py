from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from user_manager import UserManager

TOMMORROW = datetime.now() + timedelta(1)
F_TOMMORROW = TOMMORROW.strftime('%d/%m/%Y')
SIX_MONTHS = datetime.now() + relativedelta(months=+6)
F_SIX_MONTHS = SIX_MONTHS.strftime('%d/%m/%Y')
MY_LOCATION = "ATL"

flightSearch = FlightSearch()
dataManager = DataManager()
notificationManager = NotificationManager()
userManager = UserManager()

codes = flightSearch.find_IATAs(dataManager.cities)
dataManager.update_IATAs(codes)

for i in range(len(dataManager.cities)):
    search_data = flightSearch.find_deals(fly_from=MY_LOCATION, fly_to=codes[i], date_from=F_TOMMORROW, date_to=F_SIX_MONTHS, price_limit=int(dataManager.prices[i]))
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
        body = f"Only ${price} to fly from {city_from}-{code_from} to {city_to}-{code_to}, from {departure} to {arrival}!"
        stop_overs = len(cheapest_flight["route"]) - 1
        if stop_overs > 0:
            stopped_cities = ', '.join([route["cityTo"] for route in cheapest_flight["route"] if route["cityTo"] != city_to])
            body += f"\n\nThere are {stop_overs} stop overs in this flight. Via: {stopped_cities}."
        body += f"\n\nHere is the link: \n\n{link}"
        
        notificationManager.send_notification_all(subject, body, userManager.emails)
    
