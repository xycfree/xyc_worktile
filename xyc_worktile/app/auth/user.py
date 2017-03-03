#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 10:38
# @Descript: 用户登录,注册
import re

import config
from app.common import db
from logger import Logger
from werkzeug.security import generate_password_hash, check_password_hash

logger = Logger()


class User(object):
    def __init__(self, phone=None, **kwargs):
        self._db = db.DB()
        self.phone = phone
        self.info = kwargs

    def check_phone_format(self, phone_email):
        """正则检查手机号,邮箱是否合格"""
        par = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}|[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+')
        # par = re.compile(r'^1[3578]\d{9}$|^147\d{8}')
        if par.match(phone_email):
            return True
        else:
            return False

    def check_user_exits(self, phone):
        """检查用户是否存在"""
        self.sql = "SELECT phone FROM user WHERE phone={}".format(phone)
        result = self._db.db_select_on(self.sql)
        if result:
            return False  # 数据库中存在
        return True

    def user_status(self, phone):
        """查询用户状态"""
        self.sql = "SELECT status FROM user WHERE phone={}".format(phone)
        result = self._db.db_select_on(self.sql)
        if result:
            status = result[0]
            return status  # 用户状态
        logger.info('该用户不存在!')
        return None

    def verify_password(self, phone, password):
        """用户密码校验"""
        passwd = self._db.md5(password)
        # passwd = generate_password_hash(password)
        # return check_password_hash(self.password_hash, passwd)
        sql = "SELECT phone,passwd FROM user WHERE phone='{0}' AND passwd='{1}'".format(phone, passwd)
        result = self._db.db_select_on(sql)
        if result:
            return True
        logger.info('用户名或密码错误!')
        return False

    def check_enpasswd(self, passwd, en_passwd):
        """密码是否一致"""
        if passwd == en_passwd:
            return True
        return False

    def check_passwd_len(self, passwd):
        """密码长度大于等于6,小于等于20位"""
        if len(passwd) > 20 or len(passwd) < 6:
            logger.error('密码长度为6-20位,请重新设置!')
            return False
        return True

    def login(self, info):
        sql = "SELECT nickname FROM user WHERE phone='{0}' AND passwd='{1}'".format(
            info['phone'], self._db.md5(info['passwd']))
        res = self._db.db_select_on(sql)
        if res:
            result = {
                'code': '0000',
                'msg': config._code.get('0000'),
                'uname': res[0]
            }
            return result
        return {
            'code': '1003',
            'msg': config._code.get('1003'),
        }

    def register(self, info):
        """用户注册"""
        phone = info['phone']
        if not self.check_phone_format(phone):
            return False
        if not self.check_user_exits(phone):
            return False
        passwd = info['passwd']
        en_passwd = info['en_passwd']
        if not self.check_passwd_len(passwd):
            return False
        if not self.check_enpasswd(passwd, en_passwd):
            return False
        sql = "INSERT INTO user(phone, passwd, status,role) VALUES ('{0}','{1}','{2}','{3}')".format(
            phone, self._db.md5(passwd), '0', '100')
        result = self._db.db_insert_on(sql)
        if result:
            return True
        return False

    def user_info(self, phone):
        """用户信息查询"""
        sql = "SELECT * FROM user WHERE phone='{}'".format(phone)
        result = self._db.db_select_on(sql)
        if result:
            return result
        else:
            logger.error('该手机号不存在!')
            return None

    def user_modify(self, info):
        """用户信息修改"""
        sql = "UPDATE user SET nickname='{0}',age='{1}' WHERE phone='{2}'".format(
            info['nickname'], info['age'], info['phone'])
        result = self._db.db_update_on(sql)
        if result in (0, 1):
            return True
        return False

    def user_passwd_modify(self, info):
        """用户密码修改"""
        phone = info.get('phone')
        old_passwd = info.get('old_passwd')
        if not self.verify_password(phone, old_passwd):
            return False
        new_passwd = info.get('new_passwd')

        if not self.check_passwd_len(new_passwd):
            return False

        if self.check_enpasswd(old_passwd, new_passwd):
            logger.error('新密码不能与旧密码相同!')
            return False
        sql = "UPDATE user set passwd='{0}' WHERE phone='{1}' AND passwd='{2}'".format(
            self._db.md5(new_passwd), phone, self._db.md5(old_passwd))
        result = self._db.db_update_on(sql)
        if result:
            return True
        return False

    @property
    def password(self):
        """没有读取的属性"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """只有赋值写的属性，加密"""
        self.password_hash = generate_password_hash(password)

    def verify_password_(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == '__main__':
    phone = '13720027400'
    info = {
        'phone': '13720027401',
        'passwd': '111111',
        'en_passwd': '111111'
    }
    user = User(phone)
    # print(user.check_user_exits(user.phone))
    # result = user.user_status(user.phone)
    # result = user.verify_password(phone,'111111')
    # result = user.check_enpasswd(info)

    # result = user.user_passwd_modify(info)
    # result = user.user_info(phone)
    # result = user.login(info)
    result = user.register(info)
    print(result)
