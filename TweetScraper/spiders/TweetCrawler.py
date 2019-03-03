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

from bs4 import BeautifulSoup
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

logger = logging.getLogger(__name__)

#REQUIRED libraries
#pip install requests
#pip install beautifulsoup4
#pip install selenium
#https://sites.google.com/a/chromium.org/chromedriver/downloads

class TweetScraper(CrawlSpider):
    name = 'TweetScraper'
    allowed_domains = ['twitter.com']

    def __init__(self, query='', lang='', crawl_user=False, top_tweet=False, following=False):

        #command used to start project
        #scrapy crawl TweetScraper -a query="foo,#bar"
        #scrapy crawl TweetScraper -a query="@katyperry" -a following=True
        self.query = query
        self.following = following
        self.url = "https://twitter.com/i/search/timeline?l={}".format(lang)

        if not top_tweet:
            self.url = self.url + "&f=tweets"

        # temp = "%20"
        # temp1 = "from%3A"
        # self.url = self.url + "&q=" + temp1 +"%s" + temp +"since%3A2019-02-01" + temp +"until%3A2019-02-07"

        self.url = self.url + "&q=from:" + "%s&src=typed&max_position=%s"
        # self.url = self.url + "&q=from@%s%%20since%3A2019-02-10%%20until%3A2019-02-18&src=typed&max_position=%s"
        # self.url = self.url + "&q="  + self.query[1:]
        self.profile_url = "https://twitter.com/" + self.query[1:]
        self.profile_following = "https://twitter.com/" + self.query[1:] + "/following/"
        # self.url = "https://twitter.com/search?l=en&q=from%3Amohamed%%20since%3A2019-02-10%%20until%3A2019-02-18&src=typd&lang=en"

        # self.url = "https://twitter.com/search?l=&q=from%%3A" + "%s" + temp + "since%3A2019-02-10" + temp + "until%3A2019-02-18&src=typed&max_position=%s"

        # self.test = "https://twitter.com/search?l=&q=from%3Amohamed&src=typd&lang=en"

        self.crawl_user = crawl_user

    def start_requests(self):
        if self.following:
            # with requests.Session() as s:
            #     r = s.get("https://twitter.com/login")
            #     soup = BeautifulSoup(r.text,"lxml")

            #     token = soup.select_one("[name='authenticity_token']")['value']

            #     payload={
            #     'session[username_or_email]':'bvams2019@gmail.com',
            #     'session[password]':'ilias2019!',
            #     'authenticity_token':token,
            #     'ui_metrics':'{"rf":{"c6fc1daac14ef08ff96ef7aa26f8642a197bfaad9c65746a6592d55075ef01af":3,"a77e6e7ab2880be27e81075edd6cac9c0b749cc266e1cea17ffc9670a9698252":-1,"ad3dbab6c68043a1127defab5b7d37e45d17f56a6997186b3a08a27544b606e8":252,"ac2624a3b325d64286579b4a61dd242539a755a5a7fa508c44eb1c373257d569":-125},"s":"fTQyo6c8mP7d6L8Og_iS8ulzPObBOzl3Jxa2jRwmtbOBJSk4v8ClmBbF9njbZHRLZx0mTAUPsImZ4OnbZV95f-2gD6-03SZZ8buYdTDkwV-xItDu5lBVCQ_EAiv3F5EuTpVl7F52FTIykWowpNIzowvh_bhCM0_6ReTGj6990294mIKUFM_mPHCyZxkIUAtC3dVeYPXff92alrVFdrncrO8VnJHOlm9gnSwTLcbHvvpvC0rvtwapSbTja-cGxhxBdekFhcoFo8edCBiMB9pip-VoquZ-ddbQEbpuzE7xBhyk759yQyN4NmRFwdIjjedWYtFyOiy_XtGLp6zKvMjF8QAAAWE468LY"}',
            #     'scribe_log':'',
            #     'redirect_after_login':'https://twitter.com/katyperry/following',
            #     'authenticity_token':token,
            #     'remember_me':1
            #     }
            #     headers={
            #     'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            #     'content-type':'application/x-www-form-urlencoded',
            #     'origin':'https://twitter.com',
            #     'referer':'https://twitter.com/login',
            #     'upgrade-insecure-requests':'1',
            #     'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            #     }
            #     res = s.post("https://twitter.com/sessions",data=payload,headers=headers)
            #     soup = BeautifulSoup(res.text,"lxml")

            browser = webdriver.Chrome('D:\Downloads\chromedriver_win32\chromedriver.exe')
            browser.get("https://twitter.com/katyperry/following")
            action = action_chains.ActionChains(browser)

            # open up the developer console, mine on MAC, yours may be diff key combo
            # action.send_keys(keys.Keys.CONTROL,keys.Keys.SHIFT,'i')
            # action.perform()
            time.sleep(2)
            # action.send_keys(keys.Keys.ENTER)
            # inject the JavaScript...
            # action.send_keys("document.querySelectorAll('label.boxed')[1].click()"+keys.Keys.ENTER)
            # action.perform()
            # browser.execute_script("document.querySelectorAll('label.boxed')[1].click()")

            username = browser.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
            username.send_keys('bvams2019@gmail.com')

            password = browser.find_element_by_css_selector('.js-password-field')
            password.send_keys('ilias2019!')

            form = browser.find_element_by_css_selector('.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
            form.submit()

            # elem = browser.find_element_by_class_name("ProfileCard-screenname")
            # elem = browser.find_element_by_xpath("//span[@class='username u-dir']").click()
            # browser.implicitly_wait(6000000)
            
            no_of_pagedowns = 20

            # while no_of_pagedowns:
            #     action.send_keys(keys.Keys.PAGE_DOWN)
            #     time.sleep(0.2)
            #     no_of_pagedowns-=1
            SCROLL_PAUSE_TIME = 0.5

            # Get scroll height
            last_height = browser.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            #     element = browser.find_element_by_xpath("//div[@class='GridTimeline-end has-items']")
            # action.move_to_element(element).perform()
            # element = browser.find_elements_by_class_name('Grid Grid--withGutter')
            # browser.location_once_scrolled_into_view
            element = browser.find_element_by_xpath("//body")
            # action.move_to_element(element).perform()
            page = Selector(text=element.text)
            # items = page.xpath('text()')
            info = (element.text).split()
            # print((element.text).split(), "saklfjslfjolsjfdlkiskjfkl")

            
            self.saveUserPath = settings['SAVE_USER_FOLLOWERS_PATH']
            mkdirs(self.saveUserPath)
            savePath = os.path.join(self.saveUserPath, "following" + ".txt")
            with open(savePath,'a+') as f:
                for i in info:
                    if i.startswith('@') and len(i) > 1 and i != self.query:
                        print(i)
                        f.write(i)
                        f.write("\n")
                # try:
                #     # element = WebDriverWait(browser, 20).until(
                #     #     EC.element_to_be_clickable((By.XPATH, "//div"))
                #     # )
                #     element = browser.find_element_by_xpath('//div')
                #     print(element.text.split(" "), "saklfjslfjolsjfdlkiskjfkl")
                #     # element.click()
                # finally:
                #     browser.quit()

            # post_elems = browser.find_elements_by_class_name("post-item-title")

            # for item in soup.select(".u-linkComplex-target"):
            #     print(item.text)
            # yield http.Request(url, callback=self.scrap_following)
        else:
            url = self.url % (quote(self.query), '')
            yield http.Request(url, callback=self.parse_page)
            yield http.Request(self.profile_url, callback=self.parse_profile_page)

    def scrap_following(self,response):
        print("fsfsdf")
        print(response)
        response = urlopen(self.profile_following,)
        data = response.read().decode("utf-8")
        # print(data)
        page = Selector(text=data)
        # print(page.xpath("//"))

    def parse_page(self, response):
        # inspect_response(response, self)
        # handle current page
        data = json.loads(response.body.decode("utf-8"))
        for item in self.parse_tweets_block(data['items_html']):
            yield item

        # get next page
        min_position = data['min_position']
        min_position = min_position.replace("+","%2B")
        url = self.url % (quote(self.query), min_position)
        yield http.Request(url, callback=self.parse_page)

    def parse_profile_page(self, response):
        # print(response)
        response = urlopen(self.profile_url,)
        data = response.read().decode("utf-8")
        page = Selector(text=data)
        items = page.xpath('//span/@data-count')

        if self.crawl_user:
            ### get user info
            user = User()
            user['ID'] = page.xpath('.//div/@data-user-id').extract()[0]
            user['name'] = page.xpath('.//div/@data-name').extract()[0]
            user['screen_name'] = page.xpath('.//div/@data-screen-name').extract()[0]

            user['number_of_tweets'] = items.extract()[0]
            user['following'] = items.extract()[1]
            user['followers'] = items.extract()[2]
            user['likes'] = items.extract()[3]
            yield user

    def parse_tweets_block(self, html_page):
        page = Selector(text=html_page)

        ### for text only tweets
        items = page.xpath('//li[@data-item-type="tweet"]/div')
        for item in self.parse_tweet_item(items):
            yield item

    def parse_tweet_item(self, items):
        for item in items:
            try:
                tweet = Tweet()
                tweet['usernameTweet'] = item.xpath('.//span[@class="username u-dir u-textTruncate"]/b/text()').extract()[0]

                ID = item.xpath('.//@data-tweet-id').extract()
                if not ID:
                    continue
                tweet['ID'] = ID[0]

                ### get text content
                tweet['text'] = ' '.join(
                    item.xpath('.//div[@class="js-tweet-text-container"]/p//text()').extract()).replace(' # ',
                                                                                                        '#').replace(
                    ' @ ', '@')
                if tweet['text'] == '':
                    # If there is not text, we ignore the tweet
                    continue

                ### get meta data
                tweet['url'] = item.xpath('.//@data-permalink-path').extract()[0]

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

                ### get photo
                has_cards = item.xpath('.//@data-card-type').extract()
                if has_cards and has_cards[0] == 'photo':
                    tweet['has_image'] = True
                    tweet['images'] = item.xpath('.//*/div/@data-image-url').extract()
                elif has_cards:
                    logger.debug('Not handle "data-card-type":\n%s' % item.xpath('.').extract()[0])

                ### get animated_gif
                has_cards = item.xpath('.//@data-card2-type').extract()
                if has_cards:
                    if has_cards[0] == 'animated_gif':
                        tweet['has_video'] = True
                        tweet['videos'] = item.xpath('.//*/source/@video-src').extract()
                    elif has_cards[0] == 'player':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary_large_image':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'amplify':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == 'summary':
                        tweet['has_media'] = True
                        tweet['medias'] = item.xpath('.//*/div/@data-card-url').extract()
                    elif has_cards[0] == '__entity_video':
                        pass  # TODO
                        # tweet['has_media'] = True
                        # tweet['medias'] = item.xpath('.//*/div/@data-src').extract()
                    else:  # there are many other types of card2 !!!!
                        logger.debug('Not handle "data-card2-type":\n%s' % item.xpath('.').extract()[0])

                is_reply = item.xpath('.//div[@class="ReplyingToContextBelowAuthor"]').extract()
                tweet['is_reply'] = is_reply != []

                is_retweet = item.xpath('.//span[@class="js-retweet-text"]').extract()
                tweet['is_retweet'] = is_retweet != []

                tweet['user_id'] = item.xpath('.//@data-user-id').extract()[0]
                yield tweet

            except:
                logger.error("Error tweet:\n%s" % item.xpath('.').extract()[0])
                # raise

    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default

    def get_query(self):
        return self.query

