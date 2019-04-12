# -*- coding: utf-8 -*-


# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
USER_AGENT = 'TweetScraper'

# settings for spiders
BOT_NAME = 'TweetScraper'
LOG_LEVEL = 'INFO'
# from http://stackoverflow.com/a/31233576/2297751, TODO
DOWNLOAD_HANDLERS = {'s3': None, }

SPIDER_MODULES = ['TweetScraper.spiders']
NEWSPIDER_MODULE = 'TweetScraper.spiders'
ITEM_PIPELINES = {
    'TweetScraper.pipelines.SaveToFilePipeline': 100,
    # 'TweetScraper.pipelines.SaveToMongoPipeline':100, # replace `SaveToFilePipeline` with this to use MongoDB
}

# settings for where to save data on disk
SAVE_TWEET_PATH = './Data/tweet/'
SAVE_USER_PATH = './Data/user/'
SAVE_USER_FOLLOWERS_PATH = './Data/followers/'
