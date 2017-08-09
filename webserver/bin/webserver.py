#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import logging
import logging.config
import os
import platform
import signal


def is_platform_windows():
    return 'Windows' in platform.system()


def is_platform_linux():
    return 'Linux' in platform.system()


# change dir
webserver_path = os.getcwd()
if is_platform_linux():
    webserver_path = os.path.dirname(webserver_path)
    os.chdir(webserver_path)

# logging must be initialize first
config_path = webserver_path + '/config/logging.conf'
logging.config.fileConfig(config_path)
main_logger = logging.getLogger('main')

import tornado.ioloop

import config
import methods 
from methods import mysql_pool
import mysql_driver
# global variables
global AlertMonitoring,HomeBroadbandBusiness,ImportantBusiness
AlertMonitoring = {}
HomeBroadbandBusiness = {}
ImportantBusiness = {}


def receive_signal(signum, stack):
    tornado.ioloop.IOLoop.current().stop()


def get_app():
    return tornado.web.Application([
        (r"/", methods.OnIndex),
        (r"/database", methods.OnDatabase),
        (r"/transfer", methods.OnTransfer),
        (r"/export", methods.OnExport),
        (r"/demo", methods.OnDemo),
        (r"/getHomeBroadbandDevicesAlertCount", methods.OnGetHomeBroadbandDevicesAlertCount),
    ])


if __name__ == "__main__":
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    main_logger.info('server start...')
    webserver_config = config.WebServerConfig()
    LoadRelatedSystemProperty()
    get_app().listen(webserver_config.port)
    tornado.ioloop.IOLoop.current().start()

    main_logger.info('server stop...')
