import requests
from bs4 import BeautifulSoup
import json
from geopy.geocoders import Nominatim
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


def scrape_calypso():
    url = "https://justgym.pl/kluby/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    hours = {day: "N/A" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
    try:
        res = requests.get("https://www.calypso.com.pl/nasze-kluby/", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        select = soup.find('select', id="club-city-select")
        options = select.find_all('option')
        for option in options:
            res = requests.get(option.get('ref'))
            soup = BeautifulSoup(res.text, 'html.parser')
            elements = soup.find_all('div', class_="gotoclub")
            for element in elements:
                el = element.find('a')
                link = el.get('href')
                res = requests.get(link)
                soup = BeautifulSoup(res.text, 'html.parser')
                target_script = soup.find('script', string=lambda t: t and 'ExerciseGym' in t)
                data = json.loads(target_script.string)
                lat, lng = get_coords(data.get('address').get('streetAddress'), data.get('address').get('addressLocality'))
                
                gym_row = {
                    "id": f"calypso-{data.get('name')}",
                    "name": data.get('name'),
                    "network": "Calypso",
                    "address": data.get('address').get('streetAddress'),
                    "city": data.get('address').get('addressLocality'),
                    "latitude": lat,
                    "longitude": lng,
                    "hours": hours,
                    "link": link
                }

                upsert_benefit_systems_gyms_to_db(gym_row)
                print(f"✅ Saved: {gym_row['city']} | {gym_row['address']} (Coords: {lat}, {lng})")
                
    except Exception as e:
        print(f"Error {url}: {e}")
        return None
    
if __name__ == "__main__":
    scrape_calypso()