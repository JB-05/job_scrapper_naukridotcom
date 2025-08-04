import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class NaukriJobScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.jobs = []
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_page_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'srp-jobtuple-wrapper'))
            )
            time.sleep(2)
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            logging.error(f"Error loading page {url}: {e}")
            return None

    def extract_job_details(self, job_element) -> Dict:
        job_data = {
            'title': None,
            'company': None,
            'location': None,
            'experience': None,
            'salary': None,
            'description': None,
            'posted_date': None,
            'job_link': None
        }

        try:
            title_elem = job_element.find('a', class_='title')
            if title_elem:
                job_data['title'] = title_elem.text.strip()
                job_data['job_link'] = title_elem.get('href')

            company_elem = job_element.find('a', class_='comp-name')
            job_data['company'] = company_elem.text.strip() if company_elem else "Not specified"

            exp_elem = job_element.find('span', class_='expwdth')
            job_data['experience'] = exp_elem.text.strip() if exp_elem else "Not specified"

            sal_elem = job_element.find('span', class_='sal')
            job_data['salary'] = sal_elem.text.strip() if sal_elem else "Not disclosed"

            loc_elem = job_element.find('span', class_='loc')
            job_data['location'] = loc_elem.text.strip() if loc_elem else "Not specified"

            desc_elem = job_element.find('span', class_='job-desc')
            job_data['description'] = desc_elem.text.strip() if desc_elem else "Not available"

            posted_elem = job_element.find('span', class_='job-post-day')
            job_data['posted_date'] = posted_elem.text.strip() if posted_elem else "Not specified"

        except Exception as e:
            logging.warning(f"Error extracting job: {e}")
        return job_data

    def scrape_jobs(self, max_pages: int = 5) -> List[Dict]:
        start = 0
        page = 1
        while page <= max_pages:
            logging.info(f"Scraping page {page}...")
            current_url = f"{self.base_url}?start={start}"
            soup = self.get_page_soup(current_url)
            if not soup:
                break

            job_elements = soup.find_all('div', class_='srp-jobtuple-wrapper')
            if not job_elements:
                logging.info("No job listings found.")
                break

            for job_el in job_elements:
                job = self.extract_job_details(job_el)
                if job['title']:
                    self.jobs.append(job)

            start += 20  
            page += 1
            time.sleep(2)

        return self.jobs

    def save_to_excel(self, filename: str):
        df = pd.DataFrame(self.jobs)

        wb = Workbook()
        ws = wb.active
        ws.title = "Job Postings"

        # Add headers with bold font
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                if r_idx == 1:
                    cell.font = Font(bold=True)

        wb.save(filename)
        logging.info(f"Saved {len(self.jobs)} jobs to {filename}")

    def close(self):
        self.driver.quit()

def main():
    # Example URL for software jobs
    career_page_url = "https://www.naukri.com/software-jobs"
    scraper = NaukriJobScraper(career_page_url)

    try:
        scraper.scrape_jobs(max_pages=5)
        scraper.save_to_excel("naukri_jobs.xlsx")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
