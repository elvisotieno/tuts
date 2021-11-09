import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


# Webscrape oie immediate-notifications-in-africa
# get the url to return all diseases, from which we extract all the links to individual diseases
# we can now source all the information we want
# To avoid being blocked we obtain user agent the resembles modern browsers from: 'WhatIsMyBrowser.com'
PATH = 'C:\Program Files (x86)\chromedriver.exe'
base_url = 'https://rr-africa.oie.int/en/immediate-notifications-in-africa/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


def rendering(url):
    service = Service(PATH)
    driver = webdriver.Chrome(service=service)  # run ChromeDriver
    driver.get(url)  # load the web page from the URL
    time.sleep(3)  # wait for the web page to load
    render = driver.page_source  # get the page source HTML
    driver.quit()  # quit ChromeDriver
    return render  # return the page source HTML


def get_diseases():

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


def get_specific_details():
    #test_link = 'https://wahis.oie.int/#/report-info?reportId=30451'
    for link in get_diseases():
        disease_page = rendering(link)
        disease_page_soup = BeautifulSoup(disease_page, 'lxml')
        soup_div = disease_page_soup.find('div', class_="report-desc")
        disease_country= soup_div.text.split(',')
        region = disease_country[-1].strip()
        raw_disease = disease_country[0]
        disease = raw_disease.replace('(Inf. with)','').strip()

        status_div = disease_page_soup.find_all('div', class_="reporter-summary-data-val")
        status_section =status_div[-2]
        uncleaned_status = status_section.find('span', class_='txt')
        status = uncleaned_status.text.strip()

        date_div = disease_page_soup.find_all('div', class_="summary-bottom-detail")[1]
        confirmed_on = date_div.find('span', class_='detail').text.strip()

        causal_agent = date_div.find_all('span')[-1].text.strip()

        treatment_div =disease_page_soup.find_all('div', class_="summary-bottom-detail")[-15]
        treatment_measure = treatment_div.find('span', class_="detail").text.strip()

        disease_outbreak ={
           'area': region,
           'name': disease,
           'status': status,
           'date_confirmed': confirmed_on,
           'causes': causal_agent,
           'treatment': treatment_measure
        }

        print(disease_outbreak)

get_specific_details()
