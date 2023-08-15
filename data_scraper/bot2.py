import bs4, time
from requests_html import HTMLSession

'''

NOW:
-> checking the latest data_string that is up on web and the most recent data_string on the log file
    -> create a function that returns the most recent data-string of the log file {done}
    -> create a function that accesses the web-page and returns the first data-string on the table
    -> create directory that stores all of the downloaded html contents

'''

# approach with requests-html
target_url = 'https://hedgefollow.com/insider-trading-tracker'

# function that returns the first data-string from the website
def latest_web_datastring(soup):
    return

# retrieve the response object through GET
session = HTMLSession()
response = session.get(target_url)
response.html.render()

time.sleep(5)

# save webpage locally
html_content = response.html.html


# Save the HTML content to a file
with open('random-attempt.txt', "w", encoding="utf-8") as file:
    file.write(html_content)

# Close the session
session.close()

print('Successfully stored the webpage!')

try:
    with open('./random-attempt.txt', 'r') as file:
        soup = bs4.BeautifulSoup(file, 'html.parser')

    all_trs = soup.find('table', class_='dataTable')
    content = soup.select('.dataTable tbody tr')
    print(content)
    print('Successfully retreived the date contents!')
except Exception as error:
    print('Failed to retreive date contents...')

'''
NOTE: 8/7/23
-> import bot/bot2 modules into the detect/start file and only run them when the most recent data string
   that's current on the webpage is not equal to the most recent data string on the log

-> may just exclude the downloaded content into a directory and sort them out

-> also store all relevant data on a json file for data analysis and for visualizing them on pies charts, etc

-> setup cron on mac so that mac can automatically run the script at 6pm

Real-time Audio/Video Processing: Create a real-time audio or video processing application, such as a digital audio workstation (DAW) or a video editing tool, that requires efficient memory management and low-latency processing.

Data Visualization: Develop a simple data visualization tool (possibly a PC application) that can interpret and display the logged sensor data in graphical or tabular format.

finish this web scraping python project then complete the shell project -> multiplayer -> network disrupter w/ c++ -> sound displayer c++ -> file encryption
'''