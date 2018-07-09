from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome("C:/Users/atrivedy/Documents/Visualilzation/chromedriver.exe")
driver.get('https://servicecafe.service-now.com/')
user = 'mc55804'
passwd = 'Bigmac09'

elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_UsernameRegular")
elem.send_keys(user)

elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_PasswordTextBoxRegular")
elem.send_keys(passwd)

elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnSubmit")
elem.click()

driver.get('https://servicecafe.service-now.com/incident_list.do?sysparm_query=active=true&sysparm_order=opened_at&sysparm_order_direction=desc')


elem = driver.find_element_by_id('incident_filter_toggle_image')
elem.click()


delay = 10 # seconds
myElem = driver.find_element_by_class_name(".btn.btn-default")

#myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, '.btn.btn-default')))
myElem.click()
'''
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "//*[@id='QUERYPART95a926095a9b7095a570095aec4095ad']/tr[4]/td/table/tbody/tr/td[4]/button")))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
'''
#select = Select(driver.find_element_by_id('select2-chosen-4'))
#select = Select(driver.find_element_by_id('select2-result-label-641'))

#select.select_by_visible_text('Assignment group')
