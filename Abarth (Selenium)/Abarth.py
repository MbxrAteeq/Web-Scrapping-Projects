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
driver = webdriver.Chrome(options=options,executable_path="./chromedriver.exe")

# DB Connection
myclient_local = pymongo.MongoClient("mongodb://" + "localhost" + ":" + "27017")
mydb_local = myclient_local["menufacturerMakes"]
mycol_local = mydb_local["abarth"]

# Websites URL
driver.get('https://usedabarth.co.uk/search/?adobe_mc_ref=')

# Iframe Accesding
time.sleep(5)
driver.switch_to.frame(driver.find_element_by_xpath("/html/body/iframe[2]"))
#Clicking the accept cookies Button
accept = driver.find_element(By.XPATH, '(//*[@id="acceptAllBtn"])')
accept.click()
driver.switch_to.parent_frame()


# Scraping the data
def scrape():

    i=1

    while i<=12:

        print("Car " + str(i))
        title = driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div/div/div/div/div/h3/a').text
        make = title.split(' ')[0]
        model = " ".join(title.split(' ')[2:])
        _range = re.findall("124 Spider|695|595|500", title)[0]
        price = driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div[2]/div/div/div[2]/div/div[1]/div[2]/p').text
        priceSimplified = re.sub('[£,]', '', price)
        mileage = driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div[2]/div/div/div[2]/div/div[1]/div[1]/p[2]').text
        fuel =  driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div[2]/div/div/div[2]/div/div[1]/div[1]/p[3]').text
        transmission =  driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div[2]/div/div/div[2]/div/div[1]/div[1]/p[4]').text
        regNumberAndRegisterDate  = driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div[2]/div/div/div[2]/div/div[1]/div[1]/p[1]').text
        regNumber =  regNumberAndRegisterDate.split(' ')[0]
        try:
            registerDate = regNumberAndRegisterDate.split(' ')[1].strip("()")
        except:
            pass
        image =  driver.find_element_by_xpath('//*[@id="ajax-results"]/div['+str(i)+']/div/div[1]/div/div/a/img')
        imageURL = image.get_attribute("src")
        if imageURL:
            imageURL = imageURL.split('%')[0]
        my_details ={
                    'title': title,
                    'model':model,
                    'make':make,
                    '_range':_range,
                    'price': price,
                    'priceSimplified':priceSimplified,
                    'mileage': mileage,
                    'fuel': fuel,
                    'transmission': transmission,
                    'regNumberAndRegisterDate': regNumberAndRegisterDate,
                    'regNumber': regNumber,
                    'registerDate': registerDate,
                    'imageURL': imageURL,
        }
        print(my_details)
        mycol_local.insert_one(my_details)
        i+=1
        

scrape()
# Handling Next Page
loop = 1
while True:
    try:
        print(loop)
        try:
            next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[3]/div/div/ul/li[2]/a')
        except:
            next_page = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[3]/div/div/ul/li/a')
        next_page.click()
        time.sleep(5)
        scrape()
        loop += 1
        

    except (TimeoutException, WebDriverException) as e:
        
        print("Last page reached")
        time.sleep(5)
        scrape()
        False
        break

time.sleep(2)
driver.close()
