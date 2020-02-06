# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#dataPath = "C:\\Users\\persy\\PycharmProjects\\SeleniumMedium\\businessData\\"


def get_article(url, browser):
    browser.get(url)

    # Wait 20 seconds for page to load
    timeout = 20

    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//article')))
    except TimeoutException:
        print('Timed out waiting for page to load')
        browser.quit()

    articleElement = browser.find_elements_by_xpath('//article//p')

    titleElement = browser.find_element_by_xpath('//h1')

    articleText = ""

    for p in articleElement:
        articleText = articleText + p.text + '\n'

    articleText = ''.join(i for i in articleText if ord(i) < 128)

    title = titleElement.text.replace(" ", "")
    title = "".join(x for x in title if x.isalnum())

    articleText = ''.join(i for i in articleText if ord(i) < 128)

    return {"title": title, "article": articleText}

    # articleFile = open(dataPath + title + str(index) + ".txt", 'w')
    # print(articleText, file=articleFile)


def process_links(links, browser):
    # linkInput = open('linkFile.txt', 'r')
    # articleLinks = []
    # for line in linkInput.readlines():
    #     articleLinks.append(line)

    # option = webdriver.ChromeOptions()
    # option.add_argument(' — incognito')
    #
    # chrome = webdriver.Chrome(
    #     executable_path='C:\\Users\\persy\\PycharmProjects\\SeleniumMedium\\chromedriver\\chromedriver.exe',
    #     options=option)

    articles = []
    for link in links:
        articles.append(get_article(link, browser))

    browser.quit()

    return articles
