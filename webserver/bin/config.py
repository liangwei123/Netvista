#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import ConfigParser
import logging
import os


# global variables
main_logger = logging.getLogger('main')


class WebServerConfig():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.getcwd() + "/config/webserver.conf")

        # WEBSERVER
        self.port = config.getint("WEBSERVER", "port")


class MysqlConfig():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.getcwd() + "/config/webserver.conf")

        # MYSQL
        self.host = config.get("MYSQL", "host")
        self.port = config.getint("MYSQL", "port")
        self.user = config.get("MYSQL", "user")
        self.passwd = config.get("MYSQL", "passwd")
        self.db = config.get("MYSQL", "db")


class MongoConfig():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.getcwd() + "/config/webserver.conf")

        # MONGO
        self.host = config.get("MONGO", "host")
        self.port = config.getint("MONGO", "port")


if __name__ == "__main__":
    import os
    import logging.config
    logging.config.fileConfig(os.getcwd() + '/config/logging.conf')

    WebServerConfig()
    MysqlConfig()
    MongoConfig()
