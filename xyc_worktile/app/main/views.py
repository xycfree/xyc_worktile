#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/3 16:00
# @Descript:
from flask import abort
from flask import current_app
from flask import make_response
from flask import render_template
from flask import request
from requests import session

from app.main import main


@main.route('/index/', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'



