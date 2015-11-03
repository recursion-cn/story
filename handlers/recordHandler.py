#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/28

import baseHandler
from modules.db import db

"""
get the records list
@return records list
"""
class ListHandler(baseHandler.RequestHandler):

    def get(self):
        query = 'select id, title, content, created, updated from tb_post where visible = 1'
        records = db.query(query)

        self.render('index.html', records=records)

"""
direct to the edit page
"""
class EditHandler(baseHandler.RequestHandler):

    def get(self, record_id=None):
        get_categories = 'select id, name from tb_category where visible = 1'
        categories = db.query(get_categories)

        self.render('edit.html', categories=categories)

"""
create new record/post
"""
class NewHandler(baseHandler.RequestHandler):

    def post(self):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')
        category_id = self.get_body_argument('category')
        pass
