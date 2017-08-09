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

global AlertMonitoring,HomeBroadbandBusiness,ImportantBusiness
AlertMonitoring = {}
HomeBroadbandBusiness = {}
ImportantBusiness = {}

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

def LoadRelatedSystemProperty():
    mysql = mysql_driver.Mysql(mysql_pool.get_connection())
    if mysql.is_valided():
        SQL = "SELECT `propertyValue` FROM `relatedsystemproperty` WHERE propertyName='homeBroadband'"
        propertyValue = mysql.select(SQL)
        propertyValue = propertyValue[0]
        propertyValue = eval(propertyValue["propertyValue"])
        
        monitoringpropertyValue = propertyValue["monitoring"]
        AlertMonitoring["graphId"] = str(monitoringpropertyValue["GraphId"])
        AlertMonitoring["nodeCountAn"] = int(monitoringpropertyValue["AN"])
        AlertMonitoring["nodeCountMan"] = int(monitoringpropertyValue["MAN"])
        AlertMonitoring["nodeCountCmnet"] = int(monitoringpropertyValue["CMNET"])
        AlertMonitoring["nodeCountImportantBusiness"] = int(monitoringpropertyValue["importantBusiness"])
        AlertMonitoring["nodeCountThirdAndGame"] = int(monitoringpropertyValue["thirdAndGame"])
        AlertMonitoring["nodeCountWebsiteAndApp"] = int(monitoringpropertyValue["websiteAndApp"])
        AlertMonitoring["nodeCountOther"] = int(monitoringpropertyValue["other"])
        AlertMonitoring["groupIds"] = str(monitoringpropertyValue["groupIds"]).decode('utf-8')
        AlertMonitoring["filterAlert"] = str(monitoringpropertyValue["screen"]).decode('utf-8')
        AlertMonitoring["deviceTypeBusiness"] = str(monitoringpropertyValue["businessType"]).decode('utf-8')
        AlertMonitoring["deviceTypeNetwork"] = str(monitoringpropertyValue["netType"])
        
        jkBusinesspropertyValue = propertyValue["jkBusiness"]
        HomeBroadbandBusiness["graphId"] = str(jkBusinesspropertyValue["graphId"])
        HomeBroadbandBusiness["testIdWebpage"] = str(jkBusinesspropertyValue["testIdWebpage"])
        HomeBroadbandBusiness["testIdFlv"] = str(jkBusinesspropertyValue["testIdFlv"])
        HomeBroadbandBusiness["testIdGame"] = str(jkBusinesspropertyValue["testIdGame"])
        HomeBroadbandBusiness["firstPageTime"] = float(jkBusinesspropertyValue["standardFirstPageTime"]) * 1000.0
        HomeBroadbandBusiness["reachPercentGroup"] = float(jkBusinesspropertyValue["standardReachPercent"])
        HomeBroadbandBusiness["throughPutGroup"] = float(jkBusinesspropertyValue["standardThroughPut"]) * 1024.0
        HomeBroadbandBusiness["stallTimes"] = float(jkBusinesspropertyValue["standardStallTimes"])
        HomeBroadbandBusiness["avgBufferPercent"] = float(jkBusinesspropertyValue["standardAvgBufferPercent"])
        HomeBroadbandBusiness["avgDelay"] = float(jkBusinesspropertyValue["standardAvgDelay"]) * 1000.0
        HomeBroadbandBusiness["lossPercent"] = float(jkBusinesspropertyValue["standardLossPercent"])
        #HomeBroadbandBusiness["exTime"] = str(jkBusinesspropertyValue["exTime"])
        
        importantSecuritypropertyValue = propertyValue["importantSecurity"]
        ImportantBusiness["graphIdRadius"] = importantSecuritypropertyValue["graphId"]
        ImportantBusiness["testIdRadius"] = importantSecuritypropertyValue["radiusTestID"]
        ImportantBusiness["serverIpRadius"] = importantSecuritypropertyValue["radiusServerIP"]
        ImportantBusiness["testIdRadiusTcpPing"] = importantSecuritypropertyValue["radiusServerTcpPingID"]
        ImportantBusiness["testIdRadiusPing"] = importantSecuritypropertyValue["radiusServerPingTestID"]
        ImportantBusiness["destNodeIdRadiusTcpPing"] = importantSecuritypropertyValue["radiusServerTcpPingIDs"]
        ImportantBusiness["destNodeIdRadiusPing"] = importantSecuritypropertyValue["radiusServerPingTestNodeID"]
        ImportantBusiness["graphIdCache"] = importantSecuritypropertyValue["cacheTopologyID"]
        ImportantBusiness["testIdCache"] = importantSecuritypropertyValue["cacheTestID"]
        ImportantBusiness["cacheDevelopers"] = importantSecuritypropertyValue["cacheFriend"]
        ImportantBusiness["graphIdDns"] = importantSecuritypropertyValue["dnsTopologyID"]
        ImportantBusiness["testIdDns"] = importantSecuritypropertyValue["DNSTestID"]
        ImportantBusiness["destNodeIdHomeBroadband"] = importantSecuritypropertyValue["JKID"]
        ImportantBusiness["destNodeIdMobilePhone"] = importantSecuritypropertyValue["PhoneID"]
        ImportantBusiness["testIdOtt"] = importantSecuritypropertyValue["OTTTestID"]
        ImportantBusiness["testIdEpgTime"] = importantSecuritypropertyValue["testIdEpgTime"]
        ImportantBusiness["testIdDemandBufferTime"] = importantSecuritypropertyValue["testIdDemandBufferTime"]
        ImportantBusiness["dbUrlEpgTime"] = importantSecuritypropertyValue["dbUrlEpgTime"]
        ImportantBusiness["dbUrlDemandBufferTime"] = importantSecuritypropertyValue["dbUrlDemandBufferTime"]
        ImportantBusiness["dbUrlLiveMos"] = importantSecuritypropertyValue["dbUrlLiveMos"]
        ImportantBusiness["dbUrlStallTimes"] = importantSecuritypropertyValue["dbUrlStallTimes"]
        ImportantBusiness["liveMosAliasNames"] = importantSecuritypropertyValue["liveMosAliasNames"]
        
        main_logger.info('Get propertyValue finish...')
        
        print AlertMonitoring 
        print "\n"
        print HomeBroadbandBusiness
        print "\n"
        print ImportantBusiness
    mysql.close()


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
         
         
    
         if mysql.is_valided():
             #获取配置的内容
             SQL = "SELECT `propertyValue` FROM `relatedsystemproperty` WHERE propertyName='homeBroadband'"
             propertyValue = mysql.select(SQL)
             print '123'
             print propertyValue
             #main_logger.info(propertyValue)
             #print propertyValue[monitoring]
            # for r in propertyValue:
            #     self.write(str(r))
            #     self.write('\n')

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
