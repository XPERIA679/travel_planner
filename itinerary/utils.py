import google.generativeai as gemini
import os

from Tools.i18n.msgfmt import generate
from dotenv import load_dotenv
import requests

load_dotenv()

gemini.configure(api_key=os.environ["GMAPS_API_KEY"])

def generate_itinerary(destination, preferences):
    model = gemini.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""Create a personalized day-by-day itinerary for {destination} based on preferences: {preferences}.
        Ensure the response is formatted in Markdown with the following structure:
        - **Day 1:** [Title]
          - **Morning:** [Activities]
          - **Midday:** [Activities]
          - **Afternoon:** [Activities]
          - **Evening:** [Activities]
        - **Day 2:** [Title]
          ...
        Include any important notes at the end, prefixed with "Important Notes:" and listed as bullet points
        """)
    if hasattr(response, "text"):
        return response.text
    else:
        return "Unable to generate itinerary"

def get_lat_lon_from_destination(destination):
    geocode_api_key = os.environ["GMAPS_API_KEY"]
    geocode_url = F"https://maps.googleapis.com/maps/api/geocode/json?address={destination}&key={geocode_api_key}"
    response = requests.get(geocode_url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

def get_local_recommendations(destination):
    maps_api_key = os.environ["GMAPS_API_KEY"]
    lat, lon = get_lat_lon_from_destination(destination)
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=1500&type=tourist_attraction&key={maps_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch recommendations"}

def get_weather_forecast(destination):
    weather_api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={destination}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# if __name__ == "__main__":
#     generate_itinerary("San Francisco", "Hiking")