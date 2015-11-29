#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import baseHandler
import hashlib
from modules.db import db
import datetime
import string
import constants

class LoginHandler(baseHandler.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        nick = self.get_body_argument('nick')
        password = self.get_body_argument('password')
        nick = nick.strip()
        if not nick or not password:
            self.write({'success': False, 'error_code': constants.error_code['miss_nick_or_password']})
            self.finish()
            return
        user = db.get('select id, nick, password from tb_user where nick = %s', nick)

        if user:
            md5 = hashlib.md5()
            md5.update(password)
            password_md5 = md5.hexdigest().upper()
            if user.password.upper() == password_md5:
                self.set_secure_cookie('current_user', nick, 10)
                self.write({'success': True, 'data': user})
                self.finish()
            else:
                self.write({'success': False, 'error_code': constants.error_code['wrong_password']})
                self.finish()
            return

        self.write({'success': False, 'error_code': constants.error_code['member_not_exist']})
        self.finish()

class SignupHandler(baseHandler.RequestHandler):
    def get(self):
        self.render('signup.html');

    def post(self):
        nick = self.get_body_argument('nick')
        password = self.get_body_argument('password')
        password_confirm = self.get_body_argument('password_confirm')
        invite_code = self.get_body_argument('invite_code')
        nick = nick.strip()
        if nick and password and password_confirm and invite_code:
            length = len(password)
            if length >= 6 and length <= 18 and password == password_confirm:
                query_exist = 'select count(1) count from tb_user where nick = %s'
                user_num = db.get(query_exist, nick)
                if user_num and user_num.count:
                    self.write({'success': False, 'error_code': constants.error_code['user_has_exist']})
                    self.finish()
                    return
                query_invite_code = 'select count(1) count from tb_invite where code = %s'
                code_num = db.get(query_invite_code, invite_code)
                if code_num and code_num.count:
                    md5 = hashlib.md5()
                    md5.update(password)
                    password_md5 = md5.hexdigest()
                    now = datetime.datetime.now()
                    insert_sql = 'insert into tb_user (nick, password, created) values (%s, %s, %s)'
                    try:
                        member_id = db.insert(insert_sql, nick, password_md5, now)
                        self.write({'success': True})
                        self.finish()
                        return
                    except:
                        pass
                        # TODO add log
                elif not code_num.count:
                    self.write({'success': False, 'error_code': constants.error_code['invite_code_not_exist']})
                    self.finish()
                    return

        self.write({'success': False})
        self.finish()

class LogoutHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        current_url = self.request.headers.get('Referer') or r'/'
        self.clear_cookie('current_user')
        self.redirect(current_url)

class ProfileHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, id):
        user = db.get('select id, nick, created, updated from tb_user where id = %s', id)
        if user:
            self.render('profile.html', user=user)

        raise tornado.web.HTTPError(404)

class SettingHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        query_category = 'select id, name from tb_category where user_id = %s'
        categories_id = []
        categories = db.query(query_category, str(self.current_user.id))
        if categories:
            for cate in categories:
                categories_id.append(str(cate.id))
        cate_post_count_mapper = []
        if categories_id:
            query_posts = 'select category_id, count(1) count from tb_post where category_id in {0} group by category_id'.format(tuple(categories_id))
            cate_post_count_mapper = db.query(query_posts)

        for cate in categories:
            for mapper in cate_post_count_mapper:
                cate['post_count'] = 0
                if mapper.category_id == cate.id:
                    cate['post_count'] = mapper.count

        self.render('setting.html', categories=categories)


