#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 10:31
# @Descript:

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件（比如配置文件）所在的路径

# 远程上传文件路径
_REMOTE_FOLDER = 'uploads'  # 获取当前用户目录，并建立uploads文件夹
# 本地临时保存文件路径
_UPLOAD_FOLDER = ''.join([basedir, '/app/static/uploads'])
# 上传文件大小限制
_MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16M，允许最大上传文件


# the secret key
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# configuration mysql--- for prodict
SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % ('root', 'root', '127.0.0.1', 'aops')

# mail address
MAILHOST = 'mail.autotest.com'
MAIL_SERVER = 'mail.autotest.com'
DEFAULT_MAIL_SENDER = 'mailtest@autotest.com'
MAIL_DEFAULT_SENDER = 'mailtest@autotest.com'
MAIL_USERNAME = 'mailtest'
MAIL_PASSWORD = 'yvtg45h5'
DEFAULT_MAIL_RECEIVER = "dd@autotest.com"
MAIL_RECEIVER = ["dd@autotest.com"]
MAIL_SUBJECT = "Fatal: Task: %s  fail num: %s! Please check task manage web, thanks!"
MAIL_BODY = "Please check: http://10.0.2.205:8080/task/%s/showstat_name/, thanks!"
#lan
ACCEPT_LANGUAGES = ['en', 'zh', 'en_gb']


# smsbao message
message_info = {
    'login_url': 'http://api.smsbao.com/sms',
    'query_url': 'http://www.smsbao.com/query',
    'user': 'zwhset',
    'passwd': '8ab497874b7e7afbb02e2f0441696f3b'
}

db_info = {
    'host': "127.0.0.1",
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'aops',
    'charset': 'utf8'
}
'''
0000 正确
1001 - 1999 用户类错误
2001 - 2050 smsbao短信宝错误信息
'''
_code = {
    0000: '成功',
    1001: '用户不存在',
    1002: '用户未激活',
    1003: '密码错误',
    1004: '用户名或密码不能为空',
    1005: '登录失败',
    1010: '请填写相应信息',
    1011: '手机号格式不正确',
    1012: '密码不一致',
    1013: '注册失败',
    1014: '手机号已注册，请更换手机号',
    1015: '查询用户时出错',
    1016: '用户激活失败',
    1017: '密码长度为6-20位',
    1018: '用户信息修改失败',

    2001: '短信发送失败',
    2002: '参数不全',
    2003: '短信发送失败，未知错误',
    2004: '发送失败，请联系管理员',
    2005: '短信查询失败',
    2006: '数据库写入失败，请联系管理员',
    2007: '数据库查询失败',
    2008: '查询条件不符',
    2009: '数据库连接异常，请联系管理员',
    2010: '修改失败',
    2011: '无修改记录',
    2012: '删除失败',
    2013: '请提交正确的URL地址',
    2014: '服务器不支持get/post以外的请求',
    2015: '执行远程命令失败',
    2016: '远程文件已存在',
    2017: '上传失败',

}
