#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 10:30
# @Descript:

from flask import Blueprint

auth = Blueprint('auth', __name__)
from . import user
from . import views
