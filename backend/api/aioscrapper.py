import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import aiohttp
import asyncio

# Webscrape oie immediate-notifications-in-africa
# get the url to return all diseases, from which we extract all the links to individual diseases
# we can now source all the information we want
# To avoid being blocked we obtain user agent the resembles modern browsers from: 'WhatIsMyBrowser.com'
PATH = 'C:\Program Files (x86)\chromedriver.exe'
base_url = 'https://rr-africa.oie.int/en/immediate-notifications-in-africa/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

def get_diseases_links(base_url):

    raw_data= requests.get(base_url)
    soup = BeautifulSoup(raw_data.content, 'html.parser')
    diseases_list=soup.find_all('p')

    diseases_links = []
    for disease in diseases_list:
        for link in disease.find_all('a', href=True):
            if len(link['href'])==50:
                diseases_links.append(link['href'])
    diseases_links.pop()
    return diseases_links


def rendering_page(urls):
    pages=[]
    for url in urls:
        service = Service(PATH)
        driver = webdriver.Chrome(service=service)  # run ChromeDriver
        driver.get(url)  # load the web page from the URL
        time.sleep(3)  # wait for the web page to load
        page_rendered = driver.page_source  # get the page source HTML
        pages.append(page_rendered)
        driver.close()
    driver.quit()  # quit ChromeDriver
    return pages  # return the page source HTML



def get_specific_details(html_pages):
    list_of_diseases=[]
    for page in html_pages:
        soup = BeautifulSoup(page, 'lxml')
        soup_div = soup.find('div', class_="report-desc")
        disease_country= soup_div.text.split(',')
        region = disease_country[-1].strip()
        raw_disease = disease_country[0]
        disease = raw_disease.replace('(Inf. with)','').strip()

        status_div = soup.find_all('div', class_="reporter-summary-data-val")
        status_section =status_div[-2]
        uncleaned_status = status_section.find('span', class_='txt')
        status = uncleaned_status.text.strip()

        date_div = soup.find_all('div', class_="summary-bottom-detail")[1]
        confirmed_on = date_div.find('span', class_='detail').text.strip()

        causal_agent = date_div.find_all('span')[-1].text.strip()

        treatment_div = soup.find_all('div', class_="summary-bottom-detail")[-15]
        treatment_measure = treatment_div.find('span', class_="detail").text.strip()

        disease_outbreak ={
           "name": disease,
           "area": region,
           "status": status,
           "date_confirmed": confirmed_on,
           "causes": causal_agent,
           "treatment": treatment_measure
        }
        # to ensure we don't take in null values
        if len(disease_outbreak['area'])>1:
            list_of_diseases.append(disease_outbreak)


    print(list_of_diseases)

urls = get_diseases_links(base_url)
html_pages= rendering_page(urls)
get_specific_details(html_pages)

