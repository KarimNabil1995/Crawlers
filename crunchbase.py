from selenium import webdriver
from selenium.webdriver import Chrome
import json
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import selenium.common.exceptions as exception
from selenium.common.exceptions import TimeoutException




webdriver = 'C:\\Users\karim\projects\selenium\chromedriver.exe'
driver = Chrome(webdriver)
driver.implicitly_wait(2)

column_names = ['Entity_Name', 'Website']
df = pd.read_excel('test.xlsx', names = column_names)

names = df[0:3].Website.to_list()


url = 'https://google.com'
driver.maximize_window()
driver.get(url)
count = 0

Crunch_links_list = []
names_list = []
all_regions_list = []
Fdates_list = []
employees_list = []
weblinks_list = []
LND_list = []
TW_list = []
oper_stat = []
All_industries_list = []
All_locations_list = []


for name in names:

    # select search box, input the google search and fire up the search
    search_query = driver.find_element_by_name('q')
    search_query.clear()
    search_query.send_keys('site:http://crunchbase.com AND "{}"'.format(name))
    time.sleep(5)

    search_query.send_keys(Keys.RETURN)
    time.sleep(5)

    # Grab the first link from google search results, visit the href
    try:
        link = driver.find_element_by_xpath("//div[@class='g'][1]/div/div/a").get_attribute("href")
        driver.get(link)
    except:
        print('No Crunchbase page found')
        continue

    wait = WebDriverWait(driver, 4)

    try:
        # To close a "save" pop-up that appears everynow and then
        time.sleep(2)
        save_popup = driver.find_element_by_xpath("//button[@class='bb-button _pendo-button-custom _pendo-button']")
        save_popup.click()
        time.sleep(5)
    except NoSuchElementException:
        print('No Save-PopUp')
    
    

    industries_list = []
    locations_list = []
    regions_list = []

    try:
        # Company name, Headquarter region and Location, Foundation Date
        c_name = wait.until(EC.presence_of_element_located((By.XPATH, "//h1/span"))).text

        HQ_regions = driver.find_elements_by_xpath("//span[text()='Regions']/parent::span/parent::span/parent::label-with-info/following::field-formatter[1]/identifier-multi-formatter/span/a")
        for region in HQ_regions:
            regions_list.append(region.text)

        foundation_date = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='component--field-formatter field-type-date_precision ng-star-inserted']"))).text
        locations = driver.find_elements_by_xpath("//span[text()='Headquarters ']/parent::span/parent::label-with-info/following::field-formatter[1]/identifier-multi-formatter/span/a")[:2]
        for location in locations:
            locations_list.append(location.text)


        # Number of Employees, registered industries
        employees = wait.until(EC.presence_of_element_located((By.XPATH, "(//*[contains(@href, 'num')])[1]"))).text
        time.sleep(3)
        industries =  driver.find_elements_by_xpath("//div[@class='mat-chip-list-wrapper']/mat-chip")
        for industry in industries:
            industries_list.append(industry.text)
        

        # Operating website, LinkedIn, Twitter selectors, operating status
        op_website = wait.until(EC.presence_of_element_located((By.XPATH, "(//a[@role='link'])[1]"))).get_attribute('href')
        LinkedIn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='View on LinkedIn']"))).get_attribute('href')
        Twitter = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='View on Twitter']"))).get_attribute('href')

        operating_status = wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Active']"))).text
        time.sleep(3)
    except:
        print('no proper crunchbase profile found')
        pass

    count +=1
    time.sleep(3)

    try:
        print('\n')
        print('Company # {}'.format(count))
        print('Company name is {}'.format(c_name))
        print('HQ region is in {}'.format(regions_list))
        print('HeadQuarter Location is in {}'.format(locations_list))
        print('Company has {} employees'.format(employees))
        print('Company established in {}'.format(foundation_date))
        print('Involved Industries : {}'.format(industries_list))
        print('Active website is: {}'.format(op_website))
        print('Active twitter is: {}'.format(Twitter))
        print('Active LinkedIn is: {}'.format(LinkedIn))
        print('Operating status is {}'.format(operating_status))
        print('Crunchbase url is {}'.format(link))
    except:
        pass

    try:
        Crunch_links_list.append(link)
        names_list.append(c_name)
        all_regions_list.append(regions_list)
        Fdates_list.append(foundation_date)
        All_industries_list.append(industries_list)
        employees_list.append(employees)
        weblinks_list.append(op_website)
        LND_list.append(LinkedIn)
        TW_list.append(Twitter)
        oper_stat.append(operating_status)
        All_locations_list.append(locations_list)
    except:
        print('array lists are not formed')


    driver.back()
    time.sleep(3)

try: 
    df = pd.DataFrame(list(zip(names_list,Crunch_links_list, All_locations_list, all_regions_list, All_industries_list, employees_list, Fdates_list, TW_list, LND_list, weblinks_list, oper_stat)), columns=['Company_Name', 'Crunchbase_Link', 'Headquarter_location', 'Headquarter_region', 'Industries', 'Num_Of_Employees','Foundation_Date', 'Twitter_Handle', 'LinkedIn_Handle', 'Operating_website', 'Operating_status'])

    Crunchbase_data = df.to_csv('Crunchbase_data2.csv', index=False)
except:
    print('Last step not done')


driver.close()



