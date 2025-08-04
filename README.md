# 🧰 Naukri Job Scraper

A Python-based scraper that extracts job listings from [Naukri.com](https://www.naukri.com) using Selenium and BeautifulSoup. This tool automates job data collection (title, company, location, experience, salary, etc.) and exports it to a structured Excel spreadsheet.

---

## 📌 Features

- Scrapes job listings from multiple pages  
- Extracts key fields: title, company, experience, salary, location, and more  
- Handles missing data gracefully  
- Saves output to Excel (`.xlsx`) using `openpyxl`    
- Minimal, clean, and production-ready Python code

---

## 🧱 Built With

- [Selenium](https://pypi.org/project/selenium/) – for rendering dynamic content
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) – for HTML parsing
- [pandas](https://pypi.org/project/pandas/) – for data handling
- [openpyxl](https://pypi.org/project/openpyxl/) – for writing to Excel

---

## 💻 Requirements

- Python 3.7+
- Google Chrome installed
- Matching [ChromeDriver](https://chromedriver.chromium.org/downloads) in your PATH

### 📦 Install Dependencies

```bash
pip install selenium beautifulsoup4 pandas openpyxl


### How to run 

```bash 
python naukri_scraper.py




### 👨‍💻 Author
Made with ❤️ by Joel Biju
Pull requests welcome!