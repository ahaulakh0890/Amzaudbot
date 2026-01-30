from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://www.audible.com/charts/best")

book_titles = []
page_no = 1


while True:
    print(f"Scraping page {page_no}...")

    products = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "li.bc-list-item")
        )
    )

    # scrape titles
    for p in products:
        try:
            title = p.find_element(By.CSS_SELECTOR, "h3 a").text.strip()
            book_titles.append(title)
        except:
            pass

    # 🔥 FIXED SELECTOR HERE
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "span.nextButton > a")

        # click using JS
        driver.execute_script("arguments[0].click();", next_btn)

        wait.until(EC.staleness_of(products[0]))

        page_no += 1

    except:
        print("No more pages found. Stopping...")
        break


driver.quit()

book_titles = list(dict.fromkeys(book_titles))

pd.DataFrame({"Title": book_titles}).to_csv(
    "audible_books_allpages.csv",
    index=False
)

print(f"\n✅ Saved {len(book_titles)} books")
