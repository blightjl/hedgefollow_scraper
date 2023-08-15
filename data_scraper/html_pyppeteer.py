import asyncio, re, os
from pyppeteer import launch

'''
NOTE: 
8/11/23
-> add function for checking data-string until found by scanning through each of the pages until it is found or until
   the previous date is being scanned
-> create directories
-> incorporate the sequential filename for when downloading html content for consecutive/sequential page(s)
-> finish the generating of different files with sequential numbering (done)
-> fix the generate_source_name() where it properly creates the files rather than downloading them (done)
'''

# approach with pyppeteer
target_url = 'https://hedgefollow.com/insider-trading-tracker'

# function to check whether the file already exists, if it does increment the 
# digit part of the name and return it
# command to check if file exists: os.path.exists(file_path)
# also need to sort the directory so we check in order
# does not work when: there is a file with the same name with missing numbers in between
# works as long as every file with given file_name is sequential and none are missing
def generate_source_name():
    naming_convention = r'^raw_html-(\d+)\.txt$'
    sorted_directory_files = sorted(os.listdir('.'))
    print(sorted_directory_files)
    for file in sorted_directory_files:
        match = re.match(naming_convention, file)
        if match:
            print("FOUND MATCH:")
            print(file)
            # need to check if the next increment of the current number is free, if it is create that one and return
            curr_num = int(match.group(1))
            if not os.path.exists("raw_html-" + str(curr_num + 1) + ".txt"):
                print("The next available number is: raw_html-" + str(curr_num + 1) + ".txt")
                return "raw_html-" + str(curr_num + 1) + ".txt"
    print("The next available number is: raw_html-" + str(1) + ".txt")
    return "raw_html-" + str(1) + ".txt"

# function that will create a file with the given name
def create_file(filename):
    with open(filename, 'w'):
        pass

# function to download the content
def download_content(html_content):
    with open(generate_source_name(), "w", encoding="utf-8") as file:
        file.write(html_content)

# async function to retreive content
async def main():
    print("program started...")
    browser = await launch()
    page = await browser.newPage()
    await page.goto(target_url)
    print("webpage accessed!")

    # wait for elements to appear -> in html content
    await page.waitForSelector('.dataTable tbody tr', {'visible': True}) 
    
    print("found the html content!")
    # download the webpage
    html_content = await page.content()
    print("PRINTING CURRENT PAGE:")
    # print(html_content)
    await page.waitFor(5000)
    # click on the next button if it exists and then download them
    # wait for elements to appear -> time
    button_hier = '.pagination button'
    buttons = await page.querySelectorAll(button_hier)
    print("selected the buttons!")
    # print(buttons)
    for button in buttons:
        button_text_content = await page.evaluate('(el) => el.textContent', button)
        print(button)
        print(button_text_content.strip())
        if button_text_content.strip() == 'Next >':
            await button.click()
            print("next button clicked!")
            break
    await page.waitFor(5000)
    next_content = await page.content()
    print("PRINTING NEXT PAGE:")
    # print(next_content)
    download_content(next_content)
    await page.waitFor(5000)
    await browser.close()


# asyncio.run(main())
# asyncio.get_event_loop().run_until_complete(main())