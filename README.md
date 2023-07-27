
# Finance_API_Development

In that project, I build an REST API that will fetch data (By Scraping) from https://finance.yahoo.com/lookup site and then store it into a database. You can use different CRUD operation for updating, adding, modifying, and deleting data into a database.



## For Running Project

* First create virtual environment in your directory location in which you want to run a program:
```
python -m venv env_name
```
* After creating virtual environment, you have to activate virtual environment:
    - For windows:
    ```
    env_name\scripts\activate.bat
    ```
    - For Linux|macOS:
    ```
    source env_name/bin/activate
    ```
* After creating virtual environment, clone my github repository into the folder in which you created virtual environment.
* The repository contains **chromedriver.exe** for **Windows**, make sure that you save that file at the location where you saved the project file. If you have another OS and version of the Chrome browser, then install **chromedriver** from this [page](https://chromedriver.chromium.org/downloads).
* The repository contain **requirements.txt** file, install all necessary packages from **requirements.txt** file, for that use following command:
```
pip install -r requirements.txt
```

* You should have also mySQL database management system in your system, and creat database using following query:
```
CREATE DATABASE database_name
```
* After creating database change the mySQL connection details manually in the **Finance_API.py** script.

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@host/database name'
```

Now, you can run the project and enjoy scraping process.

## Features

- Scrap data of **Trending Tickers** from https://finance.yahoo.com/lookup.
- Store Data into MySQL Database.
- Save basic Information, Errors, Warnings and Criticle Errors in log file. 
- It supports different CRUD operations, you can fetch, get, modify, update, add and delete data from database using API's endpoints.


## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://www.novypro.com/profile_projects/m-talhaasif-shazad)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammadtalha0a1/)

