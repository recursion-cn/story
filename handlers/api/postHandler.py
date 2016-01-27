#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/12/03

import apiHandler
from modules.db import db
from models.Post import Post
import modules.utils
import datetime
import tornado.web
import tornado.gen
from markdown import markdown
import bleach
from bs4 import BeautifulSoup
from settings import settings
import json
import constants

class ListHandler(apiHandler.RequestHandler):

    @tornado.gen.coroutine
    def fetch_posts(self, offset, size):
        return Post.count_posts(self.current_user['id']), Post.list(self.current_user['id'], int(offset), int(size))

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        res, need_pagination, summary_length = {'data': None}, False, 150
        offset = self.get_query_argument('offset', 0)
        size = self.get_query_argument('size', 10)
        count, posts = yield tornado.gen.Task(self.fetch_posts, offset, size)
        if posts:
            need_pagination = count > (int(offset) + int(size))
            for post in posts:
                _html = markdown(post.content)
                soup = BeautifulSoup(_html, 'html.parser')
                img = soup.find('img')
                last_modified = post.last_modified
                if img:
                    img['class'] = 'inner-img-limit'
                _text = soup.get_text()
                if _text and len(_text) > summary_length:
                    _text = _text[0:summary_length] + '...'
                #post['cover'] = img
                post['summary'] = _text
                post['author'] = self.current_user
                post['last_modified_cn'] = modules.utils.date_distance(post.last_modified)

            data = {'posts': posts, 'need_pagination': need_pagination}

            self.send_result(True, data, None)

"""
get single post by id
"""
class PostHandler(apiHandler.RequestHandler):

    def get(self, id):
        post = Post.get_post(id)
        if post:
            if not ord(post.public):
                if not self.current_user:
                     self.write_error(403, '您没有该文章的阅读权限')
                     return
                elif self.current_user['id'] != post.user_id:
                    self.write_error(403, '您没有该文章的阅读权限')
                    return
            query_author = 'select id, nick from tb_user where id = %s'
            author = db.get(query_author, post.user_id)
            post['author'] = author
            post = json.dumps(post, cls=modules.utils.JSONEncoder)
            self.send_result(True, post, None)
            return

        self.write_error(404)

