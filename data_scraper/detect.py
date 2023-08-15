import sys, bs4, log, os.path, re, datetime
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from enum import Enum, auto
from transaction import Transaction, TRANSACTION_TYPE

# so far the program will only check for all data table rows in the currently loaded page
# FUTURE --> update to include / check the next page until condition is met or until pages -> 
# can include ways where it can be multiple pages with same date
# have all ran out

### NOTE: create function that prints out the number of pages that it has traversed with the number of elements that is in the current
###       table and stop at last page

# IMPORTANT: the transaction values accessed are not the most accurate! -> need a way to find the RAW VALUES FOR EACH ONE {done}

# IMPORTANT: need additional parser for data-val for the person who made the transaction {done}
#            -> need to filter out the '-' and '<br>' from the string content in the title tag in the class 'smallText hasTooltip' {done}
#            -> since inside a for loop use an incrementer to indicate which iteration the loop is on, when at 1, print/document
#               the additional contents  {done}

log_file_path = './random-attempt.txt'
temp = './latest.log' 
log_path = './latest.log'

class VALUE_TYPE(Enum):
    MAGNITUDE = auto()
    PERCENTAGE = auto()

# function that will convert a string with 
def string_to_float(formatted_string):
    char_values = {
        'k' : 1000,
        'm' : 1000000,
        'b' : 1000000000,
        't' : 1000000000000
    }
    # use regular expression to check if in format of float followed by nothing or single char

    match = re.match(r'^(\d*\.?\d*)([kmbt]?)$', formatted_string, re.IGNORECASE)
    if match:
        number = float(match.group(1))
        char = match.group(2).lower()
        if char in char_values:
            return number * char_values[char]
        return number
    raise ValueError("Invalid format provided")

# function that returns only the second match of the logged_string
def filter_log(logged_string):
    # 2023-08-14 16:35:32,703 - 
    match = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - (.*)', logged_string)
    if match:
        return match.group(1)
    else:
        return logged_string


# detects the contents of the html content from webpage.txt
def find_date(soup):
    print('Attempting...')
    if soup.name == 'tbody':
        #print('soup contains contents')
        #print('selected the first tr')
        print(soup.select('tr')[-1].select('td')[-1].text)
        #print('found the date element')

# need another function that will parse the soup object for a transaction 
# into one long string that will be appended
def parse_soup(soup):
    current_soup = soup.select('tr')[0].select('td') 
    #print(current_soup)
    text_list = []
    for td in current_soup:
        text_list.append(td.text)
    log_string = " ".join(text_list)
    log_latest(log_string) #HERE
    return log_string
    # ^ selects the list of information for that specific transaction

# checks whether the given string is equal to given soup content
# returns true if the tr content has its string equivalent to the provided data string
def check_tr_string(tr, data_string):
    td_body = tr.select('td')
    left_data_string = td_body_to_string(td_body)
    return left_data_string == data_string

# function that will filter the log string into just data string that can be used for comparison
# returns just the data portion of the logged string that filters out the access times for the data
def filter_log_string(log_string):
    if len(log_string) < 26:
        raise Exception("The logged string is invalid!")
    return log_string[26:]


# function that checks if token contains <br>, returning true if it does
def contains_br(token):
    return token.find("<br>") >= 0

# function that filters out the dashes and line break tags from string
def clean_title_element(string):
    if len(string) <= 0:
        return ""
    tokens = list(filter(None, re.split(r'- ', string)))
    no_br_tokens = [token.replace("<br>", "") if contains_br(token) else token for token in tokens]
    return '{' + ", ".join(no_br_tokens) + '}'

# function that converts given a single data table into a data string
def td_body_to_string(td_body):
    if len(td_body) < 1:
        return ""
    string_tokens = []
    count = 0
    for td in td_body:
        if count == 1:
            nested_class = 'smallText hasTooltip'
            if td.find(class_=nested_class):
                additional_info = td.select('[class="smallText hasTooltip"]')[0]
                string_tokens.append(td.get('data-val'))
                string_tokens.append(clean_title_element(additional_info.get('title')))
                '''
                print(td.get('data-val'))
                print("THE ADDITIONAL ELEMENT: ", end=' ')
                print(additional_info)
                print("THE TITLE: ", end=' ')
                #print(additional_info.get('title'))
                print(clean_title_element(additional_info.get('title')))
                '''
                continue
        #print(td.get('data-val'))
        string_tokens.append(td.text)
        count += 1
    tr_data_string = " ".join(string_tokens)
    return tr_data_string

# function that retreives the most recent data that is up on the soup table
# returns a string of the data
def most_recent_data(soup):
    tr_contents = soup.select('.dataTable tbody tr')
    td_body = tr_contents[0].select('td')
    recent = td_body_to_string(td_body)
    log_latest(recent)
    return recent

