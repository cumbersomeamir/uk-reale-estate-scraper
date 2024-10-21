from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Start Chrome in normal mode so you can manually complete the CAPTCHA
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Zoopla URL
url = "https://www.zoopla.co.uk/to-rent/commercial/retail-premises/london/?floor_area_units=sq_feet&price_frequency=per_year&q=London&results_sort=newest_listings&search_source=to-rent"
driver.get(url)

# Pause the script here to allow you time to pass the CAPTCHA
input("Please complete the CAPTCHA and press Enter to continue...")

# Now that you have passed the CAPTCHA, start scraping

# Define lists to store scraped data
prices = []
areas = []
locations = []
urls = []

# Loop through pages (Adjust the number of pages you want to scrape)
for page in range(1, 3):  # Change the range if you need more pages
    time.sleep(2)  # Let the page fully load
    
    # Find all property listings
    listings = driver.find_elements(By.CLASS_NAME, 'listing-results-wrapper')

    for listing in listings:
        try:
            # Scrape price
            price = listing.find_element(By.CLASS_NAME, 'listing-results-price').text
            prices.append(price)
        except:
            prices.append('N/A')

        try:
            # Scrape area (sq. ft.)
            area = listing.find_element(By.CLASS_NAME, 'num-sqft').text
            areas.append(area)
        except:
            areas.append('N/A')

        try:
            # Scrape location
            location = listing.find_element(By.CLASS_NAME, 'listing-results-address').text
            locations.append(location)
        except:
            locations.append('N/A')

        try:
            # Scrape URL
            url = listing.find_element(By.CLASS_NAME, 'listing-results-address').get_attribute('href')
            urls.append(url)
        except:
            urls.append('N/A')

    # Find the next page button and click it, if available
    try:
        next_button = driver.find_element(By.CLASS_NAME, 'css-1fbby7f-Button')
        next_button.click()
    except:
        print("No more pages to scrape.")
        break

# Close the browser once done
driver.quit()

# Create a DataFrame
data = {
    "Price": prices,
    "Area": areas,
    "Location": locations,
    "URL": urls
}

df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('zoopla_retail_listings.csv', index=False)

print("Scraping complete. Data saved to 'zoopla_retail_listings.csv'.")
