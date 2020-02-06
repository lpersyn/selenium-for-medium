import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import MediumArticleScraper


def lambda_handler(event, context):
    queryInfo = get_query(event)

    if len(queryInfo) == 0:
        return error_response("query is empty")

    tag = queryInfo[0]
    year = queryInfo[1]
    month = queryInfo[2]
    day = queryInfo[3]

    option = webdriver.ChromeOptions()
    option.add_argument(' — incognito')
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-gpu')
    option.add_argument('--window-size=1280x1696')
    option.add_argument('--user-data-dir=/tmp/user-data')
    option.add_argument('--hide-scrollbars')
    option.add_argument('--enable-logging')
    option.add_argument('--log-level=0')
    option.add_argument('--v=99')
    option.add_argument('--single-process')
    option.add_argument('--data-path=/tmp/data-path')
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--homedir=/tmp')
    option.add_argument('--disk-cache-dir=/tmp/cache-dir')
    option.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    option.binary_location = os.getcwd() + "/bin/headless-chromium"

    browser = webdriver.Chrome(options=option)

    browser.get('https://medium.com/tag/' + tag + '/archive/' + year + '/' + month + '/' + day)

    # Wait 20 seconds for page to load
    timeout = 20

    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="svgIcon '
                                                                                          'svgIcon--logoMonogram '
                                                                                          'svgIcon--45px"]')))
    except TimeoutException:
        # print('Timed out waiting for page to load')
        browser.quit()
        return error_response("Time out waiting for page to load")

    link_elements = browser.find_elements_by_xpath('//div[@class="postArticle postArticle--short js-postArticle '
                                                   'js-trackPostPresentation js-trackPostScrolls"]/div[2]/a[@class]')

    # link_elements.find_element_by_xpath('.//a[@class]')

    links = [x.get_attribute("href") for x in link_elements]

    return create_response(MediumArticleScraper.process_links(links, browser))


def get_query(event):
    query_string = event['queryStringParameters']
    query_info = []
    if query_string is not None:
        tag = query_string["tag"]
        date_string = query_string["date"]
        year = date_string[0:4]
        month = date_string[4:6]
        day = date_string[6:8]
        query_info = [tag, year, month, day]
    else:
        query_info = []
    return query_info


def create_response(articles):
    return {
        'statusCode': '200',
        'body': json.dumps(articles),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def error_response(error):
    return {
        'statusCode': '404',
        'body': "There was an ERROR!!!:" + error,
        'headers': {
            'Content-Type': 'application/json',
        }
    }

    # # find_elements_by_xpath returns an array of selenium objects.
    # titles_element = browser.find_elements_by_xpath('//span[@class="repo js-pinnable-item"]')
    # # use list comprehension to get the actual repo titles and not the selenium objects.
    # titles = [x.text for x in titles_element]
    # # print out all the titles.
    # print('titles:')
    # print(titles, '\n')

    # language_element = browser.find_elements_by_xpath('//p[@class="mb-0 f6 text-gray"]')
    # # same concept as for list-comprehension above.
    # languages = [x.text for x in language_element]
    # print('languages:')
    # print(languages, "\n")
    #
    # for title, language in zip(titles, languages):
    #     print("RepoName : Language")
    #     print(title + ": " + language, '\n')
