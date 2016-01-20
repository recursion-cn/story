#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2015/10/28

import baseHandler
from modules.db import db
import modules.utils
from models.Post import Post
from models.Category import Category
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import tornado.web
import tornado.ioloop
import tornado.concurrent
import tornado.gen
from settings import settings
import json
import constants

class BaseListHandler(baseHandler.RequestHandler):

    executor = ThreadPoolExecutor(3)
    io_loop = tornado.ioloop.IOLoop.current()

    # 'post' or 'draft'
    def init_post_type(self, type='post'):
        self.post_type = type

    @tornado.concurrent.run_on_executor
    def fetch_categories(self):
        return Category.list(self.current_user.id)

    @tornado.concurrent.run_on_executor
    def fetch_posts(self, user_id, cate_id, size):
        if self.post_type == 'post':
            if cate_id:
                return Post.list_by_category(user_id, int(cate_id), 0, int(size))
            return Post.list(user_id, 0, int(size))
        else:
            if cate_id:
                return Post.drafts_by_category(user_id, int(cate_id), 0, int(size))
            return Post.drafts(user_id, 0, int(size))

    @tornado.concurrent.run_on_executor
    def get_count(self, user_id, cate_id, size):
        if self.post_type == 'post':
            if cate_id:
                return Post.count_posts_by_category(user_id, cate_id)
            return Post.count_posts(user_id)
        else:
            if cate_id:
                return Post.count_drafts_by_category(user_id, cate_id)
            return Post.count_drafts(user_id)

"""
get the current user's posts list, need login.
@return posts list
"""
class ListHandler(BaseListHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        super(ListHandler, self).init_post_type()
        default_size = 100
        need_pagination = False
        cate_id = self.get_query_argument('cate', None)
        size = self.get_query_argument('size', default_size)
        user_id = self.current_user.id
        categories = yield tornado.gen.Task(self.fetch_categories)
        posts = yield tornado.gen.Task(self.fetch_posts, user_id, cate_id, size)
        count = yield tornado.gen.Task(self.get_count, user_id, cate_id, size)
        if posts:
            need_pagination = count > len(posts)
            for post in posts:
                post['author'] = self.current_user
                post['last_modified_cn'] = modules.utils.date_distance(post.last_modified)

        self.render('posts.html', cate_id=cate_id, categories=categories,
            posts=posts, page_size=size, need_pagination=int(need_pagination))

"""
get curent user's drafts, need login.
"""
class DraftListHandler(BaseListHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        super(DraftListHandler, self).init_post_type('draft')
        default_size = 100
        cate_id = self.get_query_argument('cate', None)
        size = self.get_query_argument('size', default_size)
        user_id = self.current_user.id
        categories = yield tornado.gen.Task(self.fetch_categories)
        drafts = yield tornado.gen.Task(self.fetch_posts, user_id, cate_id, size)
        count = yield tornado.gen.Task(self.get_count, user_id, cate_id, size)
        for draft in drafts:
            draft['author'] = self.current_user
            draft['last_modified_cn'] = modules.utils.date_distance(draft.last_modified)

        self.render('drafts.html', cate_id=cate_id, categories=categories, drafts=drafts)

class ListApiHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        res = {'data': None}
        need_pagination = False
        summary_length = 260
        offset = self.get_query_argument('offset', 0)
        size = self.get_query_argument('size', 10)
        user_id = self.current_user.id
        count = Post.count_posts(user_id)
        posts = Post.list(user_id, int(offset), int(size))
        if posts:
            need_pagination = count > (int(offset) + int(size))
            for post in posts:
                post['author'] = self.current_user
                post['last_modified_cn'] = modules.utils.date_distance(post.last_modified)

            data = {'posts': posts, 'need_pagination': need_pagination}

            self.send_result(True, data, None)

"""
get single post by id
"""
class PostHandler(baseHandler.RequestHandler):

    def get(self, id):
        read_mode = self.get_query_argument('mode', None)
        post = Post.get_post(id)
        if post:
            if not ord(post.public):
                if not self.current_user:
                    raise tornado.web.HTTPError(403)
                    return
                elif self.current_user.id != post.user_id:
                    raise tornado.web.HTTPError(403)
                    return
            query_author = 'select id, nick from tb_user where id = %s'
            author = db.get(query_author, post.user_id)
            post['author'] = author
        else:
            raise tornado.web.HTTPError(404)

        template_name = 'post.html'
        if self.is_mobile:
            template_name = 'read_focus.html'
        elif read_mode and read_mode == 'focus_read':
                template_name = 'read_focus.html'

        self.render(template_name, post=post)

"""
direct to the edit page
"""
class EditHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, post_id=None):
        user_id = self.current_user.id
        post = None
        if post_id:
            _post = Post.get_post(post_id)
            if _post and _post.user_id == user_id:
                post = _post
        get_categories = 'select id, name from tb_category where visible = 1 and user_id = %s'
        categories = db.query(get_categories, user_id)
        referer = self.request.headers.get('Referer') or '/'

        self.render('edit.html', categories=categories, post=post, referer=referer)

"""
make the post be public
"""
class ShareHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        post_id = self.get_body_argument('post_id', None)
        if post_id:
            query = 'select id, user_id from tb_post where id = %s and deleted = 0'
            _post = db.query(query)
            if _post and _post.id == post_id:
                update_public = 'update tb_post set public = 1 where id = %s'
                row_count = db.update(update_public, post_id)
                if row_count:
                    self.send_result(True, error_code=None)
                    return
                self.send_result()
                return
        self.send_result(error_code=constants.error_code['missing_parameters'])

"""
create new post or update an exist post
"""
class InsertOrUpdateHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        title = self.get_body_argument('title', None)
        content = self.get_body_argument('content', None)
        html_content = self.get_body_argument('html_content', None)
        category_id = self.get_body_argument('category', None)
        user_id = self.current_user.id
        post_public = self.get_body_argument('privacy', None)
        post_id = self.get_body_argument('id', -1)
        draft = self.get_body_argument('draft', 0)
        visible = 1 - int(draft)

        if title and content and category_id:
            now = datetime.now()
            if int(post_id) != -1:
                sql = 'update tb_post set title = %s, content = %s, html_content = %s, public = %s, visible = %s, category_id = %s, updated = %s where id = %s and deleted = 0'
                num = db.update(sql, title, content, html_content, int(post_public), int(visible), int(category_id), now, int(post_id))
            else:
                sql = 'insert into tb_post (title, content, html_content, user_id, category_id, public, visible, created) values (%s, %s, %s, %s, %s, %s, %s, %s)'
                num = db.insert(sql, title, content, html_content, long(user_id), int(category_id), int(post_public), int(visible), now)
            if num:
                self.send_result(True, error_code=None)
                return
            self.send_result()
            return
        self.send_result(error_code=constants.error_code['missing_parameters'])

"""
mark post as deleted
"""
class DeleteHandler(baseHandler.RequestHandler):
    def delete(self, post_id):
        if Post.pretend_delete(post_id):
            self.send_result(True, error_code=None)
            return
        self.send_result()

