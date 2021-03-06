from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.conf import settings
from scrapy import http
from scrapy.shell import inspect_response  # for debugging
import re
import json
import time
import os
import logging
import requests

# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains, keys
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

from datetime import datetime

from TweetScraper.items import Tweet, User
from TweetScraper.utils import mkdirs

from urllib.request import urlopen

from TweetScraper.spiders.preprocessor import testDictionary


logger = logging.getLogger(__name__)


# REQUIRED libraries
# pip install requests
# pip install selenium
# http://phantomjs.org/download.html

# might use
# https://sites.google.com/a/chromium.org/chromedriver/downloads

# command used to start project
# scrapy crawl TweetScraper -a query="@katyperry"


class TweetScraper(CrawlSpider):
    name = 'TweetScraper'
    allowed_domains = ['twitter.com']

    def __init__(self, query='', lang='', crawl_user=False, top_tweet=False):

        self.query = query
        self.url = "https://twitter.com/i/search/timeline?l={}".format(lang)

        if not top_tweet:
            self.url = self.url + "&f=tweets"

        self.url = self.url + "&q=from:" + "%s&src=typed&max_position=%s"
        self.profile_url = "https://twitter.com/" + self.query[1:]
        self.profile_following = "https://twitter.com/" + \
            self.query[1:] + "/following/"

        self.crawl_user = crawl_user

    def start_requests(self):
        if not self.check(self.query + "\n"):
            yield http.Request(self.profile_url, callback=self.parse_profile_page)

    def parse_page(self, response):
        # inspect_response(response, self)
        # handle current page
        data = json.loads(response.body.decode("utf-8"))
        for item in self.parse_tweets_block(data['items_html']):
            yield item

        # get next page
        min_position = data['min_position']
        min_position = min_position.replace("+", "%2B")
        url = self.url % (quote(self.query), min_position)
        yield http.Request(url, callback=self.parse_page)

    def parse_profile_page(self, response):
        response = urlopen(self.profile_url,)
        page, result = self.check_if_account_protected(response)
        print("fsdfds")
        temp = []
        temp_list = []

        if(not result):
            # data = response.read().decode("utf-8")
            print("hello")
            # page = Selector(text=data)
            items_labels = page.xpath(
                '//span[@class="ProfileNav-label"]/text()')
            items = page.xpath('//span/@data-count')

            for i in range(0, len(items_labels)-1):
                temp.append(items_labels[i].extract())

            for i in range(0, len(items)):
                temp_list.append(items[i].extract())

            if "Followers" in temp:
                index = temp.index("Followers")
                number = int(temp_list[index])

                if number > 100000:
                    user = User()
                    user['ID'] = page.xpath(
                        './/div/@data-user-id').extract()[0]
                    user['name'] = page.xpath('.//div/@data-name').extract()[0]
                    user['screen_name'] = page.xpath(
                        './/div/@data-screen-name').extract()[0]

                    for i in range(0, len(items_labels)-1):
                        if items_labels[i].extract() != "Lists" and items_labels[i].extract() != "Moments":
                            user[items_labels[i].extract()] = items.extract()[
                                i]
                    yield user

                    url = self.url % (quote(self.query), '')
                    yield http.Request(url, callback=self.parse_page)
                    self.scrap_following()

    def scrap_following(self):

        browser = webdriver.PhantomJS(
            executable_path='C:/Users/ShuaibReeyaz/Downloads/phantomjs-2.1.1-windows/bin/phantomjs')
        browser.get("https://twitter.com/" + self.query[1:] + "/following")
        action = action_chains.ActionChains(browser)

        time.sleep(2)

        username = browser.find_element_by_css_selector(
            '.js-username-field.email-input.js-initial-focus')
        username.send_keys('bvams2019@gmail.com')

        password = browser.find_element_by_css_selector('.js-password-field')
        password.send_keys('ilias2019!')

        form = browser.find_element_by_css_selector(
            '.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
        form.submit()

        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        last_height = browser.execute_script(
            "return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        element = browser.find_element_by_xpath("//body")
        page = Selector(text=element.text)
        info = (element.text).split()

        self.saveUserPath = settings['SAVE_USER_FOLLOWERS_PATH']
        mkdirs(self.saveUserPath)
        savePath = os.path.join(self.saveUserPath, "following" + ".txt")
        with open(savePath, 'a+') as f:
            for i in info:
                if i.startswith('@') and len(i) > 1 and i != self.query:
                    f.write(i)
                    f.write("\n")
        savePath = os.path.join(self.saveUserPath, "scrapped_users" + ".txt")
        with open(savePath, 'a+') as f:
            f.write(self.query)
            f.write("\n")

    def check_if_account_protected(self, response):
        data = response.read().decode("utf-8")
        page = Selector(text=data)
        protected_item_label = page.xpath(
            '//span[@class="Icon Icon--protected"]')

        # if there is a protected icon on the the account it will return True
        # otherwise it will return False if there isn't
        if(len(protected_item_label) > 0):
            return None, True
        else:
            return page, False

    def parse_tweets_block(self, html_page):
        page = Selector(text=html_page)

        # for text only tweets
        items = page.xpath('//li[@data-item-type="tweet"]/div')
        for item in self.parse_tweet_item(items):
            yield item

    def parse_tweet_item(self, items):
        for item in items:
            try:
                tweet = Tweet()
                tweet['usernameTweet'] = item.xpath(
                    './/span[@class="username u-dir u-textTruncate"]/b/text()').extract()[0]

                ID = item.xpath('.//@data-tweet-id').extract()
                if not ID:
                    continue
                tweet['ID'] = ID[0]

                # get text content
                tweet['text'] = ' '.join(
                    item.xpath('.//div[@class="js-tweet-text-container"]/p//text()').extract()).replace(' # ',
                                                                                                        '#').replace(
                    ' @ ', '@')
                if tweet['text'] == '':
                    # If there is not text, we ignore the tweet
                    continue

                # get meta data
                tweet['url'] = item.xpath(
                    './/@data-permalink-path').extract()[0]

                nbr_retweet = item.css('span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount').xpath(
                    '@data-tweet-stat-count').extract()
                if nbr_retweet:
                    tweet['nbr_retweet'] = int(nbr_retweet[0])
                else:
                    tweet['nbr_retweet'] = 0

                nbr_favorite = item.css('span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount').xpath(
                    '@data-tweet-stat-count').extract()
                if nbr_favorite:
                    tweet['nbr_favorite'] = int(nbr_favorite[0])
                else:
                    tweet['nbr_favorite'] = 0

                nbr_reply = item.css('span.ProfileTweet-action--reply > span.ProfileTweet-actionCount').xpath(
                    '@data-tweet-stat-count').extract()
                if nbr_reply:
                    tweet['nbr_reply'] = int(nbr_reply[0])
                else:
                    tweet['nbr_reply'] = 0

                tweet['datetime'] = datetime.fromtimestamp(int(
                    item.xpath('.//div[@class="stream-item-header"]/small[@class="time"]/a/span/@data-time').extract()[
                        0])).strftime('%Y-%m-%d %H:%M:%S')

                # get photo
                has_cards = item.xpath('.//@data-card-type').extract()
                if has_cards and has_cards[0] == 'photo':
                    tweet['has_image'] = True
                    tweet['images'] = item.xpath(
                        './/*/div/@data-image-url').extract()
                # elif has_cards:
                #     logger.debug('Not handle "data-card-type":\n%s' %
                #                  item.xpath('.').extract()[0])

                # get animated_gif
                has_cards = item.xpath('.//@data-card2-type').extract()
                if has_cards:
                    if has_cards[0] == 'animated_gif':
                        tweet['has_video'] = True
                        tweet['videos'] = item.xpath(
                            './/*/source/@video-src').extract()
                    elif has_cards[0] == 'player':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath(
                            './/*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary_large_image':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath(
                            './/*/div/@data-card-url').extract()
                    elif has_cards[0] == 'amplify':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath(
                            './/*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath(
                            './/*/div/@data-card-url').extract()
                    elif has_cards[0] == '__entity_video':
                        pass  # TODO
                        # tweet['has_media'] = True
                        # tweet['medias'] = item.xpath('.//*/div/@data-src').extract()
                    # else:  # there are many other types of card2 !!!!
                    #     logger.debug('Not handle "data-card2-type":\n%s' %
                    #                  item.xpath('.').extract()[0])

                is_reply = item.xpath(
                    './/div[@class="ReplyingToContextBelowAuthor"]').extract()
                tweet['is_reply'] = is_reply != []

                is_retweet = item.xpath(
                    './/span[@class="js-retweet-text"]').extract()
                tweet['is_retweet'] = is_retweet != []

                tweet['user_id'] = item.xpath('.//@data-user-id').extract()[0]

                # print(tweet)
                tweet['text'] = testDictionary(tweet)
                if tweet['text'] != []:
                    yield tweet

            except:
                pass
                # logger.error("Error tweet:\n%s" % item.xpath('.').extract()[0])
                # raise

    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default

    def get_query(self):
        return self.query

    def check(self, stringToMatch):

        saveUserPath = settings['SAVE_USER_FOLLOWERS_PATH']
        mkdirs(saveUserPath)
        savePath = os.path.join(saveUserPath, "scrapped_users" + ".txt")
        with open(savePath, 'a+') as file:
            for line in file:
                if stringToMatch == line:
                    return True
            return False
