from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Maximize the window
driver.maximize_window()

# Open the Amazon website
driver.get("https://www.amazon.in/")
print("\nData is being copied to csv [WAIT]\n")

# Find the search box element
elem = driver.find_element(By.NAME, "field-keywords")
elem.clear()
elem.send_keys("mobile under 30000")
elem.send_keys(Keys.RETURN)

# Wait for the results to load
time.sleep(5)

# Open a CSV file for writing
with open("amazon_mobiles_30k_5x.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Title", "Price", "Link"])  # Write header row

    # Function to extract data from the current page
    def scrape_current_page():
        titles = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
        prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")
        links = driver.find_elements(By.XPATH, "//a[@class='a-link-normal s-no-outline']")

        for title, price, link in zip(titles, prices, links):
            product_link = link.get_attribute("href")  # Get the hyperlink for the product
            csvwriter.writerow([title.text, price.text, product_link])

    # Scrape the first page
    scrape_current_page()

    # Loop through the next 4 pages
    for _ in range(4):  # Adjust the range if you want to scrape more pages
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next') and @aria-label]")
            next_button.click()  # Click the "Next" button
            time.sleep(5)  # Wait for the next page to load
            scrape_current_page()
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

print("\nData saved to csv\n")

# Keep the browser open
input("PRESS ENTER TO CLOSE THE BROWSER...\n\n")
driver.quit()
