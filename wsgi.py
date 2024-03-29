#!python
"""
wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from tweet_reader.web import create_app

application = DispatcherMiddleware(create_app())

if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
