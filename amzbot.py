from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = Options()

# 🔥 NEW HEADLESS MODE
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

path = r"C:/Users/amjad/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=path)

# ✅ OPTIONS YAHAN DENI HOTI HAIN
driver = webdriver.Chrome(service=service, options=options)

web = "https://www.audible.com/search"
driver.get(web)

wait = WebDriverWait(driver, 20)

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
        pass

book_titles = list(dict.fromkeys(book_titles))

driver.quit()

df_books = pd.DataFrame({'Title': book_titles})
df_books.to_csv('audible_books_headless.csv', index=False, encoding='utf-8')

print("Saved", len(book_titles), "books")
