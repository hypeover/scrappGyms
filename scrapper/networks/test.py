import cloudscraper
import time
import json
from database import upsert_benefit_systems_gyms_to_db

def scrape_benefit_systems():
    # Używamy jednego scrapera dla całej sesji
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )

    # API endpointy są znacznie stabilniejsze niż HTML
    networks = [
        {"url": "https://zdrofit.pl/api/clubs/getclubs", "name": "Zdrofit", "base": "https://zdrofit.pl"},
        {"url": "https://fitness-academy.com.pl/api/clubs/getclubs", "name": "Fitness Academy", "base": "https://fitness-academy.com.pl"},
        {"url": "https://fitfabric.pl/api/clubs/getclubs", "name": "FitFabric", "base": "https://fitfabric.pl"},
        {"url": "https://fabryka-formy.pl/api/clubs/getclubs", "name": "Fabryka Formy", "base": "https://fabryka-formy.pl"},
        {"url": "https://stepone.pl/api/clubs/getclubs", "name": "StepOne", "base": "https://stepone.pl"}
    ]

    for net in networks:
        print(f"🔍 Fetching API for: {net['name']}...")
        try:
            response = scraper.get(net['url'], timeout=20)
            
            if response.status_code != 200:
                print(f"❌ {net['name']} returned status {response.status_code}. Skipping.")
                continue

            clubs = response.json() # API zwraca gotową listę
            print(f"🚀 Found {len(clubs)} gyms in {net['name']}.")

            for club in clubs:
                # Mapujemy dane z API na Twój format bazy danych
                try:
                    # Wyciągamy URL z API (zazwyczaj pole 'url')
                    club_url = net['base'] + club.get('url', '')
                    
                    gym_data = {
                        "id": f"{net['name'].lower()}-{club.get('id')}",
                        "name": club.get("name"),
                        "network": net['name'],
                        "address": club.get("address"),
                        "city": club.get("city"),
                        "latitude": float(club.get("latitude")),
                        "longitude": float(club.get("longitude")),
                        "hours": club.get("openingHours", {}), # API często ma to już sformatowane
                        "link": club_url
                    }
                    
                    upsert_benefit_systems_gyms_to_db(gym_data)
                    print(f"  ✅ Saved: {gym_data['name']}")
                except Exception as e:
                    print(f"  ⚠️ Error processing club {club.get('name')}: {e}")
            
            time.sleep(2) # Oddech dla serwera

        except Exception as e:
            print(f"❌ Critical error for {net['name']}: {e}")

if __name__ == "__main__":
    scrape_benefit_systems()