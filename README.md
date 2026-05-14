
# 🏋️‍♂️ scrappGyms – Interactive Fitness Network Map

scrappGyms is a high-performance web application that aggregates real-time data from Poland's leading fitness networks ([JustGym](https://justgym.pl/), [Zdrofit](https://zdrofit.pl/), [Fitness Academy](https://fitness-academy.com.pl/), [Fabryka Formy](https://fabryka-formy.pl/), [Calypso](https://www.calypso.com.pl/), [CityFit](https://cityfit.pl/), [FitFabric](https://fitfabric.pl/), [Xtreme Fitness](https://www.xtremefitness.pl/), [Well Fitness](https://wellfitness.pl/) ). By combining automated web scraping with geographic data visualization, it provides users with a unified, interactive map of all available gym locations and their operating hours.


## ✨ Key Features

📍 Interactive Mapping: Full-screen visualization of gym locations across Poland with smart marker clustering for improved readability.

🕒 Live Operating Hours: Real-time extraction of opening hours directly from club websites, including full support for 24/7 facilities.

🤖 Advanced Scraper Engine: A robust Python-based backend using Playwright and BeautifulSoup4 to handle dynamic JavaScript rendering and anti-bot protections.

🌍 Geocoding & Data Validation: Automated conversion of street addresses into precise GPS coordinates via Nominatim, with built-in logic to detect and fix corrupted or duplicate spatial data.

⚡ Modern Performance: A lightning-fast frontend built with Next.js 15, optimized for mobile and desktop experiences.
## 🚀 Tech Stack

Frontend (Web App)

* Framework: Next.js 15 (App Router)
* Styling: Tailwind CSS
* UI Components: Lucide React, shadcn/ui
* Language: TypeScript

Backend (Data Pipeline)
* Language: Python 3.x
* Scraping & Automation: Playwright, BeautifulSoup4
* Database: Supabase (PostgreSQL)
* Geocoding: Geopy (Nominatim API)
## 📊 How It Works

* Extraction: Python scripts crawl the main landing pages of fitness networks to collect individual club URLs.

* Deep Parsing: For each club, Playwright renders the page to capture dynamically loaded content, while BeautifulSoup extracts Structured Data (JSON-LD) containing names, addresses, and geo-coordinates.

* Data Sanitization: The script validates coordinates. If data is missing or "corrupted" (e.g., duplicate lat/lng), the system cleans the address and performs a secondary geocoding request to ensure accuracy.

* Database Upsert: Records are pushed to Supabase using an upsert strategy, ensuring that existing clubs are updated with the latest hours while new clubs are added seamlessly.
## 🛠️ Installation & Local Setup

* **Clone the repository**

```bash
git clone https://github.com/hypeover/scrappGyms
cd scrappGyms
```

* **Setup the Scraper (Python)**
```bash
cd scrapper
pip install -r requirements.txt
playwright install chromium --with-deps
python main.py
```
*Note: Configure your Supabase credentials in database.py before running.*

* **Setup the Frontend (Next.js)**
```bash
cd frontend
npm install
npm run dev
```
## 📝 License
This project is licensed under the MIT License. You are free to use, modify, and distribute it.
* **Data Ownership**: This project is strictly for educational and portfolio purposes. I do not claim ownership of the data (gym names, addresses, operating hours, etc.) extracted during the scraping process. All data belongs to its respective owners (JustGym, Zdrofit, and other fitness networks).

* **Usage Policy**: The scraper was built to demonstrate technical proficiency in web automation and data visualization. It should not be used for commercial purposes or in a way that violates the Terms of Service of the targeted websites.
