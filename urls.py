import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.postHandler as post

urls = [
    (r'/', main.MainHandler),
    (r'/posts', post.ListHandler),
    (r'/posts/(\d+)', post.PostHandler),
    (r'/posts/edit', post.EditHandler),
    (r'/posts/create', post.NewHandler),
    (r'.*', base.RequestHandler),
]
