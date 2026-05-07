import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upsert_benefit_systems_gyms_to_db(gym_data):
    try:
        result = supabase.table("gyms").upsert(gym_data).execute()
        return result
    except Exception as e:
        print(f"Error saving to database: {e}")
        return None
