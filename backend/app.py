from flask import Flask, Blueprint, url_for
from flask_cors import CORS
from views import api

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    return 'Main page'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
