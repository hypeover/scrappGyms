import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
networks_dir = os.path.join(current_dir, 'networks')
sys.path.append(networks_dir)

from benefit_systems import get_gym_details
from calypso import scrape_calypso
from cityfit import scrape_cityfit
from justgym import scrape_justgym
from wellfitness import scrape_wellfintness
from xtremefitness import scrape_xf

def run_all_updates():
    print("Updating data...")

    scrappers = [
        "Benefit_systems", get_gym_details,
        "Calypso", scrape_calypso,
        "CityFit", scrape_cityfit,
        "JustGym", scrape_justgym,
        "Well Fitness", scrape_wellfintness,
        "Xtreme Fitness", scrape_xf
    ]

    for name, func in scrappers:
        try:
            print(f"🔄 Collecting data from: {name}...")
            func()
            print(f"✅ Complete: {name}")
        except Exception as e:
            print(f"❌ Error with {name}: {e}")
    
    print("Data updating has been completed")

if __name__ == "__main__":
    run_all_updates()