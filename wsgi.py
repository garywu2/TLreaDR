from werkzeug import run_simple

from post_service.app import create_app as post_service_create_app
from user_service.app import create_app as user_service_create_app
from comment_service.app import create_app as comment_service_create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

user_service = user_service_create_app()
post_service = post_service_create_app()
comment_service = comment_service_create_app()
application = DispatcherMiddleware(user_service, {
    '/post_service': post_service,
    '/comment_service': comment_service
})

if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=7082,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
        passthrough_errors=True,
        threaded=True)
