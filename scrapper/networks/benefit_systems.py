import requests
from bs4 import BeautifulSoup
import json
import time
from database import upsert_benefit_systems_gyms_to_db
import cloudscraper

def get_gym_details(url, network_name):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"DEBUG {name}: Status {response.status_code}")
        print(f"DEBUG {name}: HTML Length {len(response.text)}")
        if "cloud-flare" in response.text.lower() or response.status_code == 403:
            print(f"❌ Blokada CloudFlare/BotDetection na {name}!")
        target_script = soup.find('script', string=lambda t: t and 'SportsActivityLocation' in t)
        if not target_script:
            return None
            
        data = json.loads(target_script.string)
        
        if isinstance(data, dict) and "@graph" in data:
            data = next((item for item in data["@graph"] if item["@type"] == "SportsActivityLocation"), data)

        return {
            "id": f"{network_name.lower()}-{url.strip('/').split('/')[-1]}", # Unikalny ID
            "name": data.get("name"),
            "network": network_name,
            "address": data.get("address", {}).get("streetAddress"),
            "city": data.get("address", {}).get("addressLocality"),
            "latitude": float(data.get("geo", {}).get("latitude")),
            "longitude": float(data.get("geo", {}).get("longitude")),
            "hours": {
                spec.get("dayOfWeek").split("/")[-1]: f"{spec.get('opens')}-{spec.get('closes')}"
                for spec in data.get("openingHoursSpecification", [])
            },
            "link": url
        }
    except Exception as e:
        print(f"❌ Error {url}: {e}")
        return None

def scrape_benefit_systems():
    links_with_network = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
}
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    clubs_list = [
        ("https://zdrofit.pl/kluby-fitness", "Zdrofit"),
        ("https://fitness-academy.com.pl/kluby-fitness", "Fitness Academy"),
        ("https://fitfabric.pl/kluby-fitness", "FitFabric"),
    ]

    for url, name in clubs_list:
        print(f"🔍 Collecting links from: {name}")
        try:
            response = scraper.get(url, timeout=20)
            print(f"DEBUG {name}: Status {response.status_code}, Length {len(response.text)}")
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', class_='button primary'):
                href = link.get('href')
                if href and href.startswith("/kluby-fitness/"):
                    base = url.split("/kluby-fitness")[0]
                    links_with_network.append((base + href, name))
        except Exception as e:
            print(f"❌ Could not reach {name}: {e}")

    ff_clubs_list = [
        ("https://fabryka-formy.pl/kluby-fitness", "Fabryka Formy"),
        ("https://stepone.pl/kluby-fitness", "StepOne")
    ]

    for url, name in ff_clubs_list:
        print(f"🔍 Collecting links from: {name}")
        try:
            response = scraper.get(url, timeout=20)
            print(f"DEBUG {name}: Status {response.status_code}, Length {len(response.text)}")
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.select('ul > li > div > a'):
                href = link.get('href')
                if href and href.startswith("/kluby-fitness/"):
                    base = url.split("/kluby-fitness")[0]
                    links_with_network.append((base + href, name))
        except Exception as e:
            print(f"❌ Could not reach {name}: {e}")

    print(f"\n🚀 Found {len(links_with_network)} gyms. Starting upsert...")

    for full_url, network_name in links_with_network:
        gym_data = get_gym_details(full_url, network_name)
        if gym_data:
            upsert_benefit_systems_gyms_to_db(gym_data)
            print(f"✅ Saved: {gym_data['name']} [{network_name}]")
        time.sleep(1)

if __name__ == "__main__":
    scrape_benefit_systems()