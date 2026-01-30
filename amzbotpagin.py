from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ---------------------------
# Chrome Options (stable)
# ---------------------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ Let Selenium manage driver automatically (NO Service, NO path)
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 20)

web = "https://www.audible.com/search"
driver.get(web)

# ---------------------------
# Pagination
# ---------------------------

pagination = driver.find_elements(By.XPATH, '//ul[contains(@class, "pagingElements")]') '

pages = pagination.find_elements(By.TAG_NAME, 'li')

last_page = int(pages[-2].text)   # second last is last page number

next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
next_page.click()



# //a[contains(@class, "bc-button-text")]

# ---------------------------
# Wait for products to load
# ---------------------------
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//li[contains(@class,"bc-list-item")]')
    )
)

time.sleep(3)  # extra load safety (Audible lazy loads)

products = driver.find_elements(
    By.XPATH, '//li[contains(@class,"bc-list-item")]'
)

book_titles = []

for product in products:
    try:
        title = product.find_element(By.XPATH, './/h3//a').text.strip()
        if title:
            book_titles.append(title)
    except:
        continue

# remove duplicates
book_titles = list(dict.fromkeys(book_titles))

driver.quit()

# ---------------------------
# Save CSV
# ---------------------------
df = pd.DataFrame({'Title': book_titles})
df.to_csv('audible_books_headless.csv1', index=False, encoding='utf-8')

print(f"Saved {len(book_titles)} books")
