# Selenium-Based Web Scraper Collection

Warning: Don't run these specially linkdin on your personal account use the burner account and have an extra layer of safety like VPN. 

The data I collect through these codes are just for educational purposes and in no way to be sold or used for any monetary value.

This repository contains three Selenium-based automation scripts that extract structured data from different types of platforms. Each script is designed to work independently and saves the scraped data into CSV files for analysis or tracking.

> ⚠️ **Disclaimer**: The file names used here (e.g., `ecommerce_scraper.py`) are purposefully generic to respect platform terms of service. Actual scraping targets include Amazon, LinkedIn, and Glassdoor. Users must use their **own credentials** for scripts that require login.

---

## 🔧 General Instructions (I'm using VS code.)

1. Make sure you have **Python** and **Selenium** installed. Run pip install selenium to install selenium in your teminal 
2. You must have the Chrome WebDriver installed and added to your system PATH.
3. Open the script in VS Code or any IDE of your choice.
4. Make sure your browser window is not minimized — Selenium needs it visible.
5. Run the script and follow on-screen prompts, if any. 


# ecommerce_scraper.py → For Amazon
1. This script launches Amazon and attempts to scroll the product list.
2. Ideal for learning or customizing to extract product details.
3. Stores product-related data (when extended) into a .csv file.
4. Customize the URL and search query manually inside the script.
5. No login is required for Amazon.

Note: Update this line to taget a specific page or update the search query as well 
      driver.get("https://www.amazon.com")


# job_site_selenium.py → For LinkedIn
This script logs into LinkedIn, navigates to the Jobs section, searches for a given role and location, and scrapes all job listings.

Features: 
1. Automatically scrolls and scrapes details like company name, role, location, job type, and Easy Apply status.
2. Stores the data in linkedin_jobs_1.csv. (which you can edit for your own file name)
3. Linkdin is a stable site so it can easily go through hundread of job listing pages without any issue. Same code can be modified to get specific buissnes company employee or 
   hr data as well. 

Notes: Requires a LinkedIn login. Replace the email and password in the script:
       username.send_keys("your_email_here")
       password.send_keys("your_password_here")
      
       You can modify the search keywords from:
       role_input.send_keys("Analyst")
       location_input.send_keys("Bengaluru")
       The limit is set to 25 jobs for safety and speed.


# salarysite_scraper.py → For Glassdoor
This script logs into Glassdoor and scrapes salary data for a given role and location.

Features:
1. Scrapes company name, role, salary, rating, median salary, and open job count.
2. Navigates through multiple pages and saves all results in Glassdoor_full.csv (which you can edit for your own file name).
3. Unlike linkdin glassdoor is not that so stable so you will encounter random 404 or crashes i have a code to tackle this 404, but not so sure about crashes. 
   Requires a Glassdoor login. Replace the credentials in the script:

Note: Change your credentials here:
      send_keys("your_email_here")
      send_keys("your_password_here")
      
      Modify job role and location here:
      role_input.send_keys("Analyst")
      location_input.send_keys("Bengaluru (India)")
      Make sure to monitor and control pagination manually if needed.



# At last or conclusion:
These codes run well for now in April 2025 might need to tweak some stuffs in the future. Anti-bot detection version linkdin and 404 handler version of these I have you can ask me on linkdin for these at a cheap price. 
Thanks

