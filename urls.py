import handlers.baseHandler as base
import handlers.mainHandler as main
import handlers.postHandler as post

urls = [
    (r'/', main.MainHandler),
    (r'/records', post.ListHandler),
    (r'/records/edit', post.EditHandler),
    (r'/records/create', post.NewHandler),
    (r'.*', base.RequestHandler),
]
