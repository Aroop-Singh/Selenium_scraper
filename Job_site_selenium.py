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
driver.set_window_size(427, 760)

# Open LinkedIn
driver.get("https://www.linkedin.com")
print("\nLOGGING in wait\n")
time.sleep(4)

# Log in to LinkedIn
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign in with email"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys("use your own@gmail.com")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    ).send_keys("use your own", Keys.RETURN)
    time.sleep(10)

    # Navigate to the "Jobs" tab
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Jobs"))
    ).click()
    time.sleep(2)

    # Wait for the role (job title) input field
    role_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by title, skill, or company"]'))
    )
    role_input.clear()
    role_input.send_keys("Analyst")

    # Wait for the location input field
    location_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="City, state, or zip code"]'))
    )
    location_input.clear()
    location_input.send_keys("Bengaluru")
    time.sleep(3)

    # Submit the search by pressing Enter
    location_input.send_keys(Keys.ENTER)
    time.sleep(5)

except Exception as e:
    print(f"Error during login or search: {e}")
    driver.quit()
    exit()

try:
    # Scroll the element
    driver.execute_script("window.scrollBy(0,800);")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0,950);")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0,900);")
    time.sleep(1)

    print("Scrolled the column till end")

    driver.execute_script("window.scrollBy(0,-800);")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0,-955);")
    time.sleep(1)

    driver.execute_script("window.scrollBy(0,-910);")
    time.sleep(1)

    print("Scrolled the column till up")

except Exception as e:
    print(f"Error scrolling the column: {e}")

# Prepare CSV file
csv_filename = "linkedin_jobs_1.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Company", "Role", "Location & Applicants", "Job Type & Skills", "Easy Apply"])

    # Get all job listings on the page (limit to 25 jobs)
    try:
        job_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-entity-lockup__subtitle"))
        )

        total_jobs = min(len(job_listings), 25)  # Limit to 25 jobs
        print(f"Found {total_jobs} job postings.")

        for index in range(total_jobs):
            try:
                print(f"\nScraping job {index + 1}...")

                # Refresh job list to avoid StaleElementReferenceException
                job_listings = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-entity-lockup__subtitle"))
                )
                
                # Click on the job posting
                job_listings[index].click()
                time.sleep(3)  # Wait for job details to load

                # Extract details from the job page
                company_name = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name"))
                ).text
                print("Company:", company_name)

                role = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title").text
                print("Role:", role)

                location_time_applicant = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__primary-description-container").text
                print("Location & Applicants:", location_time_applicant)

                # Check for job type (hybrid/full-time/remote)
                try:
                    job_type_skill = driver.find_element(By.CLASS_NAME, "job-details-preferences-and-skills").text
                    job_type_skill = job_type_skill.replace("\n", " ")  # **Fix: Replace newlines with spaces**
                    print("Job Type & Skills:", job_type_skill)
                except NoSuchElementException:
                    job_type_skill = "N/A"
                    print("Job Type & Skills: N/A")

                # Easy Apply status
                try:
                    easy_apply = driver.find_element(By.CLASS_NAME, "jobs-apply-button--top-card").text
                    print("Easy Apply:", easy_apply)
                except NoSuchElementException:
                    easy_apply = "Not available"
                    print("Easy Apply: Not available")

                # Save job details to CSV
                writer.writerow([company_name, role, location_time_applicant, job_type_skill, easy_apply])

                time.sleep(2)  # Short delay before going back

                # Go back to job listings
                try:
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "scaffold-layout__detail-back-button"))
                    )
                    back_button.click()
                    print("Navigated back to job listings.")
                    time.sleep(2)  # Small delay before the next job
                except Exception as e:
                    print(f"Error clicking Back button: {e}")
                    break  # Exit loop if unable to go back

            except (StaleElementReferenceException, Exception) as e:
                print(f"Error processing job {index + 1}: {e}")
                continue  # Skip to the next job if any issue occurs

    except Exception as e:
        print(f"Error finding job listings: {e}")

print(f"Scraping completed. Data saved to '{csv_filename}'.")
input("\n\nPRESS ENTER TO continue...\n\n")
driver.quit()
