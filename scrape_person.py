from linkedin_scraper import Person
from selenium import webdriver
driver = webdriver.Chrome()
url = input("login and submit url here: ")
person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", scrape=False, driver=driver)
person.scrape(close_on_complete=False)
