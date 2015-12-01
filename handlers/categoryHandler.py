#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/11/27

import baseHandler
import tornado.web
from modules.db import db
import constants

class IsCategoryExistHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        category = self.get_query_argument('cate_name', None)
        if category:
            query_exist = 'select count(*) count from tb_category where name = %s and user_id = %s'
            num = db.get(query_exist, category, self.current_user.id)
            if num and num.count:
                self.write({'success': True, 'exist': True})
                self.finish()
                return
            elif not num.count:
                self.write({'success': True, 'exist': False})
                self.finish()
                return
        self.write({'success': False, 'error_code': constants.error_code['missing_parameters']})
        self.finish()

class AddHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        category = self.get_body_argument('cate_name')
        if category:
            query_exist = 'select count(*) count from tb_category where name = %s and user_id = %s'
            num = db.get(query_exist, category, self.current_user.id)
            if num and num.count:
                self.write({'success': False, 'error_code': constants.error_code['category_already_exist']})
                self.finish()
                return
            query_new = 'insert into tb_category (name, user_id, visible) values (%s, %s, %s)'
            id = db.insert(query_new, category, self.current_user.id, 1)
            if id:
                self.write({'success': True, 'category_id': id})
                self.finish()

class BatchDeleteHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        categories = self.get_body_argument('categories')
        print categories