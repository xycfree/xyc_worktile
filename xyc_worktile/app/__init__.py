#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/2 9:59
# @Descript:
from flask import Flask
# from flask.ext.bootstrap import Bootstrap
from flask_login import LoginManager
# from flask.ext.pagedown import PageDown

from config import config

# bootstrap = Bootstrap()
# pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'basic'  # strong
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # db.init_app(app)
    login_manager.init_app(app)
    # pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
