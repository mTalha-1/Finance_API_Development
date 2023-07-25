from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import logging

logging.basicConfig(filename='app.log', filemode='w',level=logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')

def webdriver_connection():
    '''
    Keep your chromedriver file path in project folder and can manully change executable path,
    according to your chromedriver file path.
    '''
    try:
        service =   Service(executable_path = "/chromedriver")
        driver = webdriver.Chrome(service=service)
    except Exception as e:
        logging.critical(e)
    else:
        driver.maximize_window()
    return driver

def main_site_opening(driver):
    '''This function will request driver for opening website you want to scrap'''
    website = "https://finance.yahoo.com/lookup"
    try:
        driver.set_page_load_timeout(100)
        driver.implicitly_wait(50)
        driver.get(website)
    except Exception as e:
        logging.critical(e)

def Scraping_Data():

    driver = webdriver_connection()
    main_site_opening(driver=driver)

    try:
        xpaths = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td/a'
        Symbols = driver.find_elements(by='xpath',value= xpaths)
    except NoSuchElementException as e:
        logging.debug(e)

    try:
        name_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[2]'
        names = driver.find_elements(by='xpath',value=name_xpath)
    except NoSuchElementException as e:
        logging.debug(e)

    try:
        L_Price_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[3]'
        Last_Prices = driver.find_elements(by='xpath',value=L_Price_xpath)
    except NoSuchElementException as e:
        logging.debug(e)

    try:
        change_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[4]/span'
        changes = driver.find_elements(by='xpath',value=change_xpath)
    except NoSuchElementException as e:
        logging.debug(e)

    try:
        per_change_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[5]/span'
        per_changes = driver.find_elements(by='xpath',value=per_change_xpath)
    except NoSuchElementException as e:
        logging.debug(e)

    data = []
    try:  
        for i,(symbol,name,last_price,change,per_change) in enumerate(zip(Symbols,names,Last_Prices,changes,per_changes)):
            print('Inserting row: ',i+1)

            data.append({
                'Symbol': symbol.text,
                'Name': name.text,
                'URL':  symbol.get_attribute('href'),
                'Last_Price': last_price.text,
                'Change_': change.text,
                'Percentage_Change': per_change.text
            })
    except Exception as e:
        logging.critical(e)
    
    driver.close()
    return data

if __name__ == '__main__':
    
    Scraping_Data()