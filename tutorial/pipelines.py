# -*- coding: utf-8 -*-

import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy import log

SETTINGS = get_project_settings()

class MySQLPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def __init__(self, stats):
        #Instantiate DB
        self.dbpool = adbapi.ConnectionPool ('MySQLdb',
            host=SETTINGS['DB_HOST'],
            user=SETTINGS['DB_USER'],
            passwd=SETTINGS['DB_PASSWD'],
            port=SETTINGS['DB_PORT'],
            db=SETTINGS['DB_DB'],
            charset='utf8',
            use_unicode = True,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    def spider_closed(self, spider):
        """ Cleanup function, called after crawing has finished to close open
            objects.
            Close ConnectionPool. """
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._insert_record, item)
        query.addErrback(self._handle_error)
        return item

    def _insert_record(self, tx, item):
        if item['item'] == 'error.html' or item['value'] == "":
            return
        else:
            sql = "INSERT INTO medicine_expand VALUES ('%s','%s','%s')" % (item['item'], item['attribute'], item['value'])
            sql = "INSERT INTO medicine_expand VALUES (%s,%s,%s)"
            # print "sql: " + sql
            result = tx.execute(sql, [item['item'], item['attribute'], item['value']])
            if result > 0:
                self.stats.inc_value('database/items_added')

    def _handle_error(self, e):
        log.err(e)