#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 14:55
# @Descript:
import sys
import traceback

import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

import config
from logger import Logger

logger = Logger()


class DbConnect(object):
    def __init__(self):
        self.db_info = config.db_info

    def get_conn(self):
        try:
            self.conn = MySQLdb.connect(**self.db_info)
            self.cur = self.conn.cursor()
            return self.conn, self.cur
        except Exception as e:
            logger.error('{0},{1}'.format(e, traceback.format_exc()))
            raise e

    def db_close(self, conn, cur):
        cur.close()
        conn.close()


if __name__ == '__main__':
    db = DbConnect()
    conn, cur = db.get_conn()
    cur.execute('select * from user')
    record = cur.fetchall()
    print(len(record))
