#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/17

import tornado.web
import baseHandler
from modules.db import db
from models.Post import Post
import markdown
import bleach
from bs4 import BeautifulSoup
import datetime
import random
import constants

"""
direct into the site index page or the corresponding user's posts list page
@param nick
"""
class IndexHandler(baseHandler.RequestHandler):

    def get(self, nick=None):
        posts = None
        if not nick:
            self.redirect('/posts')
            return

        select_user = 'select id, nick from tb_user where nick = %s'
        user = db.get(select_user, nick)
        if user:
            default_size = 10
            summary_length = 200
            need_pagination = False
            size = self.get_query_argument('size', default_size)
            count = Post.count_posts(user.id)
            posts = Post.list(user.id, 0, default_size)
            if posts:
                need_pagination = count > len(posts)
                for post in posts:
                    _html = markdown.markdown(post.content)
                    soup = BeautifulSoup(_html, 'html.parser')
                    img = soup.find('img')
                    if img:
                        img['class'] = 'inner-img-limit'
                    _text = soup.get_text()
                    if _text and len(_text) > summary_length:
                        _text = _text[0:summary_length] + '...'
                    post['cover'] = img
                    post['summary'] = _text
                    post['author'] = user

            self.render('main.html', user=user, posts=posts,
                page_size=size, need_pagination=int(need_pagination))

class InviteHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        query_invite_record = 'select id, invitee_id, code, created, used from tb_invite where inviter_id = %s'
        records = db.query(query_invite_record, self.current_user.id)
        self.render('invite.html', records=records)

class InviteGenerateHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        count_code = 'select count(1) count from tb_invite where inviter_id = %s and used = 0'
        count_obj = db.get(count_code, self.current_user.id)
        if count_obj.count >= 3:
            self.send_result(error_code=constants.error_code['invitation_reached_limit'])
            return
        code = ''
        for i in range(8):
            code += str(random.randint(0, 9))
        insert_code = 'insert into tb_invite (inviter_id, code, created, used) values (%s, %s, %s, %s)'
        id = db.insert(insert_code, self.current_user.id, code, datetime.datetime.now(), 0)
        if id:
            self.send_result(True, code, None)
            return
        self.send_result()


