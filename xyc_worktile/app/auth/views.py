#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/3 11:36
# @Descript:
from flask import flash
from flask import request, render_template, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required

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
        user = User()
        result = user.login(info)
        if result['code'] == '0000':
            # login_user(info['phone'], remember=remember, force=True)  # 在用户会话时把用户标记为登录
            session['phone'] = info['phone']
            # uname = result['uname']
            print('login success')
            return redirect(url_for('.index'))  # , name=uname
        flash(result['msg'])
        res = result
    return render_template('auth/login.html', result=res)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('main.index'))
