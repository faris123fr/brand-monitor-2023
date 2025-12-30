import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_all_reviews():
    base_url = "https://web-scraping.dev/reviews" # Replace with your target URL
    all_reviews = []
    page_num = 1
    
    while True:
        # Construct the URL for the current page
        current_url = f"{base_url}?page={page_num}"
        print(f"Scraping page: {page_num}...")
        
        response = requests.get(current_url)
        if response.status_code != 200:
            break  # Exit if the page doesn't exist
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # YOUR EXISTING LOGIC: Find the review containers
        reviews = soup.select('.review-card') # Update with your specific selector
        
        if not reviews:
            break  # Exit if no reviews are found on this page
            
        for review in reviews:
            # Extract text and date logic here
            all_reviews.append({
                "date": review.select_one('.date').text, # Example selector
                "text": review.select_one('.text').text
            })
            
        # Increment to the next page
        page_num += 1
        time.sleep(1) # Ethical delay to avoid overloading the server
        
    # Save all collected data to your JSON file
    with open('data.json', 'w') as f:
        json.dump(all_reviews, f)
