#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/17

import tornado.web
import baseHandler
from modules.db import db
import markdown
import bleach
from bs4 import BeautifulSoup
import datetime

"""
direct into the site index page or the corresponding user's posts list page
@param nick
"""
class IndexHandler(baseHandler.RequestHandler):

    def get(self, nick=None):
        posts = None
        if not nick:
            #self.render('index.html')
            self.redirect('/posts')
            return

        select_user = 'select id, nick from tb_user where nick = %s'
        user = db.get(select_user, nick)
        if user:
            defaultSize = 10
            needPagination = False
            size = self.get_query_argument('size', defaultSize)
            count_posts = 'select count(1) count from tb_post where visible = 1 and deleted = 0 and public = 1 and user_id = %s'
            _count = db.get(count_posts, user.id)
            count = _count.count
            select_posts = """select id, title, content, user_id, category_id, created, updated,
                        if(updated is NULL, created, updated) last_modified from tb_post where
                        user_id = %s and public = 1 and visible = 1 order by last_modified desc limit 0, %s
                    """
            posts = db.query(select_posts, user.id, int(size))
            if posts:
                needPagination = True if count > len(posts) else False
                for post in posts:
                    _html = markdown.markdown(post.content)
                    soup = BeautifulSoup(_html, 'html.parser')
                    _text = soup.get_text()
                    if _text and len(_text) > 200:
                        _text = _text[0:200] + '...'
                    post['summary'] = _text
                    post['author'] = user

            self.render('main.html', user=user, posts=posts, pageSize=size, needPagination=int(needPagination))

class InviteHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        query_invite_record = 'select id, invitee_id, code, invitee_email, created from tb_invite where inviter_id = %s'
        records = db.query(query_invite_record, self.current_user.id)
        self.render('invite.html', records=records)

class InviteGenerateHandler(baseHandler.RequestHandler):
    def get(self):
        pass


