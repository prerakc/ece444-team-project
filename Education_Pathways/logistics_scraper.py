from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def find_prof(course_name: str) -> str:
    """
    Scrapes for Professor names from the UofT Hub website.
    For now, only returns the first professor name. (Commented code returns entire list of professors)
    """
    # prof_names = []
    prof = "N/A"
    URL = "https://uofthub.ca/course/" + course_name
    print("Scraping: ", URL)
    DRIVER_PATH = "resources/chromedriver"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH) 
    driver.get(URL)
    time.sleep(1) # wait for content to fully load
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    sections = soup.find("div", class_="container").find_all("p")
    for section in sections:
        if section.get_text()=="Professors":
            prof_section = section.parent.find("div", class_="v-list-item__title text-h7 font-weight-medium")
            if prof_section:
                prof = prof_section.find("p").get_text().split("(")[0]
    driver.quit()
    return prof

def find_hours(course_name: str) -> str:
    """
    Scrapes for course hours from Engineering Faculty website.
    """
    hours = "N/A"
    URL = "https://engineering.calendar.utoronto.ca/course/" + course_name.lower()
    print("Scraping: ", URL)
    DRIVER_PATH = "resources/chromedriver"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH) 
    driver.get(URL)
    time.sleep(1) # wait for content to fully load
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    block_field = soup.find(id="block-apsc-content")
    if block_field:
        hours_field = block_field.find("div", class_="field field--name-field-hours field--type-string field--label-inline clearfix")
        if hours_field:
            hours = hours_field.find("div", class_="field__item").get_text()
    return hours

def clean_term(string: str) -> list:
    """
    Cleans up the Term column from courses.csv (from courses.csv.old)
    """
    out = string.replace("[", "").replace("]", "").replace("' '", "/").strip("' ")
    return out

courses_df = pd.read_csv("resources/courses.csv.orig", index_col=0)

print("---start prof scraping---")
courses_df['Professors'] = courses_df['Code'].apply(lambda x: find_prof(x[:6]).strip())
print("---done prof scraping---")

print("---start hours scraping---")
courses_df['Hours'] = courses_df['Code'].apply(lambda x: find_hours(x))
print("---done hours scraping---")

print("---start term cleaning---")
courses_df.head()['Term'] = courses_df.head()['Term'].apply(clean_term)
courses_df['Term'] = courses_df['Term'].apply(clean_term)
print("---done term cleaning---")

courses_df.to_csv("resources/courses_v3.csv", sep=",", header=True, index_label="")
print("---done making final csv---")

print(courses_df.head()['Term'])