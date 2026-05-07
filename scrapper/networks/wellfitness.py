import requests
from bs4 import BeautifulSoup
import time
from geopy.geocoders import Nominatim
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import upsert_benefit_systems_gyms_to_db

def get_coords(address, city):
    try:
        loc = Nominatim(user_agent="GymMapProject_Scraper")
        search_query = f"{address.replace('ul. ', '')}, {city}, Poland"
        getLoc = loc.geocode(search_query)
        if getLoc:
            return getLoc.latitude, getLoc.longitude
        return 0.0, 0.0 
    except Exception as e:
        print(f"❌ Error fetching coordinates for {address}, {city}: {e}")
        return 0.0, 0.0


def get_just_gym_hours(link_key):
    try:
        wf_hours = {day: "00:00-23:59" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        res = requests.get(link_key)
        soup = BeautifulSoup(res.text, 'html.parser')
        container = soup.find('div', class_='feature-box')
        all_hours = container.find_all('div', class_='hours-row')
        for day, row in zip(days, all_hours):
            hour_text = row.find('span').text.strip()
            wf_hours[day] = hour_text
        return wf_hours
    except Exception as e:
        print(f"❌ Error fetching hours: {e}")

def scrape_wellfintness():
    url = "https://wellfitness.pl/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    wf_hours = {day: "00:00-23:59" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        clubs_items = soup.find_all('li', class_='map__city-item')

        for item in clubs_items:
            raw_lat = item.get('data-map-lat', '')
            raw_lng = item.get('data-map-long', '')

            is_lat_corrupted = len(raw_lat) > 20 or raw_lat.count('.') > 1
            is_lng_corrupted = len(raw_lng) > 20 or raw_lng.count('.') > 1        

            if not raw_lat or not raw_lng or is_lat_corrupted or is_lng_corrupted:
                print(f"⚠️ Corrupted coordinates for {item.get('data-map-place')}, geocoding...")
                lat, lng = get_coords(item.get('data-map-address'), item.get('data-map-city'))
                time.sleep(1)
            else:
                try:
                    lat = float(raw_lat)
                    lng = float(raw_lng)
                except ValueError:
                    lat, lng = get_coords(item.get('data-map-address'), item.get('data-map-city'))

            if item.get('data-map-twentyfour') == '':
                print(f"⚠️ Collecting hours for {item.get('data-map-place')}...")
                hours = get_just_gym_hours(item.get('data-map-link'))
            else:
                hours = wf_hours


            gym_row = {
            "id": f"wellfitness-{item.get('data-map-city')}-{item.get('data-map-address')}".replace(" ", "-").lower(),
            "name": item.get('data-map-place'),
            "network": "WellFitness",
            "address": item.get('data-map-address'),
            "city": item.get('data-map-city'),
            "latitude": lat,
            "longitude": lng,
            "hours": hours,
            "link": item.get("data-map-link")
            }

            upsert_benefit_systems_gyms_to_db(gym_row)
            print(f"✅ Saved: {gym_row['city']} | {gym_row['address']} (Coords: {lat}, {lng})")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_wellfintness()