from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from random import randrange

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(5)
action = ActionChains(driver)
wait = WebDriverWait(driver, 10)
driver.get('https://www.google.com')

search_field = wait.until(
    EC.visibility_of_element_located((By.XPATH, '//input[@name="q"]'))
)

assert 'Поиск' in driver.page_source

input_word = 'Совкомбанк'

search_field.send_keys(input_word)

search_listbox = wait.until(
    EC.visibility_of_element_located((By.XPATH, '//ul[@role="listbox"]'))
)

assert search_listbox.get_attribute('role') == 'listbox'

search_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'sb43')]/..//div[@class='wM6W7d']/span")
elem_list = []
for elem in search_elements:
    elem_list.append(elem.text)

assert 'совкомбанк' in ' '.join(elem_list).split()

search_btn = driver.find_element(By.CSS_SELECTOR, "input[name='btnK']")
i = randrange(2)
if i == 0:
    action.send_keys(Keys.ENTER).perform()
else:
    search_btn.click()

assert 'Результаты поиска' in driver.page_source

search_results = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/a")
search_results_lst = []
for search in search_results[:5]:
    search_results_lst.append(search.get_attribute("host"))

assert 'sovcombank.ru' in search_results_lst




driver.close()
