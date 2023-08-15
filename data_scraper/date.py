import html_pyppeteer, detect
from datetime import datetime

'''
instead of datetime, can just use time

date1 = "31/12/2015"
date2 = "01/01/2016"

newdate1 = time.strptime(date1, "%d/%m/%Y")
newdate2 = time.strptime(date2, "%d/%m/%Y")

then <, >
'''


# date.py that will handle checking the dates of the data-string given a tr body, maybe an array the filenames only
# so that the next page can be checked if required, this will hold the current date and the previous date,
# one of the functions will be to see if the given data-string is within the current date
# -> returns true, if data-string is within the current date
# -> returns false, if data-string is before the current date

# function check whether the data-string is within the span of current date

# function that will store the current date by looking at the most recent data string, this will be 
# stored in a GLOBAL VARIABLE
def current_date(tr): # -> tr will be the latest data-string from the most recent html content file
    return            

# function that will compare two data-strings: the left will be checked to see if it is before the one on the right
def check_preceding(check: str, current: str):
    check_dt = datetime("%Y-%m-%d")
    current_dt = datetime("%Y-%m-%d")
    return check_dt < current_dt

def get_day(date):
    return

def get_month(date):
    return

def get_year(date):
    return

def main():
    print("DATETIME")
    return