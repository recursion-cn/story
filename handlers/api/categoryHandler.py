#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2016/01/16

import apiHandler
from models.Category import Category
import modules.utils
import tornado.web
import tornado.gen
import json
import constants

class CategoryListHandler(apiHandler.RequestHandler):

    @tornado.gen.coroutine
    def fetch_categories(self):
        return Category.list(self.current_user['id'])

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        categories = yield tornado.gen.Task(self.fetch_categories)
        self.send_result(True, categories, None)