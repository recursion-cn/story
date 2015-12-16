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
import datetime
import markdown
import bleach
from bs4 import BeautifulSoup
import tornado.web
from settings import settings
import json
import constants

"""
get the current user's posts list, need login.
@return posts list
"""
class ListHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        default_size = 10
        need_pagination = False
        cate_id = self.get_query_argument('cate', None)
        size = self.get_query_argument('size', default_size)
        categories = Category.list(self.current_user.id)
        if cate_id:
            posts = Post.list_by_category(self.current_user.id, int(cate_id), 0, int(size))
            count = Post.count_posts_by_category(self.current_user.id, cate_id)
        else:
            count = Post.count_posts(self.current_user.id)
            posts = Post.list(self.current_user.id, 0, int(size))
        if posts:
            need_pagination = True if count > len(posts) else False
            for post in posts:
                _html = markdown.markdown(post.content)
                soup = BeautifulSoup(_html, 'html.parser')
                _text = soup.get_text()
                if _text and len(_text) > 200:
                    _text = _text[0:200] + '...'
                post['summary'] = _text
                post['author'] = self.current_user

        self.render('posts.html', cate_id=cate_id, categories=categories, posts=posts, page_size=size, need_pagination=int(need_pagination))

"""
get curent user's drafts, need login.
"""
class DraftListHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        default_size = 10
        summary_length = 200
        size = self.get_query_argument('size', default_size)
        drafts = Post.drafts(self.current_user.id, 0, int(size))
        for draft in drafts:
            draft['author'] = self.current_user
            _html = markdown.markdown(draft.content)
            soup = BeautifulSoup(_html, 'html.parser')
            _text = soup.get_text()
            if _text and len(_text) > summary_length:
                _text = _text[0:summary_length] + '...'
            draft['summary'] = _text

        self.render('drafts.html', drafts=drafts)

class ListApiHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        res = {'data': None}
        need_pagination = False
        summary_length = 200
        offset = self.get_query_argument('offset', 0)
        size = self.get_query_argument('size', 10)
        count = Post.count_posts(self.current_user.id)
        posts = Post.list(self.current_user.id, int(offset), int(size))
        if posts:
            need_pagination = True if count > (int(offset) + int(size)) else False
            for post in posts:
                _html = markdown.markdown(post.content)
                soup = BeautifulSoup(_html, 'html.parser')
                _text = soup.get_text()
                if _text and len(_text) > summary_length:
                    _text = _text[0:summary_length] + '...'
                post['summary'] = _text
                post['author'] = self.current_user
            posts = json.dumps(posts, cls=modules.utils.JSONEncoder)
            res = {'res': {'data': posts, 'need_pagination': need_pagination}}

        self.write(res)
        self.finish()

"""
get single post by id
"""
class PostHandler(baseHandler.RequestHandler):

    def get(self, id):
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

        self.render('post.html', post=post)

"""
direct to the edit page
"""
class EditHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def get(self, post_id=None):
        post = None
        if post_id:
            _post = Post.get_post(post_id)
            if _post and _post.user_id == self.current_user.id:
                post = _post
        get_categories = 'select id, name from tb_category where visible = 1 and user_id = %s'
        categories = db.query(get_categories, self.current_user.id)
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
                    self.write({'success': True})
                    self.finish()
                    return
                self.write({'success': False, 'error_code': constants.error_code['internal_error']})
                self.finish()
                return
        self.write({'success': False, 'error_code': constants.error_code['missing_parameters']})
        self.finish()

"""
create new post or update an exist post
"""
class InsertOrUpdateHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        title = self.get_body_argument('title', None)
        content = self.get_body_argument('content', None)
        category_id = self.get_body_argument('category', None)
        user_id = self.current_user.id
        post_public = self.get_body_argument('privacy', None)
        post_id = self.get_body_argument('id', -1)
        draft = self.get_body_argument('draft', 0)
        visible = 1 - int(draft)

        if title and content and category_id:
            now = datetime.datetime.now()
            if int(post_id) != -1:
                sql = 'update tb_post set title = %s, content = %s, public = %s, visible = %s, category_id = %s, updated = %s where id = %s and deleted = 0'
                num = db.update(sql, title, content, int(post_public), int(visible), int(category_id), now, int(post_id))
            else:
                sql = 'insert into tb_post (title, content, user_id, category_id, public, visible, created) values (%s, %s, %s, %s, %s, %s, %s)'
                num = db.insert(sql, title, content, long(user_id), int(category_id), int(post_public), int(visible), now)
            if num:
                self.write({'success': True})
                self.finish()
                return
            self.write({'success': False, 'error_code': constants.error_code['internal_error']})
            self.finish()
            return
        self.write({'success': False, 'error_code': constants.error_code['missing_parameters']})
        self.finish()

"""
mark post as deleted
"""
class DeleteHandler(baseHandler.RequestHandler):
    def delete(self, post_id):
        if Post.pretend_delete(post_id):
            self.write({'success': True})
            self.finish()
            return
        self.write({'success': False, 'error_code': constants.error_code['internal_error']})
        self.finish()

