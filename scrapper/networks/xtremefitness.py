import requests
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

def parse_hours(data_hours):
    day_map = {
        "MO": "Monday", "TU": "Tuesday", "WE": "Wednesday",
        "TH": "Thursday", "FR": "Friday", "SA": "Saturday", "SU": "Sunday"
    }
    
    formatted_hours = {}
    for entry in data_hours:
        if entry.get("isOpen"):
            time_range = f"{entry.get('openTime')}-{entry.get('closeTime')}"
        else:
            time_range = "Closed"

        for day_short in entry.get("daysOfWeek", []):
            full_day_name = day_map.get(day_short)
            if full_day_name:
                formatted_hours[full_day_name] = time_range
    return formatted_hours

def scrape_xf():
    try: 
        res = requests.get("https://api.xtremefitness.pl/api/locations", timeout=10)
        res.raise_for_status()
        data = res.json()
        cities = data.get('data', {}).get('cities', [])

        for city_group in cities:
            locations = city_group.get('locations', [])
            
            for loc in locations:
                city_name = loc.get('city') or city_group.get('name')
                
                if "test" in loc.get('name', '').lower() or not city_name:
                    continue
                    
                hours_data = loc.get("openingHours", [])

                gym_row = {
                    "id": f"xf-{loc.get('key')}",
                    "name": loc.get('name'),
                    "network": "Xtreme Fitness",
                    "address": loc.get('street'),
                    "city": city_name,
                    "latitude": float(loc.get('latitude') or 0),
                    "longitude": float(loc.get('longitude') or 0),
                    "hours": parse_hours(hours_data),
                    "link": f"https://www.xtremefitness.pl/kluby/{loc.get('key')}"
                }
                
                upsert_benefit_systems_gyms_to_db(gym_row)
                print(f"✅ Przetworzono: {gym_row['name']} w {gym_row['city']}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrape_xf()