# -*- coding: utf-8 -*-
import MediumArticleScraper


def get_tag_articles(tag, date, browser):
    # year = date[:4]
    # month = date[4:6]
    # day = date[6:8]

    # articles that day
    # browser.get('https://medium.com/tag/' + tag + '/archive/' + year + '/' + month + '/' + day)

    # top ten articles for year
    browser.get('https://medium.com/tag/' + tag + '/archive/' + date + '/')

    # Wait 20 seconds for page to load
    # timeout = 20

    # try:
    #     WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="svgIcon '
    #                                                                                       'svgIcon--logoMonogram '
    #                                                                                       'svgIcon--45px"]')))
    # except TimeoutException:
    #     print('Timed out waiting for page to load')
    #     browser.quit()
    # return error_response("Time out waiting for page to load")

    link_elements = browser.find_elements_by_xpath('//div[@class="postArticle postArticle--short js-postArticle '
                                                   'js-trackPostPresentation js-trackPostScrolls"]/div[2]/a[@class]')

    links = [x.get_attribute("href") for x in link_elements]

    return MediumArticleScraper.process_links(links, browser, tag, date)
