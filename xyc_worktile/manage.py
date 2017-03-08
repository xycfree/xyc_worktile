#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 10:31
# @Descript:
import os

from app import create_app
from flask_script import Manager, Shell

app = create_app('default')
# manager = Manager(app)


if __name__ == '__main__':
    # manager.run()
    app.run(host='0.0.0.0',port=8000)