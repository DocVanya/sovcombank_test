from random import randrange

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

service = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.implicitly_wait(10)
action = ActionChains(driver)
wait = WebDriverWait(driver, 10)

# Сценарий 1: Поиск в Гугл

# 1. Зайти на google.com
driver.get('https://www.google.com')

# 2. Проверить наличие поля поиска
search_field = wait.until(
    EC.visibility_of_element_located((By.XPATH, '//input[@name="q"]'))
)

assert 'Поиск' in driver.page_source

# 3. Ввести в поиск «Совкомбанк»
input_word = 'Совкомбанк'
search_field.send_keys(input_word)

# 4. Проверить, что появилась таблица с подсказками
search_listbox = wait.until(
    EC.visibility_of_element_located((By.XPATH, '//ul[@role="listbox"]'))
)

assert search_listbox.get_attribute('role') == 'listbox'

# 5. Проверить, что в вариантах подсказок есть слово «совкомбанк» (не в рекламном блоке)
search_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'sb43')]/..//div[@class='wM6W7d']/span")
elem_list = []
for elem in search_elements:
    elem_list.append(elem.text)

assert 'совкомбанк' in ' '.join(elem_list).split()

# 6. Выполнить поиск по ключевому слову «Совкомбанк». «Выполнить поиск» возможно несколькими способами:
# A. Нажать ENTER
# B. Нажать кнопку «Поиск в Google»
search_btn = driver.find_element(By.CSS_SELECTOR, "input[name='btnK']")
i = randrange(2)
if i == 0:
    action.send_keys(Keys.ENTER).perform()
else:
    search_btn.click()

# 7. Поверить:
# a. Появляется таблица результатов поиска
assert 'Результаты поиска' in driver.page_source

search_results = wait.until(
    EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='yuRUbf']/a"))
)

# b. В первых 5 результатах поиска есть ссылка на sovcombank.ru
search_results_lst = []
for search in search_results[:5]:
    search_results_lst.append(search.get_attribute("host"))

assert 'sovcombank.ru' in search_results_lst

# Сценарий 2: Картинки в Гугл
# 1. Выполнить все действия из Сценария 1
# 2. Проверить, что кнопка «Картинки» присутствует на странице
pictures_btn = driver.find_element(By.XPATH, '//a[contains(text(),"Картинки")]')

assert "Картинки" in pictures_btn.text

# 3. Нажать на кнопку «Картинки»
pictures_btn.click()

# 4. Открыть вторую картинку, проверить что открылась
pictures = driver.find_elements(By.XPATH, "//div[contains(@jsmodel, 'Whqy4b')]")
pictures[1].click()

pictures_text = driver.find_elements(By.XPATH, "//div[contains(@jsmodel, 'Whqy4b')]/h3")
pict_text_1 = pictures_text[1].text
open_pict_text = driver.find_elements(By.XPATH, '//div[@jsname="QH4tvd"]//h1')[1].text

assert pict_text_1 == open_pict_text

# 5. При нажатии кнопки «Вперед» картинка изменилась
next_btn = driver.find_elements(By.XPATH, "//a[@jsname='OCpkoe']")[1]
next_btn.click()
open_pict_text = driver.find_elements(By.XPATH, '//div[@jsname="QH4tvd"]//h1')[1].text

assert pict_text_1 != open_pict_text

# 6. Нажать кнопку «Назад»
prev_btn = driver.find_elements(By.XPATH, "//a[@jsname='ttdpI']")[1]
prev_btn.click()

open_pict_text = driver.find_elements(By.XPATH, '//div[@jsname="QH4tvd"]//h1')[1].text

# 7. Проверить, что картинка изменилась на картинку из шага 4
assert pict_text_1 == open_pict_text

driver.close()
