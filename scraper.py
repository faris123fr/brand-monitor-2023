import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def scrape_to_file():
    print("Starting the web scraper...")
    
    # 1. Target URL (The sandbox environment)
    url = "https://web-scraping.dev/products/"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. Extract Product Data
        products = []
        for item in soup.select('.product-card'): # This selects the product containers
            products.append({
                "name": item.select_one('.card-title').get_text(strip=True),
                "price": item.select_one('.price').get_text(strip=True)
            })

        # 3. Create Simulated 2023 Review Data
        # We simulate this to ensure you have specific dates for your 2023 analysis
        reviews = [
            {"date": "2023-01-15", "text": "Exceptional quality, I love using this every day!"},
            {"date": "2023-01-22", "text": "Very disappointed. It stopped working after a week."},
            {"date": "2023-05-10", "text": "Decent product for the price. Fast shipping."},
            {"date": "2023-08-14", "text": "Absolute waste of money. Do not buy!"},
            {"date": "2023-08-20", "text": "The best purchase I've made all year. Five stars."},
            {"date": "2023-12-05", "text": "Works as advertised, but the packaging was damaged."}
        ]

        # 4. Save everything to a JSON file
        final_data = {
            "products": products,
            "reviews": reviews,
            "testimonials": [{"user": "Customer A", "content": "Great service!"}]
        }

        with open('data.json', 'w') as f:
            json.dump(final_data, f, indent=4)
            
        print("Success! 'data.json' has been created in your folder.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_to_file()