#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 10:38
# @Descript: 用户登录,注册
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.common import db
from logger import Logger
from werkzeug.security import generate_password_hash, check_password_hash

logger = Logger()


class User(object):
    def __init__(self, phone, info=None):
        self._db = db.DB()
        self.phone = phone
        self.info = info

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
        sql = "SELECT phone,passwd FROM user WHERE phone='{0}' AND passwd='{1}'".format(phone, passwd)
        # return check_password_hash(self.password_hash, passwd)
        result = self._db.db_select_on(sql)
        if result:
            return True
        logger.info('用户名或密码错误!')
        return False

    def check_enpasswd(self, passwd, enpasswd):
        if passwd.strip() == enpasswd.strip():
            return True
        return False

    def check_pass_len(self):
        pass

    def login(self):
        pass

    def register(self, user_info={}):
        pass

    def user_info(self, phone):
        """用户信息查询"""
        pass

    def user_edit(self, user_info=None):
        """用户信息修改"""
        pass

    def user_passwd_edit(self, info):
        phone = info.get('phone')
        old_passwd = info.get('old_passwd')
        if self.verify_password(phone, old_passwd):
            new_passwd = info.get('new_passwd')
            if len(new_passwd) > 20 or len(new_passwd) < 6:
                logger.error('密码长度为6-20位,请重新设置!')
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



#     def generate_confirmation_token(self, expiration=3600):
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'confirm': self.id})
#
#     def confirm(self, token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#         if data.get('confirm') != self.id:
#             return False
#         self.confirmed = True
#         db.session.add(self)
#         return True
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     """加载用户的回调函数"""
#     return User.query.get(int(user_id))


if __name__ == '__main__':
    phone = '13720027400'
    info = {
        'phone': '13720027400',
        'old_passwd': '111111',
        'new_passwd': '111111'
    }
    user = User(phone)
    # print(user.check_user_exits(user.phone))
    # result = user.user_status(user.phone)
    # result = user.verify_password(phone,'111111')
    # result = user.check_enpasswd(info)

    result = user.user_passwd_edit(info)
    print(result)
