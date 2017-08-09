#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import logging

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor


# global variables
main_logger = logging.getLogger('main')


class MysqlPool(object):
    _pool = None

    def __init__(self, db_info={}):
        try:
            main_logger.info('create mysql connection pool({0})'.format(db_info))
            self._pool = PooledDB(creator=pymysql,
                                    host=db_info['host'],
                                    port=db_info['port'],
                                    user=db_info['user'],
                                    passwd=db_info['passwd'],
                                    db=db_info['db'],
                                    charset='utf8',
                                    mincached=5,
                                    maxcached=5,
                                    maxshared=5,
                                    maxconnections=5,
                                    use_unicode=False,
                                    cursorclass=DictCursor)
        except Exception as e:
            main_logger.error(e)

    def __del__(self):
        self._pool.close()

    def get_connection(self):
        try:
            return self._pool.connection()
        except Exception as e:
            main_logger.warning('get connection failed')
            return False


class Mysql(object):
    _conn = None
    _cursor = None

    def __init__(self, connection):
        try:
            self._conn = connection
            if self._conn:
                self._cursor = self._conn.cursor()
        except Exception as e:
            main_logger.error(e)

    def execute(self, sql):
        return self._query(sql)

    def select(self, sql, param=None):
        count = self._query(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def update(self, sql, param=None):
        return self._query(sql, param)

    def delete(self, sql, param=None):
        return self._query(sql, param)

    def insert_one(self, sql, value):
        self._cursor.execute(sql, value)
        return self._get_insert_id()

    def insert_many(self, sql, values):
        count = self._cursor.executemany(sql, values)
        return count

    def _query(self, sql, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
        except Exception as e:
            main_logger.error("{0}, {1}".format(sql, e))
        return count

    def _get_insert_id(self):
        self._cursor.execute("SELECT @@IDENTITY AS `id`")
        result = self._cursor.fetchall()
        return result[0]['id']

    def close(self):
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            self._conn.close()
            self._conn = None

    def is_valided(self):
        valided = self._conn and self._cursor
        return valided


if __name__ == "__main__":
    import config
    mysql_config = config.MysqlConfig()
    db_info = {}
    db_info["user"] = mysql_config.user
    db_info["passwd"] = mysql_config.passwd
    db_info['host'] = mysql_config.host
    db_info['port'] = mysql_config.port
    db_info['db'] = mysql_config.db

    import os
    import logging.config
    logging.config.fileConfig(os.getcwd() + '/config/logging.conf')
    mysql_pool = MysqlPool(db_info)
    mysql = Mysql(mysql_pool.get_connection())
    if mysql.is_valided():
        res = mysql.select("SELECT * FROM Groups")
        if res:
            main_logger.info(res)
    mysql.close()
