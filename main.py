import os
import time
from dotenv import load_dotenv
from data_manager import DataManager
from flight_data import get_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta


load_dotenv()
ORIGIN_CITY_CODE = "LON"
TO_PHONE = os.getenv("TO_PHONE")

# ============== SETUP ================
notification_manager = NotificationManager()
data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()

# ============== UPDATE AIRPORT CODES IN GOOGLE SHEETS ==============
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_codes(row["city"])
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.data = sheet_data
data_manager.update_data()

# ============== SEARCH FOR FLIGHTS ==============
tomorrow = (datetime.now() + timedelta(days=1))
six_months_from_now = (datetime.now() + timedelta(days=180))

for destiny in sheet_data:
    print(f"Getting flights for {destiny['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_CODE,
        destiny["iataCode"],
        from_time= tomorrow,
        to_time= six_months_from_now
    )

    cheapest_flight = get_cheapest_flight(flights)

    if cheapest_flight.price == "N/A":
        print(f"Skipping {destiny['city']} due to unavailable flight.")
        continue

    print(f"{destiny['city']}: R${cheapest_flight.price}")
    time.sleep(2)

    if destiny["lowestPrice"] > float(cheapest_flight.price):
        notification_manager.send_message(
            phone=f"whatsapp:{TO_PHONE}",
            content= f"LOW PRICE ALERT! ONLY R${cheapest_flight.price} "
                     f"to fly from {cheapest_flight.origin} "
                     f"to {cheapest_flight.destiny}, "
                     f"on {cheapest_flight.departure_date} "
                     f"until {cheapest_flight.return_date}"
        )
