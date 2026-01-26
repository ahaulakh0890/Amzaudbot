from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

web = "https://www.audible.com/search"

path = r"C:/Users/amjad/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

service = Service(path)
driver = webdriver.Chrome(service=service)

driver.get(web)
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# ✅ ONLY real product cards
products = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//li[contains(@class,"bc-list-item")]')
    )
)

book_titles = []

for product in products:
    try:
        title = product.find_element(By.XPATH, './/h3//a').text.strip()
        book_titles.append(title)
    except:
        pass   # skip ads / broken cards

# ✅ yahan deduplicate karo
book_titles = list(dict.fromkeys(book_titles))

driver.quit()

df_books = pd.DataFrame({'Title': book_titles})
df_books.to_csv('audible_books.csv', index=False, encoding='utf-8')

print("Saved", len(book_titles), "books")
