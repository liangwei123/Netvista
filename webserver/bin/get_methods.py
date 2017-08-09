#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import logging
import time

import tornado.gen
import tornado.httpclient
import tornado.httputil
import tornado.web

import config
import mongo_driver
import mysql_driver

# global variables
main_logger = logging.getLogger('main')

mysql_config = config.MysqlConfig()
mysql_info = {}
mysql_info["user"] = mysql_config.user
mysql_info["passwd"] = mysql_config.passwd
mysql_info['host'] = mysql_config.host
mysql_info['port'] = mysql_config.port
mysql_info['db'] = mysql_config.db
mysql_pool = mysql_driver.MysqlPool(mysql_info)

mongo_config = config.MongoConfig()
mongo_info = {}
mongo_info['host'] = mongo_config.host
mongo_info['port'] = mongo_config.port
mongo_pool = mongo_driver.MongoPool(mongo_info)


class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        client = mongo_pool.get_connection()
        document = client.local.startup_log.find_one()
        self.write(str(document))
        
        url = self.get_query_argument('url', 'http://www.baidu.com')

        try:
            http_client = tornado.httpclient.AsyncHTTPClient()
            response = yield http_client.fetch(url)
            self.write(response.body)
        except tornado.httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            main_logger.error('request (%s) failed, %s' % (url, str(e)))
        except Exception as e:
            # Other errors are possible, such as IOError.
            main_logger.error('request (%s) failed, %s' % (url, str(e)))

        http_client.close()
        self.finish()

    # @tornado.gen.coroutine
    # def post(self):
    #     headers = self.request.headers
    #     for (k,v) in sorted(headers.get_all()):
    #         print('%s: %s' % (k,v))
    #     body = self.request.body
    #     self.write(body)


class UserHandler(tornado.web.RequestHandler):
    def get(self):
        mysql = mysql_driver.Mysql(mysql_pool.get_connection())
        if mysql.is_valided():
            res = mysql.select("SELECT * FROM Groups")
            # if res:
            #     for r in res:
            #         self.write(str(r))
        mysql.close()

        client = mongo_pool.get_connection()
        document = client.local.startup_log.find_one()
        self.write(str(document))
