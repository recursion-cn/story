#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author victor li nianchaoli@msn.cn
# date 2016/01/05

import tornado.web
import baseHandler
import qiniu
import random
import os
import time
from datetime import datetime
from settings import qiniu_setting

class FileHandler(baseHandler.RequestHandler):
    @tornado.web.authenticated
    def post(self):
        access_key = qiniu_setting['qiniu_ak']
        secret_key = qiniu_setting['qiniu_sk']
        bucket_name = qiniu_setting['images_bucket']
        q = qiniu.Auth(access_key, secret_key)
        file = self.request.files['editormd-image-file']
        file = file[0]
        file_body = file['body']
        mime_type = file['content_type']
        file_name = file['filename']
        uploaded_file_name = str(time.mktime(datetime.now().timetuple())) + '_' + str(random.random())
        fo = open(u'/tmp/' + file_name, 'wb+')
        fo.write(file_body)
        fo.close()
        token = q.upload_token(bucket_name, uploaded_file_name)
        localfile = u'/tmp/{0}'.format(file_name)
        ret, info = qiniu.put_file(token, uploaded_file_name, localfile, mime_type=mime_type)
        if ret and ret['key'] == uploaded_file_name:
            self.write({'success': 1, 'url': 'http://7xl7p4.com1.z0.glb.clouddn.com/' + uploaded_file_name})
        else:
            self.write({'success': 0, 'message': u'图片上传失败'})

