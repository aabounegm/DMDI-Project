from flask import Flask, Blueprint, send_from_directory
from flask_gzip import Gzip
from views import api
import os

app = Flask(__name__)
if 'DYNO' not in os.environ:
    # For local development on different ports
    from flask_cors import CORS
    CORS(app)
Gzip(app)
app.register_blueprint(api, url_prefix='/api')
app.url_map.strict_slashes = False


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def home(path):
    if not (path.startswith('js/') or path.startswith('css/') or path == 'favicon.ico'):
        path = 'index.html'
    return send_from_directory('./dist', path)


if __name__ == '__main__':
    app.run('0.0.0.0', os.getenv('PORT', 5000),
            debug=os.getenv('FLASK_DEBUG') == 1)
