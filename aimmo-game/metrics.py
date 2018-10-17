from werkzeug.wsgi import DispatcherMiddleware
from prometheus_client import make_wsgi_app

def expose_metrics(flask_app):
    app_dispatch = DispatcherMiddleware(flask_app, {'/metrics': make_wsgi_app()})