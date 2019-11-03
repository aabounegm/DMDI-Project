from flask import Blueprint, jsonify
import psycopg2

api = Blueprint('api', __name__, url_prefix='/api')
conn = psycopg2.connect(host='localhost', user='postgres',
                        password='password', database='hospital')


@api.route('/doctors')
def api_home():
    cur = conn.cursor()
    cur.execute('SELECT name FROM doctors')
    results = []
    colnames = [desc[0] for desc in cur.description]
    for row in cur.fetchall():
        results.append(dict(zip(colnames, row)))
    cur.close()
    return jsonify(results)
