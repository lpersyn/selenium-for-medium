# -*- coding: utf-8 -*-
import os

from selenium import webdriver
import MediumTagScraper

# windows path
dataPath = "C:\\Users\\persy\\PycharmProjects\\SeleniumMedium\\"


# linux path
# dataPath = "/u/lpersyn/Desktop/Python/SeleniumMedium/data-output/"

def save_files(articles):
    for article in articles:
        articleTitle = article[0]
        articleText = article[1]

        articleFile = open(dataPath + directory + '\\' + articleTitle + ".txt", 'w')
        print(articleText, file=articleFile)


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('-incognito')

    # linux path
    # browser = webdriver.Chrome("/u/lpersyn/Desktop/Python/SeleniumMedium/chromedriver/chromedriver.exe",
    #                            options=option)

    # windows path
    browser = webdriver.Chrome("C:\\Users\\persy\\PycharmProjects\\SeleniumMedium\\chromedriver\\chromedriver.exe",
                               options=option)

    tags = ['entrepreneurship']

    for tag in tags:
        directory = tag + 'Articles'
        if not os.path.exists(directory):
            os.mkdir(directory)
        for i in range(0, 20):
            year = 2000 + i
            save_files(MediumTagScraper.get_tag_articles(tag, str(year), browser))

    browser.quit()
