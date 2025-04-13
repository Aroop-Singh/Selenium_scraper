# Glassdoor Salary Scraper
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Initialize Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

# Open Glassdoor
driver.get("https://www.glassdoor.co.in/")
print("\nLOGGING in wait\n")
time.sleep(4)

# Log into Glassdoor
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "inlineUserEmail"))
    ).send_keys("use your own @gmail.com")
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "emailButton"))
    ).click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "inlineUserPassword"))
    ).send_keys("use your own", Keys.RETURN)
    time.sleep(5)

    # Navigate to the "Salaries" tab
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Salaries"))
    ).click()
    time.sleep(2)

    # Wait for the role (job title) input field
    role_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Your job title"]'))
    )
    role_input.clear()
    role_input.send_keys("Analyst")
    time.sleep(3)

    # Wait for the location input field
    location_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="location-autocomplete_label"]'))
    )
    location_input.clear()
    location_input.send_keys("Bengaluru (India)")
    time.sleep(1)

    dropdown_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'location-autocomplete-search-suggestions'))
    )
    dropdown_input.click()
    time.sleep(3)

    # Submit the search by pressing Search
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'HeroSearch_searchButton__33N2u'))
    ).click()
    time.sleep(5)

except Exception as e:
    print(f"Error during login or search: {e}")
    driver.quit()
    exit()

# Scroll down the page to load more results
try:
    for _ in range(3):  # Scroll multiple times to ensure all listings are loaded
        driver.execute_script("window.scrollBy(0,1000);")
        time.sleep(1)

    print("Scrolled the page successfully.")

except Exception as e:
    print(f"Error scrolling the page: {e}")

# Prepare CSV file
csv_filename = "Glassdoor_full.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Company", "Role", "Rating", "Salary", "Median Salary", "Open Jobs"])

def scrape_page():
    """Function to scrape salary listing data on the current page."""
    while True:
        try:
            listings = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "SalariesList_Item__WbllO"))
            )
            
            for listing in listings:
                try:
                    company = listing.find_element(By.CLASS_NAME, "salary-card_EmployerName__y02_p").text.strip()
                    role = listing.find_element(By.CLASS_NAME, "salary-card_TitleTrim__HAigD").text.strip()
                    rating = listing.find_element(By.CLASS_NAME, "salary-card_Rating__EUxG2").text.strip()
                    salary = listing.find_element(By.CLASS_NAME, "salary-card_TotalPay__qajkN").text.replace("\n", " ").strip()
                    median_salary = listing.find_element(By.CLASS_NAME, "salary-card_BreakdownBold__o0N1l").text.replace("\n", " ").strip()
                    open_jobs = listing.find_element(By.CLASS_NAME, "button_ButtonContent__C7s3i").text.strip()

                    # Write to CSV
                    with open(csv_filename, mode="a", newline="", encoding="utf-8-sig") as file:
                        writer = csv.writer(file)
                        writer.writerow([company, role, rating, salary, median_salary, open_jobs])

                    print(f"Scraped: {company} | {role} | {rating} | {salary} | {median_salary} | {open_jobs}")

                except NoSuchElementException:
                    print("Some elements are missing in this listing. Skipping...")
            
            break  # If scraping succeeds, exit retry loop

        except TimeoutException:
            print("No listings found on this page or page took too long to load.")
            input("Press ENTER after fixing the issue to retry...")


# Loop through all pages with manual retry option
while True:
    scrape_page()

    while True:  # Retry loop for pagination
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next"]'))
            )
            next_button.click()
            time.sleep(5)  # Allow time for the next page to load
            break  # If next button works, break retry loop
        
        except (NoSuchElementException, TimeoutException):
            print("No more pages found OR page not loading.")
            choice = input("Press ENTER after fixing issue to retry pagination OR type 'exit' to stop scraping: ")
            if choice.lower() == "exit":
                driver.quit()
                exit()

print(f"Scraping completed. Data saved to '{csv_filename}'.")
input("\n\nPRESS ENTER TO continue...\n\n")
driver.quit()


