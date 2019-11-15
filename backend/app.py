from flask import Flask, Blueprint, send_from_directory
from flask_cors import CORS
from views import api
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix='/api')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def home(path):
    if not (path.startswith('/js/') or path.startswith('/css/') or path == '/favicon.ico'):
        path = 'index.html'
    return send_from_directory('../frontend/dist', path)


if __name__ == '__main__':
    app.run('0.0.0.0', os.getenv('PORT', 5000), debug=True)
