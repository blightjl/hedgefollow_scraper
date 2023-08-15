import requests, sys, bs4, os
from selenium import webdriver

# approach with requests

target_url = 'https://hedgefollow.com/insider-trading-tracker'

# retrieve the response object through GET
response = requests.get(target_url)

# exit if the webpage is not accessible
# try:
#    response.raise_for_status()
#    print('successfully retreived html')
# except Exception as error:
    # log the failure
#    sys.exit(1)

# save webpage locally
webpage = open('webpage.txt', 'wb')
for chunk in response.iter_content(100000):
   webpage.write(chunk)

# webpage.close()

# check for any changes in the table of stock exchange
# log_path = './dates.txt' 

# print(log_path)

# retreive the current date the source is updated
# current_date = '99/99/9999'

# retreive the last date that was logged from the log file (dates.txt)

with open('./webpage.txt', 'r') as file:
    soup = bs4.BeautifulSoup(file, 'html.parser')

# print(current_date)
try:
    all_trs = soup.find('table', class_='dataTable')
    print('PART 2')
    print(all_trs)
    names = []
    print('PART 3')
    for i in all_trs.find_all('tr'):
        names.append(i.find('td').text.strip())
    print('p3')
except Exception as error:
    print('FAILED')

# with open(log_path, 'r') as file:
#     first_line = file.readline().strip()

# if it exists (for buy + sell)
# function to find greatest change in magnitude

# function to find greatest change in percentage


# function to convert string into integer value for calculation
# ex: 5k -> 5000, 10m -> 10000000, 1.92b -> 1920000000
#
# use selenium for actual tweeting
# use requests for web scraping

# launch firefox and open up the website
# browser = webdriver.Firefox()
# browser.get(target_url) 