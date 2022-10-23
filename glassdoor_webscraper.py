# used code from: https://mersakarya.medium.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905
# github: https://github.com/arapfaik/scraping-glassdoor-selenium

# import packages
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
import time
import pandas as pd


# function to get value from WebElement list
def try_index(list, index):
    try:
        var = list[index].text
    except:
        var = ''

    return var


# webscrape function
def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    #Initializing the webdriver
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(
        executable_path="/Users/stanvanklink/OneDrive/Analytics projects/salary predictions/ds_salary_predictions/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.nl/Vacature/" + keyword + \
        "-vacatures-SRCH_KO0,12.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=&context=Jobs&dropdown=0"
    driver.get(url)
    jobs = []

    # wait for the cookies pop-up to show and close it
    time.sleep(5)
    try:
        driver.find_element(
            by="xpath", value='.//button[@id="onetrust-accept-btn-handler"]').click()
    except:
        pass

    # If true, should be still looking for new jobs.
    while len(jobs) < num_jobs:

        #Going through each job in this page
        job_buttons = driver.find_elements(
            by="xpath", value='.//article[@id="MainCol"]//ul/li[@data-adv-type="GENERAL"]')
        for job_button in job_buttons:

            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            stale = True
            while(stale):
                try:
                    job_button.click()
                    stale = False
                except StaleElementReferenceException:
                    stale = True

            time.sleep(1)

            try:
                driver.find_element(
                    by="xpath", value='.//span[@class="SVGInline modal_closeIcon"]').click()
            except NoSuchElementException:
                pass

            collected_successfully = False

            while not collected_successfully:

                try:
                    company_name = driver.find_element(
                        by="xpath", value='.//div[@class="css-87uc0g e1tk4kwz1"]').text
                except NoSuchElementException:
                    company_name = ''

                try:
                    location = driver.find_element(
                        by="xpath", value='.//div[@class="css-56kyx5 e1tk4kwz5"]').text
                except NoSuchElementException:
                    location = ''

                try:
                    job_title = driver.find_element(
                        by="xpath", value='.//div[@class="css-1vg6q84 e1tk4kwz4"]').text
                except NoSuchElementException:
                    job_title = ''

                try:
                    salary = driver.find_element(
                        by="xpath", value='.//div[@class="css-1bluz6i e2u4hf13"]').text
                except NoSuchElementException:
                    salary = ''

                try:
                    salary_range_list = driver.find_elements(
                        by="xpath", value='.//span[@class="css-16uanij e1wijj242"]')
                    salary_range = salary_range_list[-1].text
                except NoSuchElementException:
                    salary_range = ''

                try:
                    company_overview_list = driver.find_elements(
                        by="xpath", value='.//span[@class="css-i9gxme e1pvx6aw2"]')

                    size = try_index(company_overview_list, 0)
                    founded = try_index(company_overview_list, 1)
                    type_of_ownership = try_index(company_overview_list, 2)
                    industry = try_index(company_overview_list, 3)
                    sector = try_index(company_overview_list, 4)
                    revenue = try_index(company_overview_list, 5)

                except NoSuchElementException:
                    size = ''
                    founded = ''
                    type_of_ownership = ''
                    industry = ''
                    sector = ''
                    revenue = ''

                collected_successfully = True

            jobs.append({
                "company_name": company_name,  # .split("\n", 1)[0],
                "location": location,
                "job_title": job_title,
                "salary": salary,
                "salary_range": salary_range,
                "size": size,
                "founded": founded,
                "type_of_ownership": type_of_ownership,
                "industry": industry,
                "sector": sector,
                "revenue": revenue
            })

         #Clicking on the "next page" button
        try:
            driver.find_element(
                by="xpath", value='.//button[@class="nextButton css-1hq9k8 e13qs2071"]').click()
            time.sleep(10)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)
