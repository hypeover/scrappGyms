from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import json
from database import upsert_benefit_systems_gyms_to_db

def get_gym_details(url, network_name):

    """ Function that scraps data from HTML """

    with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            print("Connecting with", {url}, "page.")
        
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                page.wait_for_selector('main', timeout=15000) 
                page.wait_for_timeout(2000)
    
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                target_script = soup.find('script', string=lambda t: t and 'SportsActivityLocation' in t)
                if not target_script:
                    return None
            
                data = json.loads(target_script.string)
                print("Data of", url, "has been succesfuly collected." )

                if isinstance(data, dict) and "@graph" in data:
                    data = next((item for item in data["@graph"] if item["@type"] == "SportsActivityLocation"), data)

                return {
                    "id": f"{network_name.lower()}-{url.strip('/').split('/')[-1]}",
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
                print(f"Error: {e}")
            
            finally:
                browser.close()

def scrape_benefit_systems():

    """ Function that scraps links """

    links_with_network = []
    clubs_list = [
        ("https://zdrofit.pl/kluby-fitness", "Zdrofit"),
        ("https://fitness-academy.com.pl/kluby-fitness", "Fitness Academy"),
        ("https://fitfabric.pl/kluby-fitness", "FitFabric"),
    ]

    ff_clubs_list = [
        ("https://fabryka-formy.pl/kluby-fitness", "Fabryka Formy"),
        ("https://stepone.pl/kluby-fitness", "StepOne")
    ]

    for url, name in clubs_list:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
        
            print("Connecting with", {name}, "page")
        
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                print("Waiting for the list of clubs to load...")
                page.wait_for_selector('main', timeout=15000) 
                page.wait_for_timeout(2000)
            
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                for link in soup.find_all('a', class_='button primary'):
                    href = link.get('href')
                    if href and href.startswith("/kluby-fitness/"):
                        base = url.split("/kluby-fitness")[0]
                        links_with_network.append((base + href, name))
            
            except Exception as e:
                print(f"Error: {e}")
            
            finally:
                print("Links of", name, "have been succesfuly collected.")
                browser.close()

    for url, name in ff_clubs_list:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
        
            print("Connecting with", {name}, "page")
        
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                print("Waiting for the list of clubs to load...")
                page.wait_for_selector('main', timeout=15000) 
                page.wait_for_timeout(2000)
            
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                for link in soup.select('ul > li > div > a'):
                    href = link.get('href')
                    if href and href.startswith("/kluby-fitness/"):
                        base = url.split("/kluby-fitness")[0]
                        links_with_network.append((base + href, name))
            
            except Exception as e:
                print(f"Error: {e}")
            
            finally:
                print("Links of", name, "have been succesfuly collected.")
                browser.close()


    for full_url, network_name in links_with_network:
        gym_data = get_gym_details(full_url, network_name)
        if gym_data:
            upsert_benefit_systems_gyms_to_db(gym_data)
            print(f"✅ Saved: {gym_data['name']} [{network_name}]")
        time.sleep(1)
    

if __name__ == "__main__":
    scrape_benefit_systems()