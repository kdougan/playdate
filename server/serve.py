"""Main entry point for serving the app."""
import os
import sys

from src.webserver import config
from src.webserver import create_app

app = create_app(config.DevConfig)


def main():
    if len(sys.argv) > 1:
        app.extensions['hurricane'].set_local_development(sys.argv[1])
        # app.extensions['hurricane'].verbose = True
    os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
    app.run(debug=True,
            host='0.0.0.0',
            port=5000,
            threaded=True)


if __name__ == '__main__':
    main()