# function that will retreive the most recently accessed data table from the log file
# return the last table row data that was accessed, throws an exception error if
# no data table was accessed before or if the log file does not exist
def last_data():
    if not os.path.isfile(log_path):
        raise Exception("Log file does not exist.")
    with open(log_path, 'rb') as log_file:
        try:
            log_file.seek(-2, os.SEEK_END)
            while log_file.read(1) != b'\n':
                log_file.seek(-2, os.SEEK_CUR)
        except Exception:
            log_file.seek(0)
        last = log_file.readline().decode()
        if last != "Start of log file:":
            return last
    raise Exception("No record of last log.")

# IMPORTANT -> need to further parse the logged date out of the format


'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ALL FUNCTION IN THE FOLLOWING TAKES IN A SOUP OBJECT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
# checks whether the transaction was for buying or selling {or in some cases sale plan}
# retreives the number of shares that were in the transaction
def transaction_change(tr):
    return string_to_float(tr.select('td')[3].text)

# retreives the total number of shares owned in the transaction
def transaction_owned(tr):
    return string_to_float(tr.select('td')[6].text)

# retreives the date of transaction
def transaction_date(tr):
    return tr.select('td')[-1].text

# retreives the html element that holds the data for the type of transaction that was made
# determines whether a transaction was bought or sold {or a special case where it was a sale plan}
def transaction_type(tr):
    type_string = tr.select('td')[2].select('.cellContainer .cellSpan')[0].text
    if type_string == 'Buy':
        return TRANSACTION_TYPE.BOUGHT
    elif type_string == 'Sell':
        return TRANSACTION_TYPE.SOLD
    else:
        return TRANSACTION_TYPE.SALE_PLAN
    

# function that returns today's date
def curr_date():
    return datetime.today().date()

# function that returns the day before the given date
def day_before(date: datetime):
    return date - timedelta(days=1)
    
# function that returns true if the given date is within either today or yesterdays date
def valid_date(date: str):
    today = curr_date()
    today_str = curr_date().strftime('%Y-%m-%d')
    yesterday_str = day_before(today).strftime('%Y-%m-%d')
    return date == today_str or date == yesterday_str

# function that will add all data rows from the soup object that until a table row is
# equivalent to the provided data string

### FOR  8/14/23 --> add another condition where additional parameter for var: date is taken
### and another function that checks whether the date that is being checked for can be 
### entered, if not -> return {done}
### --> another important consideration --> what to do if there are no elements that satisfy the conditions?
###
### --> NOW: combine detect.py and html_pyppeteer.py so that they work in conjunction and
###     only create a new file when necessary and does not create a new file if no need
###     -> so start off w/ checking most recent logged file with most recent web data string
'''
if web_str date < log_str date:
    log the web_str into log-file
    store all new web_str's that are updated on the website
    -> then perform the printing function
    stop once upto date
else:
    do nothing
'''
###         -> also a good time to implement the directory for the new files that get generated
###         -> instead of multiple files can store in a file for certain size (i.e.: 50MB)
###            and only creates a new file when needed {in .json file format}
###         -> store all new datas in a list then append them to the file
def list_tr(soup, data_string):
    tr_contents = soup.select('.dataTable tbody tr')
    raw_tr_list = []
    for tr in tr_contents:
        tr_date = transaction_date(tr)
        if not check_tr_string(tr, data_string) and transaction_type(tr) != TRANSACTION_TYPE.SALE_PLAN and valid_date(tr_date):
            raw_tr_list.append(tr)
    return raw_tr_list

    
# receives the tr soup objects and creates a dictionary that maps each of the sub-element to
# the Transaction class
def extract_stats(list_tr):
    stat_dictionary = {}
    for tr in list_tr:
        raw = transaction_change(tr)
        owned = transaction_owned(tr)
        percentage = None
        if owned <= 0:
            percentage = 0
        else:
            percentage = raw / owned
        type = transaction_type(tr)
        new_stat = Transaction(raw, percentage, type)
        stat_dictionary[tr] = new_stat
    return stat_dictionary

# function that will format the given key and value into a formatted string that will display
# the specific transaction and make it readable
# !the type will define whether it is for highest magnitude or percentage

