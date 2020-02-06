# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException


def get_article(url, browser):
    browser.get(url)

    articleElement = browser.find_elements_by_xpath('//article//p')

    try:
        titleElement = browser.find_element_by_xpath('//h1')
        title = titleElement.text.replace(" ", "")
        title = "".join(x for x in title if x.isalnum())
    except NoSuchElementException:
        title = 'noTitle'

    articleText = ""

    for p in articleElement:
        articleText = articleText + p.text + '\n'

    articleText = ''.join(i for i in articleText if ord(i) < 128)

    articleText = ''.join(i for i in articleText if ord(i) < 128)

    return [title, articleText]


def process_links(links, browser, tag, date):

    articlesOfTag = []

    for link in links:
        article = get_article(link, browser)
        article[0] = tag + date + '-' + article[0]
        articlesOfTag.append(article)

    return articlesOfTag
    # browser.quit()
