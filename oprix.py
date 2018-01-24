from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


query = "https://img0.gaadicdn.com/images/car-images/520x216/Maruti/Maruti-Celerio/047.jpg"

def search(query):
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.get("http://mmr-demo.orpix-inc.com/detection/main/")

    email_field = driver.find_element_by_id("email_input")
    email_field.send_keys("prodigylevan@gmail.com")
    search_field = driver.find_element_by_id("url_input")
    search_field.send_keys(query)

    sleep(3)
    driver.find_element_by_id("process_image").click()
    sleep(8)

    source = driver.page_source
    print(source)
    driver.quit()

    soup = BeautifulSoup(source, "html.parser")
    all_td = soup.find('tr', {'class': 'odd selected'})
    all_td = all_td.find_all('td')
    result = all_td[1].text
    result = result.split(' ')
    ans = {"brand":result[0], "model":result[1], "year" : result[2]}

    return ans

