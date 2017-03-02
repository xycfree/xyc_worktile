#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-11 17:17:20
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from __future__ import print_function
import os
import MySQLdb
import hashlib
import random
import base64
import sys
import config

reload(sys)
sys.setdefaultencoding('utf-8')


class DB(object):
    def __init__(self):
        # 初始化 数据库连接 对象
        self.__connection = __import__("app.common.db_connect", fromlist=True)  # 反射 , fromlist=True
        self.__connect = getattr(self.__connection, "DbConnect")()
        self.__conn, self.__cur = self.__connect.get_conn()

    def db_object(self):
        ''' 数据库连接对象 '''
        db_info = config.db_info
        try:
            conn = MySQLdb.connect(**db_info)
            cur = conn.cursor()
            return conn, cur

        except Exception as e:
            raise e
        finally:
            pass

    # 条件查询
    def db_select_on(self, query):
        '''
        数据库条件查询
        '''
        try:
            # cur = self.db_object()[1]
            self.__cur.execute(query)
            row = self.__cur.fetchone()
            return row
        except Exception as e:
            print("Mysql Error {arg0}:{arg1}".format(arg0=e.args[0], arg1=e.args[1]))
            return None

    # 模糊全部
    def db_select_all(self, query):
        '''
        数据库模糊查询
        '''
        # cur = self.db_object()[1]
        try:
            self.__cur.execute(query)
            row = self.__cur.fetchall()
            return row
        except Exception as e:
            print ("Mysql Error {arg0}:{arg1}".format(arg0=e.args[0], arg1=e.args[1]))
            return None

    # 单条插入，成功返回1，失败返回None
    def db_insert_on(self, query=None, args=None):
        # conn, cur = self.db_object()
        try:
            if args:
                result = self.__cur.execute(query, args)
                self.__conn.commit()
            else:
                result = self.__cur.execute(query)
                self.__conn.commit()
            return result
        except MySQLdb.Error as e:
            return "Mysql Error {arg0}:{arg1}".format(arg0=e.args[0], arg1=e.args[1])

    # 多条插入，成功返回count，失败返回None
    def db_insert_many(self, query=None, args=None):
        # conn, cur = self.db_object()
        try:
            if args:
                result = self.__cur.executemany(query, args)
                self.__conn.commit()
            else:
                result = self.__cur.executemany(query)
                self.__conn.commit()
            return result
        except MySQLdb.Error as e:
            return "Mysql Error {arg0}:{arg1}".format(arg0=e.args[0], arg1=e.args[1])

    # 更新，成功返回1，更新未改动返回0；
    def db_update_on(self, query=None, args=None):
        # conn, cur = self.db_object()
        try:
            if args:
                result = self.__cur.execute(query, args)
                self.__conn.commit()
            else:
                result = self.__cur.execute(query)
                self.__conn.commit()
            return result
        except MySQLdb.Error as e:
            print('Mysql Error {arg0}:{arg1}'.format(arg0=e.args[0], arg1=e.args[1]))
            return None

    # 删除，成功返回1，更新未改动返回0；
    def db_delete_on(self, query, args=None):
        # conn, cur = self.db_object()
        try:
            if args:
                result = self.__cur.execute(query, args)
                self.__conn.commit()
            else:
                result = self.__cur.execute(query)
                self.__conn.commit()
            return result
        except MySQLdb.Error as e:
            print('Mysql Error {arg0}:{arg1}'.format(arg0=e.args[0], arg1=e.args[1]))
            return None

    def db_close(self):
        # conn, cur = self.db_object()
        self.__cur.close()
        self.__conn.close()

    @staticmethod
    def md5(strs):
        """MD5加密"""
        # import hashlib
        m = hashlib.md5()  # 创建md5对象 m = hashlib.md5(strs)
        m.update(strs)  # 生成机密串
        pwd = m.hexdigest()  # 获取加密串
        return pwd

    # 获取一个固定长度的随机串
    @staticmethod
    def get_randNum(p):
        # 密码字符串池
        pwdStrPool = '0123456789abcdefghijkmnpqrstuvwxyz~@#$%^&*()_+' \
                     'ABCDEFGHIJKMNPQRSTUVWXYZ'
        # 密码字符串池长度
        pwdStrPoolSize = len(pwdStrPool)
        # 定义要生成的密码长度
        pwdLen = [16, 16]
        randStr = ''
        for i in range(p):
            randNum = random.randint(0, pwdStrPoolSize - 1)
            randStr += pwdStrPool[randNum]
        return randStr

    @staticmethod
    def base64_encode(strs):
        """base64加密"""
        str_encode = base64.encodestring(strs)
        return str_encode

    @staticmethod
    def base64_decode(strs):
        """base64解密"""
        str_decode = base64.decodestring(strs)
        return str_decode


if __name__ == '__main__':
    db = DB()
    sql = 'select * from user'
    # conn, cur = db.get_conn()
    # cur.execute('select * from user')
    # record = cur.fetchall()
    print(db.db_select_all(sql))
    print(db.md5('111111'))
