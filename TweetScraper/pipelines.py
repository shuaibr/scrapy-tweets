# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy.conf import settings
import logging
import pymongo
import json
import os
import sys

# for mysql
import mysql.connector
from mysql.connector import errorcode

from TweetScraper.items import Tweet, User
from TweetScraper.utils import mkdirs


logger = logging.getLogger(__name__)

# grabs the command line query
QUERY = sys.argv


# keep


class SaveToFilePipeline(object):
    ''' pipeline that save data to disk '''

    def __init__(self):
        self.saveTweetPath = settings['SAVE_TWEET_PATH']
        self.saveUserPath = settings['SAVE_USER_PATH']
        self.savefollowersPath = settings['SAVE_USER_FOLLOWERS_PATH']
        mkdirs(self.saveTweetPath)  # ensure the path exists
        mkdirs(self.saveUserPath)
        mkdirs(self.savefollowersPath)

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            savePath = os.path.join(
                self.saveTweetPath, QUERY[3].split("=")[1] + ".txt")
            if os.path.isfile(savePath):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                self.save_to_file(item, savePath)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                self.save_to_file(item, savePath)
                logger.debug("Add tweet:%s" % item['url'])

        elif isinstance(item, User):
            savePath = os.path.join(self.saveUserPath, "Users" + ".txt")
            if os.path.isfile(savePath):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                self.save_to_file(item, savePath)
                # logger.info("Update user:%s"%dbItem['screen_name'])
            else:
                self.save_to_file(item, savePath)
                logger.debug("Add user:%s" % item['screen_name'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))

    def save_to_file(self, item, fname):
        ''' input: 
                item - a dict like object
                fname - where to save
        '''
        with open(fname, 'a+') as f:
            json.dump(dict(item), f)
            f.write("\n")
