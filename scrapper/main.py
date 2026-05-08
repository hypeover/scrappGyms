from networks.benefit_systems import scrape_benefit_systems
from networks.calypso import scrape_calypso
from networks.cityfit import scrape_cityfit
from networks.justgym import scrape_justgym
from networks.wellfitness import scrape_wellfintness
from networks.xtremefitness import scrape_xf

def run_all_updates():
    print("Updating data...")

    scrappers = [
        ("Benefit Systems", scrape_benefit_systems),
        ("Calypso", scrape_calypso),
        ("CityFit", scrape_cityfit),
        ("JustGym", scrape_justgym),
        ("Well Fitness", scrape_wellfintness),
        ("Xtreme Fitness", scrape_xf),
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