def print_info(tr, type: VALUE_TYPE):
    # testing to check if tr contains anything
    print("PRINTING TR CONTENTS: ")
    try:
        buyer_str = ""
        buyer_td = tr.select('td')[1]
        nested_class = 'smallText hasTooltip'
        if buyer_td.find(class_=nested_class):
            additional_info = buyer_td.select('[class="smallText hasTooltip"]')[0]
            buyer_str += (buyer_td.get('data-val')) + " "
            buyer_str += (clean_title_element(additional_info.get('title')))
        stock_str = tr.select('td')[0].text
        trans_enum = transaction_type(tr)
        trans_type = None
        if trans_enum == TRANSACTION_TYPE.BOUGHT:
            trans_type = "BOUGHT"
        elif trans_enum == TRANSACTION_TYPE.SOLD:
            trans_type = "SOLD"
        else:
            trans_type = "SALE PLAN"
        value = None
        value_type = None
        trans_date = transaction_date(tr)
        if (type == VALUE_TYPE.MAGNITUDE):
            value_type = "magnitude"
            value = "$" + str(transaction_change(tr))
        else:
            value_type = "percentage"
            value = str(transaction_owned(tr)) + "%"
        print("Greatest " + value_type + " of stocks " + trans_type + " was by " + buyer_str + " for " + value + " in " + stock_str + " on " + trans_date + " over the last 24 hours.")
    except:
        print("Error occurred!")
        return
        raise Exception("tr is empty")
    
# --> next to do -> abstraction for two different functions in one
# NOTE: can probably abstract/refactor the following functions into one -> and have a condition to output different
#       strings based on the parameter passed
# finds the highest magnitude in the given list and prints out relevant information
# -> prints out information of the table data with the highest transaction magnitude
def find_max_value(dictionary, type: VALUE_TYPE):
    if len(dictionary) == 0:
        return "cannot compute on empty dictionary."
    key_iterator = iter(dictionary)
    max_key = next(key_iterator)
    max_value = 0
    for key, value in dictionary.items():
        if (type == VALUE_TYPE.MAGNITUDE):
            if value.raw > max_value:
                max_value = value.raw
                max_key = key
            else:
                max_value = value.percentage
                max_key = key
    return max_key

# function that checks whether we can start the program and run required functions
# read up on the datetime module of python and how i can calculate the previous date by looking at current date
def program_start():
    # the most recent data string from the logged file
    recent_data_string = None
    try:
        recent_data_string = last_data(log_file_path)
    except Exception as e:
        # if log file does not exist, create one and recall this method
        if str(e) == "Log file does not exist.":
            log.create_log()
            program_start()
        # if log only contains 'Start of log file:' and other log data
        # 
        elif str(e) == "No record of last log.":
            # the condition will be that until the end of the previous date or the most recent date
            # NOTE for 8/6/23: may need to modify the condition that is checked for list_tr where it also checks the date of the 
            # current object
            recent_data_string = ""
    list_data = list_tr(soup, recent_data_string)
    dict_data_stats = extract_stats(list_data)
    max_mag_key = find_max_value(dict_data_stats, VALUE_TYPE.MAGNITUDE)
    max_pers_key = find_max_value(dict_data_stats, VALUE_TYPE.PERCENTAGE)
    print_info(max_mag_key, VALUE_TYPE.MAGNITUDE)
    print_info(max_pers_key, VALUE_TYPE.PERCENTAGE)
    

# create a list that adds a bunch of values together

'''
NOTES:
- use the html content string for identification of elements
- use dictionary to map value to the string and for finding information
    * this will be a soup object to the magnitude and percentage
'''

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# logs the latest table row's information into a log file (latest.log)
# the latest data that has been accessed will be at the top
def log_latest(transaction_string):
    log.append_log(transaction_string)
    #print('Logging successful!')

# try:
#print('Opening html content...')
with open(log_file_path, 'r') as file:
    soup = bs4.BeautifulSoup(file, 'html.parser')
test_select = soup.select('.dataTable tbody')
print("MOST RECENT DATA: " + most_recent_data(soup))
# print(test_select) # this gets a list of all tbody
#print('Successfully found css content!')
#print()
#print('Finding the latest date...')

#find_date(test_select[0]) # selects the first tbody
#print('Successfully found the latest date!')
#print('The log string: ', end='')
#print(parse_soup(test_select[0]))
#print('Successfully logged!')
#program_start()
#print(curr_date().strftime('%Y-%m-%d'))
#print(day_before(curr_date()).strftime('%Y-%m-%d'))

# except Exception as error:
# print('Failed to retreive html content: ' + str(error))

print("THE LAST DATA IN LOG FILE: ")
last_log_string = last_data()
print(last_log_string)
if re.search('\n', last_log_string) == None:
    print("no new line character found")
else:
    print("there is a new line character!")
print(filter_log(last_log_string))

# function that will parse out the date and check with the logged file in the current directory

'''
program check:
-> need function to get current date and another function to extract date of data-string
-> check until curr meets latest or until two days before (so can check all of yesterday)
   (terminate on whichever happens first)
'''

'''

7/29/23

to-do:

- complete the logging function that appends to the top everytime the script is ran
- complete function that stores all of table rows until previous date or until last table string
- complete function that finds the transaction with highest change in percentage and magnitude

8/6/23

to-do:

- complete the date implementation where in addition to checking data string add condition
  where it checks within the 24 hour frame and stops as soon as it gets before the date

MORE -> can do where we can input from and to dates and maybe even by hours and see the results
        for that time interval

'''