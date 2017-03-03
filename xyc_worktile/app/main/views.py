#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/3 16:00
# @Descript:
from flask import render_template

from app.main import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
