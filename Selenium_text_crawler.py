from bs4 import BeautifulSoup
from selenium import webdriver
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
import json
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver import Chrome


url = "https://www.diginex-solutions.com/"
internal_urls = set()


#domain name with urllib module, initalizing session with requests_html to prep for rendering
domain_name = urlparse(url).netloc
session = HTMLSession()
resp = session.get(url)

# Render JavaScript if found
try:
    response.html.render()
except:
    pass


soup = BeautifulSoup(resp.html.html, 'html.parser')

all_links = soup.find_all('a')
for link in all_links:
    try:
        # what will become a relative link
        href = link.attrs.get('href')
        if href is None or href == '' :
            continue
        
        # join URL if it is relative
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        # Clean-out url & leave 3 first essential components --> Scheme, netloc, path 
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        # Compares to see if domain name == (Netloc) / exists in the newly formed href above , if yes add to internal_urls set
        if domain_name in href:
            internal_urls.add(href)
    except:
        print('critical error')
    

print(internal_urls)

webdriver = 'C:\\Users\karim\projects\selenium\chromedriver.exe'
driver = Chrome(webdriver)
page = 0

for site in internal_urls:
    driver.get(site)
    time.sleep(2)
    item = dict()
    page += 1
    item['url'] = driver.current_url
    item['body'] = driver.find_element_by_xpath("//body/descendant-or-self::*[not(ancestor-or-self::script | ancestor-or-self::style | ancestor-or-self::a | ancestor-or-self::noscript)]").get_attribute("innerText").strip().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

    domain_name = urlparse(site).netloc.split('.')

    print(item)
    print('Page # {}'.format(page))
    # print(domain_name[1])


    with open(f'{domain_name[1]}_AllText.txt', 'a', encoding='utf8') as json_file:
            json.dump(item, json_file, ensure_ascii = False)

driver.close()
driver.quit()

