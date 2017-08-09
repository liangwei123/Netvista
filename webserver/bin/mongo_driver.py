#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import logging

import pymongo


# global variables
main_logger = logging.getLogger('main')


class MongoPool(object):
    def __init__(self, db_info={}):
        try:
            main_logger.info('create mongo connection pool({0})'.format(db_info))
            self._client = pymongo.MongoClient(host=db_info['host'],
                                               port=db_info['port'],
                                               minPoolSize=2,
                                               maxPoolSize=2)
        except Exception as e:
            main_logger.error(e)

    def __del__(self):
        self._client.close()

    def get_connection(self):
        return self._client

if __name__ == "__main__":
    import config
    mongo_config = config.MongoConfig()
    db_info = {}
    db_info['host'] = mongo_config.host
    db_info['port'] = mongo_config.port

    import os
    import logging.config
    logging.config.fileConfig(os.getcwd() + '/config/logging.conf')
    mongo = MongoPool(db_info)
    client = mongo.get_connection()
    document = client.local.startup_log.find_one()
    main_logger.info(document)
    client.close()
