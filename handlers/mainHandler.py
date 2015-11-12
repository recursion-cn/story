#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/17

import baseHandler
from modules.db import db
import markdown
import bleach
from bs4 import BeautifulSoup

"""
direct into the site index page or the corresponding user's posts list page
@param nick
"""
class IndexHandler(baseHandler.RequestHandler):

    def get(self, nick=None):
        posts = None
        if nick:
            select_user = 'select id, nick from tb_user where nick = %s'
            user = db.get(select_user, nick)
            if user:
                select_posts = """select id, title, content, user_id, category_id, created, updated,
                            if(updated is NULL, created, updated) as last_modified from tb_post where
                            user_id = %s and public = 1 and visible = 1
                        """
                posts = db.query(select_posts, user.id)
                for post in posts:
                    _html = markdown.markdown(post.content)
                    soup = BeautifulSoup(_html, 'html.parser')
                    _text = soup.get_text()
                    if _text and len(_text) > 200:
                        _text = _text[0:200] + '...'
                    post['summary'] = _text
                    post['author'] = user

        self.render('index.html', posts=posts, draft=None)
