import os
import requests
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.endpoint = os.getenv("SHEETY_ENDPOINT")
        self.headers = {
            "Authorization" : os.getenv("AUTH_TOKEN")
        }
        self.data = {}

    def get_data(self):
        response = requests.get(url=self.endpoint, headers=self.headers)
        data = response.json()
        self.data = data["prices"]

        return self.data

    def update_data(self):
        for city in self.data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            response = requests.put(url=f"{self.endpoint}/{city['id']}", headers=self.headers, json=new_data)
            print(response.text)


