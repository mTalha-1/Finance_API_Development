from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

def webdriver_connection():
    '''
    Keep your chromedriver file path in project folder and can manully change executable path,
    according to your chromedriver file path.
    '''
    try:
        service =   Service(executable_path = "/chromedriver")
        driver = webdriver.Chrome(service=service)
    except Exception as e:
        print(e)
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
        print(e)

def Scraping_Data():
    driver = webdriver_connection()
    main_site_opening(driver=driver)

    xpaths = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td/a'
    Synbol = driver.find_elements(by='xpath',value= xpaths)

    name_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[2]'
    name = driver.find_elements(by='xpath',value=name_xpath)

    L_Price_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[3]'
    Last_Price = driver.find_elements(by='xpath',value=L_Price_xpath)

    change_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[4]/span'
    change = driver.find_elements(by='xpath',value=change_xpath)

    per_change_xpath = '//*[@id="lookup-page"]/section/div/div/div/table/tbody/tr/td[5]/span'
    per_change = driver.find_elements(by='xpath',value=per_change_xpath)

    for s,n,l,c,p in zip(Synbol,name,Last_Price,change,per_change):

        print(s.text)
        print(s.get_attribute('href'))
        print(n.text)
        print(l.text)
        print(c.text)
        print(p.text)
    driver.close()

if __name__ == '__main__':
    Scraping_Data()