#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 10:38
# @Descript: 用户登录,注册
import base64
import random
import re

import time

import datetime
import traceback

from flask_login import UserMixin

import config
from app import login_manager
from app.common import db
from app.common.comm import DATE_NOW
from logger import Logger
from werkzeug.security import generate_password_hash, check_password_hash

logger = Logger()


class User(UserMixin):
    def __init__(self, **kwargs):
        super(User, self).__init__()
        self._db = db.DB()
        self._db_core = db.DBCore()
        self.nick_name = kwargs.get('nickName')
        self.mobile = kwargs.get('mobile')
        self.info = kwargs

    def check_mobile_format(self, mobile_email):
        """正则检查手机号,邮箱是否合格"""
        par = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}|[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+')
        # par = re.compile(r'^1[3578]\d{9}$|^147\d{8}')
        if par.match(mobile_email):
            return True
        else:
            return False

    def check_user_exits(self, nickName):
        """检查用户是否存在"""
        self.sql = "SELECT nickName FROM user_base WHERE nickName='{}'".format(nickName)
        result = self._db.db_select_on(self.sql)
        if result:
            return False  # 数据库中存在
        return True

    def check_mobile_exits(self, mobile):
        """检查手机号是否存在"""
        self.sql = "SELECT mobile FROM user_base WHERE mobile='{}'".format(mobile)
        result = self._db.db_select_on(self.sql)
        if result:
            return False  # 数据库中存在
        return True

    def user_status(self, nickName=None, mobile=None):
        """查询用户状态"""
        self.sql = "SELECT status FROM user WHERE nickName='{0}' OR mobile='{1}'".format(nickName, mobile)
        result = self._db.db_select_on(self.sql)
        if result:
            status = result[0]
            return status  # 用户状态
        logger.info('该用户不存在!')
        return None

    def verify_password(self, nickName=None, mobile=None, password=None):
        """用户密码校验"""
        passwd = self._db.md5(password)
        # passwd = generate_password_hash(password)
        # return check_password_hash(self.password_hash, passwd)
        sql = "SELECT mobile,passwd FROM user WHERE (nickName='{0}' OR mobile='{1}') AND passwd='{2}'".format(nickName, mobile, passwd)
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

    def login(self, **kwargs):
        if self.info:
            _info = self.info
        else:
            _info = kwargs

        sql = "SELECT nickName FROM user_base WHERE (nickName='{0}' OR mobile='{1}')AND passwd='{2}'".format(
            _info.get('nickName', ''), _info.get('mobile', ''), self._db.md5(_info.get('passwd', '')))
        res = self._db.db_select_on(sql)
        if res:
            result = {
                'code': '0000',
                'msg': config._code.get('0000'),
                'user': res,
            }
            return result
        return {
            'code': '1003',
            'msg': config._code.get('1003'),
        }

    def register(self, **kwargs):
        """用户注册"""
        if self.info:
            _info = self.info
        else:
            _info = kwargs

        nickName = _info.get('nickName')
        mobile = _info.get('mobile')
        if not self.check_user_exits(nickName):
            return False
        if not self.check_mobile_format(mobile):
            return False
        if not self.check_mobile_exits(mobile):
            return False
        passwd = _info.get('passwd')
        en_passwd = _info.get('en_passwd')
        if not self.check_passwd_len(passwd):
            return False
        if not self.check_enpasswd(passwd, en_passwd):
            return False
        try:
            sql = "INSERT INTO `pcode-passport`.`user_base` (nickName,mobile, passwd, registerTime) VALUES ('{0}','{1}','{2}','{3}')".format(
                nickName, mobile, self._db.md5(passwd), DATE_NOW)

            sql_core = "INSERT INTO `pcode-core`.`user_main` (nickName,mobile, passwd, registerTime) VALUES ('{0}','{1}','{2}','{3}')".format(
                nickName, mobile, self._db.md5(passwd), DATE_NOW)

            result = self._db.db_insert_on_no_commit(sql)
            _result = self._db.db_insert_on_no_commit(sql_core)

            if result and _result:
                self._db.db_commit()
                return True
            else:
                self._db.db_rollback()
                return False
        except Exception as e:
            logger.error('Error:{0}, {1}'.format(e, traceback.format_exc()))
            raise e


    def user_info(self, nickName=None, mobile=None):
        """用户信息查询"""
        sql = "SELECT * FROM user_base WHERE mobile='{}' OR nickName='{1}'".format(mobile, nickName)
        result = self._db.db_select_on(sql)
        if result:
            return result
        else:
            logger.error('该手机号不存在!')
            return None

    def user_modify(self, info):
        """用户信息修改"""
        sql = "UPDATE user_base SET nickName='{0}'WHERE mobile='{1}'".format(
            info['nickname'], info['mobile'])
        result = self._db.db_update_on(sql)
        if result in (0, 1):
            return True
        return False

    def user_passwd_modify(self, info):
        """用户密码修改"""
        nickName = info.get('nickName')
        mobile = info.get('mobile')
        old_passwd = info.get('old_passwd')
        if not self.verify_password(mobile, old_passwd):
            return False
        new_passwd = info.get('new_passwd')

        if not self.check_passwd_len(new_passwd):
            return False

        if self.check_enpasswd(old_passwd, new_passwd):
            logger.error('新密码不能与旧密码相同!')
            return False
        sql = "UPDATE user_base set passwd='{0}' WHERE (mobile='{1}' OR nickName='{2}') AND passwd='{3}'".format(
            self._db.md5(new_passwd), mobile, nickName, self._db.md5(old_passwd))
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
        """密码验证"""
        return check_password_hash(self.password_hash, password)

    def gen_token(self, uid):
        """生成token"""
        token = base64.b64encode(':'.join([str(uid), str(random.random()),
                                           str(time.time() + 7200)]))
        self.info[uid].append(token)
        return token

    def verify_token(self, token):
        """验证token"""
        _token = base64.b64decode(token)
        if not info.get(_token.split(':')[0])[-1] == token:
            return False
        if float(_token.split(':')[-1]) >= time.time():
            return True
        else:
            return False

    @staticmethod
    def authenticate(username, password):
        """
        验证用户
        :param username: 用户名或者电子邮件地址
        :param password: 用户密码

        user = User.query.filter(db.or_(User.username == username,
                                        User.email == username)).first()
        if isinstance(user, User):
            if user.verify_password(password):
                return None, user
            else:
                return 'Invalid Password', None
        return 'Invalid Username', None
        """
        sql = "SELECT * FROM user_base WHERE mobile='{0}' AND passwd='{1}'".format(username, User()._db.md5(password))
        result = User()._db.db_select_on(sql)
        print('result is {}'.format(result))
        if result:
            return None, result[0]
        else:
            return 'Invalid Username or Password', None

    @login_manager.user_loader
    def user_loader(self, id):
        """使用user_loader装饰器的回调函数,检查user对象是否为登录状态"""
        sql = "SELECT id FROM user WHERE id='{}'".format(id)
        user = self._db.db_select_on(sql)
        return user[0]


if __name__ == '__main__':
    mobile = '13720027401'
    info = {
        'nickName': 'wang',
        'mobile': '13720027402',
        'passwd': '111111',
        'en_passwd': '111111'
    }
    user = User()
    # print(user.check_user_exits(user.mobile))
    # result = user.user_status(user.mobile)
    # result = user.verify_password(mobile,'111111')
    # result = user.check_enpasswd(info)

    # result = user.user_passwd_modify(info)
    # result = user.user_info(mobile)
    # result = user.login(**info)
    result = user.register(**info)
    # print('{0},{1}'.format(result['code'], result['msg']))
    print(result)
