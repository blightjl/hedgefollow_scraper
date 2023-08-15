import logging, os.path

'''

NOTES ON LOGGING:
* script is run everyday @6pm 

* using json file format for last process time and table row:
    - date -> including hour, minute, second
    - everything about the table row

* the next day every row until that recorded table row will be
  processed

* might need to include an algorithm that ciphers the given row's
  data into a string so that in case of conflict with same date 
  and company, we can differentiate between the two

'''

log_file_path = './latest.log'

# create log file if it does not exist
def create_log():
  if not os.path.isfile(log_file_path):
    print('LOG NEEDS TO BE CREATED...')
    print('CREATING LOG FILE')
    log = open(log_file_path, 'a')
    log.write('Start of log file\n')
    log.close()
    print('LOG CREATED.')

create_log()

# sets the logging format
logging.basicConfig(filename=log_file_path, 
                    level=logging.INFO, format='%(asctime)s - %(message)s', filemode='a')

# logs the given string into the top of the opened file
def append_log(string):
    logging.info(string)

# open up the given filename and return the string in the last line without the asctime variable
def retreive_last_data():
   return 'last_data <-'

# function that will will be able to retreive just the string value of the logged information