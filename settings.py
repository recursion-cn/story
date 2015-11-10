## application settings
##
## @author victor li
## @date 2015/09/26

import os.path

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'assets')

settings = {
    'autoreload': True,
    'debug': True,
    'compress_response': True,
    'template_path': TEMPLATE_PATH,
    'static_path': STATIC_PATH,
    'static_url_prefix': '/assets/',
    'login_url': r'/users/login',
    'cookie_secret': '7BDF5B8CB6C45F17EC11F0DBED858A67',
    'white_tags_list': [u'p', u'h1', u'h2', u'h3', u'h4', u'h5', u'h6', u'a', u'img', u'strong', u'code', u'br', u'ul', u'li', u'hr', u'ol', u'dl', u'dd'],
    'white_attrs_list': {
                            '*': ['class'],
                            'a': ['href', 'rel'],
                            'img': ['src', 'alt'],
                        }
}

database = {
    'host': '127.0.0.1',
    'database': 'recursion',
    'user': 'root',
    'password': 'test'
}
