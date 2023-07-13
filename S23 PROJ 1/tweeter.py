import time
import datetime as dt
from selenium import webdriver

#PROGRAM DOES NOT REGARDLESS OF TARGETED URL
driver = webdriver.Chrome()
driver.get("https://twitter.com/i/flow/login?redirect_after_login=%2F")
"""FIX FROM STACKEXCHANGE"""
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options) #EXECPATH REMOVED AS PER UPDATED COMMENTS


"""proof of execution"""
def proof():
    file = open(r"C:\Users\XXXXX\Desktop\python projects\S23 PROJ 1\log.txt", "a") #replace with your own path
    file.write(f"{dt.datetime.now()} - The script ran \n")

#proof()