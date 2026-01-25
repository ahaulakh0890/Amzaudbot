from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

web = "https://www.audible.com/search"

path = "C:/Users/amjad/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get(web)
driver.maximize_window()

container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')

products = container.find_elements(By.XPATH, './/li')

book_titles = []

for i, product in enumerate(products):
        book_titles.append(product.find_element(By.XPATH, './/h3[contains(@class,"bc-heading")]//a'))
driver.quit()

df_books = pd.DataFrame({'Title': book_titles})
df_books.to_csv('audible_books.csv', index=False) 

  




   