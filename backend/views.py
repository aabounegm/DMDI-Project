from flask import Blueprint, jsonify
import psycopg2
import psycopg2.extras

api = Blueprint('api', __name__, url_prefix='/api')
conn = psycopg2.connect(host='localhost', user='postgres',
                        password='password', database='hospital')


@api.route('/doctors')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM doctors')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)
