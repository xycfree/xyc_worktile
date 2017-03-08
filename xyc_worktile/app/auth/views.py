#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/3 11:36
# @Descript:
import base64

from flask import flash
from flask import g
from flask import request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required

from app.auth import auth
from app.auth.user import User


@auth.route("/")
# @login_required
def index():
    return render_template('index.html')


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    res = {}
    if request.method == 'POST':
        info = request.form.to_dict()
        remember = eval(info.get('remember_me')) if info.get('remember_me') else False
        user = User(**info)
        result = user.login()
        # msg,user = user.authenticate(info['phone'], info['passwd'])
        # print('msg is :{0}\nuser is {1}'.format(msg, user))
        if result['code'] == '0000':
            # if user:
            #     login_user(user)  # 在用户会话时把用户标记为登录
            session['mobile'] = info['mobile']
            flash('login success')
            return redirect(url_for('main.index'))
        flash(result.get('msg'))
        res = result.get('msg')
    return render_template('auth/login.html', result=res)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    res = {}
    if request.method == 'POST':
        info = request.form.to_dict()
        user = User(**info)
        result = user.register()
        if result:
            flash('注册成功')
            return redirect(url_for('main.index'))
        res['msg'] = '注册失败'
        flash(res['msg'])
    return render_template('auth/register.html', result=res)


@auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    # logout_user()
    # 如果会话中有用户名就删除它。
    session.pop('mobile', None)
    flash('退出成功')
    return redirect(url_for('main.index'))
