# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python web scraping project that extracts book data from Audible using Selenium with headless Chrome. There are two scripts:

- `amzbotpagin.py` — Scrapes Audible best-sellers with pagination (portable, works on Linux)
- `amzbot.py` — Scrapes Audible search page (has hardcoded Windows ChromeDriver path; not portable as-is)

### Running the scripts

```bash
python3 amzbotpagin.py   # works out of the box on Cloud Agent VMs
```

Note: `amzbot.py` has a hardcoded Windows path for ChromeDriver (`C:/Users/amjad/Downloads/...`). To run it on Linux, you'd need to remove the `Service` line and use `webdriver.Chrome(options=options)` like `amzbotpagin.py` does.

### Key gotchas

- Chrome and Selenium Manager (built into selenium 4.6+) handle ChromeDriver download automatically — no manual chromedriver install needed.
- The scripts require internet access to reach `audible.com`.
- Audible may block or throttle repeated requests; if scraping fails with timeouts, wait and retry.
- The `--no-sandbox` and `--disable-dev-shm-usage` Chrome flags are needed in containerized environments but `amzbotpagin.py` does not include them. If you get Chrome crashes, add those flags to the Options.
- There are no automated tests, linting, or build steps in this repo. Validation is done by running the scripts and checking the CSV output.

### Dependencies

Install with: `pip3 install -r requirements.txt`
