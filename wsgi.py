from werkzeug import run_simple

from post_service.app import create_app as post_service_create_app
from server.app import create_app as server_create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

server = server_create_app()
post_service = post_service_create_app()
application = DispatcherMiddleware(server, {
    '/post_service': post_service
})

if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=7082,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True)
