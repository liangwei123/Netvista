#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import logging
import StringIO
import time

import tornado.gen
import tornado.httpclient
import tornado.httputil
import tornado.web
import xlwt

import config
import mongo_driver
import mysql_driver

# global variables
global mongo_pool 
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
#from webserver import AlertMonitoring,HomeBroadbandBusiness,ImportantBusiness


class OnIndex(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            url = self.get_query_argument('url', 'http://www.baidu.com')
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

    @tornado.gen.coroutine
    def post(self):
        headers = self.request.headers
        for (k, v) in sorted(headers.get_all()):
            print('%s: %s' % (k, v))
        body = self.request.body
        print body
        self.write(body)
class OnGetHomeBroadbandDevicesAlertCount(tornado.web.RequestHandler):
    def get(self):
        mysql = mysql_driver.Mysql(mysql_pool.get_connection())
        nTotalQueryTime = 0
        nTotalResultCount = 0
        nErrorCode = 0
        nStart = self.get_query_argument('start',0,strip=True)
        nLimit = self.get_query_argument('limit',200,strip=True)
        nQueryType = self.get_query_argument('queryType',0,strip=True)
        nBeginTime = self.get_query_argument('beginTime',0,strip=True) * 1000000
        nEndTime = self.get_query_argument('endTime',0,strip=True) * 1000000
        nTimeInterval = self.get_query_argument('timeInterval',0,strip=True) * 1000000
        
        strFilterAlert = AlertMonitoring["filterAlert"]
        nAlertGroupIdAndDeviceType = AlertMonitoring["groupIds"].split(";")
        nAlertGroupIdToDeviceTypeMap = []
        GroupIdToDeviceTypeDict = {}
        #type后面的数字：1163，1161
        AlertGroupIdToDeviceType = []
        #保存如 CMNET
        AlertGroupIdToDeviceTypeMap = []
        for type in nAlertGroupIdAndDeviceType:
            second = type.split(":")
            AlertGroupIdToDeviceType.append(second[0])
            nAlertGroupIdToDeviceTypeMap.append(second[1])
            
        
        for type in nAlertGroupIdToDeviceTypeMap:
            if len(type)>1:
                second = type.split(",")
                for num in second:
                    AlertGroupIdToDeviceType.append(num)
            else:
                AlertGroupIdToDeviceType.append(type)
        #列表转化为字符串
        AlertGroupIdToDeviceType = ",".join(AlertGroupIdToDeviceType)
        if mysql.is_valided():
            for type in AlertGroupIdToDeviceTypeMap:
                SQL = "SELECT `id` FROM TestAlert WHERE `groupId` IN (%s) AND `extraConfig` LIKE '%%keyName\\\":\\\"device Type\\\",\\\"format\\\":\\\"\\\",""\\\"value\\\":\\\"%s%%'" % (AlertGroupIdToDeviceType,AlertGroupIdToDeviceTypeMap)
                sqlResult = mysql.select(SQL)
                #if len(sqlResult) < 0:
                #main_logger.info('query %s filed') % AlertGroupIdToDeviceTypeMap
                #continue
                GroupIdToDeviceTypeDict[str(AlertGroupIdToDeviceTypeMap)] = str(sqlResult)
        for nFirstTime in range(nBeginTime,nEndTime,nTimeInterval):
            for key in GroupIdToDeviceTypeDict:
                if len(GroupIdToDeviceTypeDict[key])==0:
                    continue
                strColumns = "  COUNT(`id`) AS `alertCount`"
                strConditions = " WHERE `alertId` IN (%s)" % str(GroupIdToDeviceTypeDict[key])
                SQL = "SELECT %s FROM TestAlertLog %s" % (strColumns,strConditions)
                #if len(strFilterAlert)>0:
                #    SQL = SQL + " AND TestAlertLog.`details` NOT LIKE \"%%%s%%\""" % (str(strFilterAlert))
                
                Result = mysql.select(SQL) 
                print Result
        mysql.close()
             


class OnDatabase(tornado.web.RequestHandler):
    def get(self):
        mysql = mysql_driver.Mysql(mysql_pool.get_connection())
        if mysql.is_valided():
            #res = mysql.select("SELECT * FROM Groups")
            res = mysql.select("SELECT * FROM `testalert` WHERE `groupId` IN (1162,1161,1163,1669,1164,1163,1602) AND `extraConfig` LIKE '%keyName\":\"device Type\",\"format\":\"\",\"value\":\"CMNET%'")
            if res:
                for r in res:
                    self.write(str(r))
        mysql.close()

        #client = mongo_pool.get_connection()
        #document = client.local.startup_log.find_one()
        #self.write(str(document))
class OnDemo(tornado.web.RequestHandler):
    def get(self):
        Name = self.get_query_argument('name',default='haha',strip=True)
        Age = self.get_query_argument('age',default='haha',strip=True)
        a={'A': [('wei', 12), ('we', 13)], 'error': '2'}
        self.write(a)
        




class OnTransfer(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        try:
            url = 'http://127.0.0.1:8080/'
            http_client = tornado.httpclient.AsyncHTTPClient()
            request = tornado.httpclient.HTTPRequest(url=url,
                                                     method='POST',
                                                     body=self.request.body)
            response = yield http_client.fetch(request)
        except tornado.httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            main_logger.error('request (%s) failed, %s' % (url, str(e)))
        except Exception as e:
            # Other errors are possible, such as IOError.
            main_logger.error('request (%s) failed, %s' % (url, str(e)))
        http_client.close()


class OnExport(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8')
        self.set_header('Content-Disposition','attachment;filename="export.xls"')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')

        ws.write(0, 0, u'北京')
        ws.write(1, 1, u'上海')
        ws.write(2, 2, u'广州')
        sio = StringIO.StringIO()
        wb.save(sio)
        self.write(sio.getvalue())


if __name__ == "__main__":
    style = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')

    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet('sheet1')

    row0 = [u'北京', u'上海', u'广州', u'深圳']
    row1 = [1, 2, 3, 4]

    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], style)
    
    for i in range(0, len(row1)):
        sheet1.write(1, i, row1[i], style)

    wb.save('example.xls')
