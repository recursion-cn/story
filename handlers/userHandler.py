#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import hashlib
import json
import datetime
import string
import baseHandler
from models.Member import Member
from modules.db import db
from modules import utils
import constants

class ConsoleHandler(baseHandler.RequestHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.render('console.html')

class LoginHandler(baseHandler.RequestHandler):
    def get(self):
        if self.current_user:
            referer = self.request.headers.get('Referer') or '/'
            print referer
            if referer.find('signup') > -1:
                referer = '/'
            self.redirect(referer)
            return
        self.render('login.html')

    def post(self):
        nick = self.get_body_argument('nick', None)
        password = self.get_body_argument('password', None)
        if not nick or not password:
            self.send_result(error_code=constants.error_code['miss_nick_or_password'])
            return
        user = Member.getByNick(nick)

        if user:
            md5 = hashlib.md5()
            md5.update(password)
            password_md5 = md5.hexdigest().upper()
            if user.password.upper() == password_md5:
                self.set_secure_cookie('current_user', nick, 10)
                user = json.dumps(user, cls=utils.JSONEncoder)
                self.send_result(True, user, error_code=None)
            else:
                self.send_result(error_code=constants.error_code['wrong_password'])
            return

        self.send_result(error_code=constants.error_code['member_not_exist'])

class SignupHandler(baseHandler.RequestHandler):
    def get(self):
        self.render('signup.html');

    def post(self):
        nick = self.get_body_argument('nick', None)
        password = self.get_body_argument('password', None)
        password_confirm = self.get_body_argument('password_confirm', None)
        invite_code = self.get_body_argument('invite_code', None)
        if nick and password and password_confirm and invite_code:
            length = len(password)
            if length >= 6 and length <= 18 and password == password_confirm:
                if Member.isExist(nick):
                    self.send_result(error_code=constants.error_code['user_has_exist'])
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
                        self.send_result(True, error_code=None)
                        return
                    except:
                        pass
                        # TODO add log
                elif not code_num.count:
                    self.send_result(error_code=constants.error_code['invite_code_not_exist'])
                    return

        self.send_result()

class LogoutHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        current_url = self.request.headers.get('Referer') or r'/'
        self.clear_cookie('current_user')
        self.redirect(current_url)

class ProfileHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, id):
        member = Member.getById(id)
        if member:
            self.render('profile.html', user=member)

        raise tornado.web.HTTPError(404)

class PasswordModifyHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        old_password = self.get_body_argument('old_password', None)
        new_password = self.get_body_argument('new_password', None)
        new_password_confirm = self.get_body_argument('new_password_confirm', None)
        if old_password and new_password and new_password_confirm:
            if len(new_password) >= 6 and len(new_password) <= 18:
                if new_password == new_password_confirm:
                    md5 = hashlib.md5()
                    md5.update(old_password)
                    password_md5 = md5.hexdigest().upper()
                    query_user = 'select password from tb_user where nick = %s'
                    user = db.get(query_user, self.current_user.nick)
                    if user.password.upper() == password_md5:
                        md5 = hashlib.md5()
                        md5.update(new_password)
                        new_password_md5 = md5.hexdigest().upper()
                        update_user = 'update tb_user set password = %s where nick = %s'
                        row = db.update(update_user, new_password_md5, self.current_user.nick)
                        if row:
                            self.send_result(True, error_code=None)
                            return
                        self.send_result()
                        return
                    self.send_result(error_code=constants.error_code['wrong_password'])
                    return
                self.send_result(error_code=constants.error_code['password_confirm_failed'])
                return
            self.send_result(error_code=constants.error_code['illegal_password'])
            return
        self.send_result(error_code=constants.error_code['missing_parameters'])


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
        if len(categories_id) > 1:
            query_posts = 'select category_id, count(1) count from tb_post where category_id in {0} group by category_id'.format(tuple(categories_id))
        elif len(categories_id) == 1:
            query_posts = 'select category_id, count(1) count from tb_post where category_id = {0}'.format(int(categories_id[0]))
        cate_post_count_mapper = db.query(query_posts)

        for cate in categories:
            for mapper in cate_post_count_mapper:
                cate['post_count'] = 0
                if mapper.category_id == cate.id:
                    cate['post_count'] = mapper.count

        self.render('setting.html', categories=categories)


