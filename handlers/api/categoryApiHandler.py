#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2016/01/16

import baseApiHandler
from models.Category import Category
import modules.utils
import datetime
from concurrent.futures import ThreadPoolExecutor
import tornado.web
import tornado.ioloop
import tornado.concurrent
import tornado.gen
from settings import settings
import json
import constants

class CategoryListHandler(baseApiHandler.RequestHandler):
    executor = ThreadPoolExecutor(3)
    io_loop = tornado.ioloop.IOLoop.current()

    @tornado.concurrent.run_on_executor
    def fetch_categories(self):
        return Category.list(self.current_user.id)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        categories = yield tornado.gen.Task(self.fetch_categories)
        self.send_result(True, categories, None)