import re
import time
import pymongo
from selenium import webdriver
from urllib.request import Request, urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Diasable page images
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options,executable_path="./chromedriver.exe")

# DB Connection
myclient_local = pymongo.MongoClient("mongodb://" + "localhost" + ":" + "27017")
mydb_local = myclient_local["menufacturerMakes"]
mycol_local = mydb_local["BMW"]

# Websites URL
# driver.get('https://usedcars.bmw.co.uk/result/?size=50&source=home')

driver.maximize_window()


# Scraping the data
def scrape():
    i=1

    while i<=50:

        # if i == 2:
        #     i+=1
        print("Car " + str(i))
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div['+str(i)+']/div[1]/div[2]/div[1]/p')))
        title = driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/p').text
        model = driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/h2/a').text
        make = title.split(' ')[0]
        range = " ".join(title.split(' ')[1:])
        price =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[3]/div/div[1]/span').text.split('\n')[0]
        mileage =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/ul/li[5]').text
        fuel =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/ul/li[2]/span').text
        transmission =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/ul/li[1]').text
        address =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[2]/ul/li[1]/a/span').text
        regNumber =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/ul/li[4]/span').text
        registerDate =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[2]/div[1]/ul/li[3]/span').text

        link = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "uvl-c-advert--results")]['+str(i)+']')))
        driver.execute_script("arguments[0].scrollIntoView();", link)
        time.sleep(0.2)
        try:
            image =  driver.find_element_by_xpath('//div['+str(i)+']/div[1]/div[1]/div/div[1]/a/img')
            imageURL = image.get_attribute("src")
        except:
            imageURL = ""

        my_details ={
                    'title': title,
                    'model': model,
                    'make': make,
                    'range': range,
                    'price': price,
                    'mileage': mileage,
                    'fuel': fuel,
                    'transmission': transmission,
                    'address': address,
                    'regNumber': regNumber,
                    'registerDate': registerDate,
                    'imageURL': imageURL,
        }
        print(my_details)
        mycol_local.insert_one(my_details)
        i+=1
        
loop = 1
page = 88

while True:
    try:
        print(loop)
        if page == 252:
            break
        # time.sleep(1)
        # https://usedcars.bmw.co.uk/result/?page=88&size=50&source=home
        driver.get('https://usedcars.bmw.co.uk/result/?page='+str(page)+'&size=50&source=home')
        time.sleep(5)
        scrape()
        page += 1
        loop += 1

    except (TimeoutException, WebDriverException) as e:
        
        print("Last page reached")
        time.sleep(5)
        # scrape()
        False
        break

time.sleep(2)
driver.close()