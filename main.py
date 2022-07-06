import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from datetime import date, timedelta

current_date = str(date.today() + timedelta(days=1))

# options fo chromedriver
# only need download chromdriver and place with a script
def get_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--enable-javascropt")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# open full html cod
web_driver = get_chrome()
web_driver.get('https://www.flashscore.ru.com/')
web_driver.find_element(By.XPATH, "//button[contains(@class, 'customCookie__button customCookie__button--accept') and text()='Принять']").click()
sleep(5)
web_driver.find_element(By.XPATH, "//div[contains(@class, 'calendar__navigation calendar__navigation--tomorrow')]").click()
sleep(5)
web_driver.find_element(By.XPATH, "//div[contains(@class, 'filters__text filters__text--default') and text()='Кэфы']").click()
sleep(2)

while True:
    try:
        element = web_driver.find_element(By.XPATH, "//span[@class='event__expanderBlock']/*[name()='svg'][@class='undefined event__expander event__expander--close']")
        WebDriverWait(web_driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//span[@class='event__expanderBlock']/*[name()='svg'][@class='undefined event__expander event__expander--close']"))).click()
        web_driver.execute_script("arguments[0].scrollIntoView()", element)
    except Exception:
        print('Готово для сбора данных')
        break

# we take all info from web
time = web_driver.find_elements(By.XPATH, "//div[contains(@class, 'event__match event__match--')]/child::div[2]")
team1 = web_driver.find_elements(By.XPATH, "//div[@class='event__participant event__participant--home']")
team2 = web_driver.find_elements(By.XPATH, "//div[@class='event__participant event__participant--away']")
kaef1 = web_driver.find_elements(By.XPATH, "//div[contains(@class, 'event__odd--odd1 kx')]")
kaefx = web_driver.find_elements(By.XPATH, "//div[contains(@class, 'event__odd--odd2 kx')]")
kaef2 = web_driver.find_elements(By.XPATH, "//div[contains(@class, 'event__odd--odd3 kx')]")
population_result = []
for i in range(len(kaef2)):
    temporary_data = {
                      'Время': time[i].text,
                      'Команда Home': team1[i].text,
                      'Команда Away': team2[i].text,
                      'Каэф 1': str(kaef1[i].text),
                      'Каэф х': str(kaefx[i].text),
                      'Кафж 2': str(kaef2[i].text),
                     }
    print(temporary_data)
    # create xlsx file and close web driver + stop script
    population_result.append(temporary_data)
    df_data = pd.DataFrame(population_result)
    df_data.to_excel(current_date + ".xlsx", index=False)
print('Данные собраны')
web_driver.quit()
sys.exit()
