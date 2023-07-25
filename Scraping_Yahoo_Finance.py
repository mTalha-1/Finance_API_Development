from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

import logging
import mysql.connector

logging.basicConfig(filename='log.txt', filemode='w',level=logging.DEBUG, format= '%(asctime)s - %(levelname)s - %(message)s - %(lineno)d')

def connection_database(host,user,password,database):
    try:
        conn = mysql.connector.connect(
                host= host,
                user= user,     
                password= password, 
                database= database 
            )
    except Exception as e:
        logging.critical(e)
    else:
        logging.info('Building Database Connection')
        return conn

def Table_creation(connection,database):
    conn = connection
    cursor = conn.cursor()
    table_name = "Finance_Data"

# MySQL query that give result if table exist
    table_exists_query = """
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = '{database}'
        AND table_name = '{table}'
    """.format(database= database, table=table_name)

    cursor.execute(table_exists_query)
    table_exists = cursor.fetchone()[0]

# Checking Table exist or not
    if table_exists:
        # Table exists, so delete it
        delete_table_query = "DROP TABLE {table}".format(table=table_name)
        cursor.execute(delete_table_query)
        logging.info("Table deleted successfully.")
    else:
        logging.info("Table does not exist.")

# MySQL query for creating table
    create_table_query = """
    CREATE TABLE {table} (
        Id INT AUTO_INCREMENT PRIMARY KEY,
        Symbol VARCHAR(50),
        Name VARCHAR(200),
        URL VARCHAR(500),
        Last_Price VARCHAR(50),
        Change_ VARCHAR(50),
        Percentage_Change VARCHAR(50)
    );
    """.format(table=table_name)

    # Execute the table creation query
    try:
        cursor.execute(create_table_query)
    except Exception as e:
        logging.error(e)
    else:
        logging.info("Table created successfully.")

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

def Scraping_Data(connection):

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

    conn = connection
    cursor = conn.cursor()
    try:  
        for i,(symbol,name,last_price,change,per_change) in enumerate(zip(Symbols,names,Last_Prices,changes,per_changes)):
            print('Inserting row: ',i+1)
            insert_query = f"INSERT INTO Finance_Data (Symbol, Name, URL, Last_Price, Change_, Percentage_Change) VALUES (%s,%s,%s,%s,%s,%s)"
            data = (symbol.text, name.text, symbol.get_attribute('href'), last_price.text, change.text,per_change.text)
            cursor.execute(insert_query,data)
            conn.commit()
    except Exception as e:
        logging.critical(e)
    driver.close()
    conn.close()

if __name__ == '__main__':
    
    print("\nGive following information to build MySQL connection.")
    Host = input("Enter your host.\n")
    User = input("Enter your MySQL username.\n")
    Password = input("Enter your MySQL password.\n")
    Database =  input("Enter your MySQL database name.\n")

    conn = connection_database(Host,User,Password,Database)
    Table_creation(conn,Database)
    Scraping_Data(conn)