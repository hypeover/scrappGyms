import requests
from bs4 import BeautifulSoup
import re 
import sys
import os

# Ta linia dodaje folder 'scrapper' do pamięci Pythona
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Teraz importujemy z nowej nazwy:
try:
    from db_manager import upsert_benefit_systems_gyms_to_db
except ImportError:
    # Backup na wypadek gdyby Python szukał inaczej
    from ..db_manager import upsert_benefit_systems_gyms_to_db

def clean_address_data(raw_address):
    zip_code_pattern = r'\d{2}-\d{3}'
    match = re.search(zip_code_pattern, raw_address)
    
    if match:
        start_index = match.start()
        address_val = raw_address[:start_index].strip().rstrip(',')
        city_part = raw_address[start_index:].strip()
        city_val = city_part.split(' ')[-1]
        
        return address_val, city_val
    else:
        if ',' in raw_address:
            parts = raw_address.split(',')
            return parts[0].strip(), parts[1].strip().split(' ')[-1]
        return raw_address, "Polska"

def scrape_cityfit():
    url = "https://cityfit.pl/nasze-kluby/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    cityfit_hours = {day: "00:00-23:59" for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        club_items = soup.find_all('div', class_='our-clubs__item')

        for item in club_items:
            raw_address = item.get('data-address', '')
            address_val, city_val = clean_address_data(raw_address)

            gym_row = {
                "id": f"cityfit-{item.get('data-id')}",
                "name": item.get('data-title'),
                "network": "CityFit",
                "address": address_val,
                "city": city_val,
                "latitude": float(item.get('data-lat') or 0),
                "longitude": float(item.get('data-lng') or 0),
                "hours": cityfit_hours,
                "link": item.find('div', class_='our-clubs__title').find('a').get('href')
            }

            upsert_benefit_systems_gyms_to_db(gym_row)
            print(f"✅ Saved: {city_val} | {address_val}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_cityfit()