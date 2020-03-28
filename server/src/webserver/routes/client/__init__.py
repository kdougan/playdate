"""Initialize client routes."""

import json
import resource
import time

from flask import Response
from flask import g
from flask import render_template
from flask import request
from flask import send_from_directory


from src.webserver.extensions import redis_store


def register(app):
    @app.before_request
    def before_request():
        """Prepare some things before the application handles a request."""
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
        g.pjax = 'X-PJAX' in request.headers

    @app.route('/', defaults={'path': ''})
    @app.route('/<path>')
    @app.route('/<path:path>')
    def index(path):
        """Index/catchall."""
        return render_template('index.html')

    @app.route('/assets/<path:path>')
    def serve_assets(path):
        """Serve Assets."""
        return send_from_directory('static/assets/', path)

    @app.route('/__health', methods=['GET'])
    def health():
        """Health check."""
        return 'OK'

    # @app.route('/__stats/instance', methods=['GET'])
    # def instance_stats():
    #     """Instance Stats (per Orchard spec)."""
    #     ru_self = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    #     ru_children = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    #     pagesize = resource.getpagesize()
    #     mem_usage = (ru_self + ru_children) * pagesize / 1024.0
    #     return json.dumps({
    #         'MetricsKV': {
    #             'mem_kbs': mem_usage
    #         },
    #         'MetricsVersion': 1
    #     })

    @app.route('/__stats/redis', methods=['GET'])
    def redis_stats():
        """REDIS Stats."""
        redis_info = redis_store.info()
        response = json.dumps(redis_info, default=str)
        return Response(response, mimetype='text/xml')

    @app.route('/__stats/config', methods=['GET'])
    def config_stats():
        """Config Stats."""
        response = json.dumps(app.config, default=str)
        return Response(response, mimetype='text/xml')
