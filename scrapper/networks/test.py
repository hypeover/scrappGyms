import requests
from bs4 import BeautifulSoup
import time
from geopy.geocoders import Nominatim


def get_coords(address, city):
    try:
        loc = Nominatim(user_agent="GymMapProject_Scraper")
        search_query = f"{address.replace('ul. ', '')}, {city}, Poland"
        getLoc = loc.geocode(search_query)
        if getLoc:
            print(getLoc.latitude, getLoc.longitude)
        return 0.0, 0.0 
    except Exception as e:
        print(f"❌ Error fetching coordinates for {address}, {city}: {e}")
        return 0.0, 0.0

get_coords("ul. Jana III Sobieskiego 6", "Dąbrowa Górnicza")