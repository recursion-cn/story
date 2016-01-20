## application settings
##
## @author victor li
## @date 2015/09/26

import os.path

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'assets')

settings = dict(
    autoreload = True,
    debug = True,
    compress_response = True,
    template_path = TEMPLATE_PATH,
    static_path = STATIC_PATH,
    static_url_prefix = '/assets/',
    login_url = r'/users/login',
    cookie_secret = '7BDF5B8CB6C45F17EC11F0DBED858A67',
)

qiniu_setting = dict(
    qiniu_ak = 'EFkcGh5tQUQYl53T41EB6NhmMDlaTFWwLmoztGwd',
    qiniu_sk = 'rPMggSq3Cj5ZZLA7ip1BdFyrOD-nAlt7acRuDGZM',
    images_bucket = 'photos',
    avatar_bucket = 'avatar'
)

database = dict(
    host = '127.0.0.1',
    database = 'recursion',
    user = 'root',
    password = 'test',
)
