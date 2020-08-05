import os
import shutil
import csv
import math
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


#VARIABLES
browser = webdriver.Chrome()

short_wait = WebDriverWait(browser,5)

medium_wait = WebDriverWait(browser,10)

long_wait = WebDriverWait(browser, 40)

csv_output = open("scriptsId.csv","w+")

csv_writer = csv.writer(csv_output)

csv_writer.writerow(
        ['ID','Nome Projeto']
    )

browser.get("https://www.google.com/script/start/")

enter_login_screen_button = browser.find_element_by_id("body-button")

ActionChains(browser).click(enter_login_screen_button).perform()

login_id_button = long_wait.until(EC.element_to_be_clickable((By.ID,'identifierId')))

ActionChains(browser).click(login_id_button).perform()

login_id_button.send_keys("") #--> Add your e-mail here

next_button_username = browser.find_element_by_id("identifierNext")

ActionChains(browser).click(next_button_username).perform()

password_field_google = medium_wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@type = 'password']")))

password_field_google.send_keys("") #--> Add your password here

next_button_password = browser.find_element_by_id("passwordNext")

ActionChains(browser).click(next_button_password).perform()

#Brazil portuguese only below, if you're using from other countries update aria-label content 
#or seek for another xPath reference on the DOM
my_projects_button = long_wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@aria-label='Meus projetos']"))) 

ActionChains(browser).click(my_projects_button).perform()

#The class below CAN change, it should be updated when it stops working
projects_id_div = long_wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='f9RONd']")))

SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
test_script_execution = browser.execute_script("console.log('Executing Script');")

#Auto-scrolling is a bit more complicated on this application
#Simply using broser.execute_script(-move down with js-) won't do
#Picking an element and using send_keys(Keys.DOWN) will likely work
#But I didn't had the time to test it out

#This approach just makes the script wait long enough so you can scroll down till all scripts are shown
#If you're likely to keep watching the whole process and are in a hurry, this could be good enough
sleep(60)

projects_id_div = long_wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='f9RONd']")))

array_projects_id = browser.find_elements_by_xpath("//div[@class='f9RONd']")

array_name_projects = browser.find_elements_by_xpath("//div[@class='f9RONd']/div[1]/div[1]/span[1]")

i = 0

for div in array_projects_id:

    script_id = div.get_attribute("data-script-id")

    project_name = array_name_projects[i].text

    csv_writer.writerow(
        [script_id,project_name]
    )

    i += 1

csv_output.close()


