"""Initialize client routes."""

import json
import resource
import time

from flask import Response
from flask import g
from flask import render_template
from flask import request
from flask import send_from_directory
from flask_graphql import GraphQLView

from ...graphql import schema
from ...extensions import cache
from ...database import db
from ..store import asset_store_route


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

    @app.route('/static/<path:path>')
    def serve_assets(path):
        """Serve Assets."""
        return send_from_directory('static/assets/', path)

    @app.route('/assets/<path:path>', methods=['GET'])
    @cache.memoize(50)
    def serve_store_content(path):
        return asset_store_route(path)

    @app.route('/__health', methods=['GET'])
    def health():
        """Health check."""
        return 'OK'

    @app.route('/__stats/config', methods=['GET'])
    def config_stats():
        """Config Stats."""
        response = json.dumps(app.config, default=str)
        return Response(response, mimetype='text/xml')

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,
            get_context=lambda: {'session': db.session}
        )
    )
