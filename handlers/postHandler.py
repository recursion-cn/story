#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/28

import baseHandler
from modules.db import db
import datetime

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

    def post(self, user_id=1):
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')
        category_id = self.get_body_argument('category')
        is_draft = self.get_body_argument('draft')

        if title and content and category_id:
            sql = 'insert into tb_post (title, content, user_id, category_id, visible, created) values (%s, %s, %s, %s, %s, %s)'
            now = datetime.datetime.now()
            post_id = db.insert(sql, title, content, long(user_id), int(category_id), int(is_draft), now)
            if post_id:
                self.write({'success': True})
                self.finish()
                return
            self.write({'success': False})
            self.finish()
            return
        self.write({'success': False})
        self.finish()
