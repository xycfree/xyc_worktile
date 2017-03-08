#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/3/8 10:13
# @Descript:
from flask import make_response
from flask import render_template
from flask import request, jsonify

from app.main import main


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    resp = make_response(render_template('403.html'), 403)
    return resp


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    resp = make_response(render_template('404.html'), 404)
    return resp


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    resp = make_response(render_template('500.html'), 500)
    return resp
