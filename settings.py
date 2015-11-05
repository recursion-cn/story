## application settings
##
## @author victor li
## @date 2015/09/26

import os.path

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'assets')

settings = {
    'autoreload': True,
    'autoscape': None,
    'debug': True,
    'compress_response': True,
    'template_path': TEMPLATE_PATH,
    'static_path': STATIC_PATH,
    'static_url_prefix': '/assets/',
    'login_url': r'/users/login',
    'cookie_secret': '7BDF5B8CB6C45F17EC11F0DBED858A67'
}

database = {
    'host': '127.0.0.1',
    'database': 'recursion',
    'user': 'root',
    'password': 'test'
}
