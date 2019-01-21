# encoding=utf-8
# @Time    : 2018/9/24 下午1:35
from flask import render_template, Response, url_for, Blueprint, current_app
from jasmine_app.main.tasks import add
import logging

main = Blueprint('main', __name__)

import os


@main.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(current_app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@main.route('/')
def index():
    add.delay(2, 3)
    logging.log(level=logging.ERROR, msg='test error')
    return render_template('main/base.html')
