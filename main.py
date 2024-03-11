import requests
from datetime import datetime
import os

API_KEY = os.environ.get("API_KEY")
APP_ID = os.environ.get("APP_ID")

print(APP_ID)
print(API_KEY)


GENDER = "male"
WEIGHT_KG = 78
HEIGHT_CM = 177
AGE = 22

nuritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ.get("SHEET_ENDPOINT")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

parameters = {
    "query": input("Tell me which exercise you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=nuritionix_endpoint, headers=headers, json=parameters)
response.raise_for_status()
data = response.json()

bearer_token = {
    "Authorization": os.environ.get("TOKEN")
}

today = datetime.now()
date = today.strftime("%d/%m/%Y")
time = today.strftime("%X")

for exercise in data["exercises"]:
    sheety_parameters = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_response = requests.post(url=sheety_endpoint, json=sheety_parameters, headers=bearer_token)
    print(sheet_response.text)

