from flask import Blueprint, jsonify, request, abort
import psycopg2
import psycopg2.extras
import os

api = Blueprint('api', __name__, url_prefix='/api')
conn = psycopg2.connect(os.getenv('DATABASE_URL'))


@api.route('/doctors', endpoint='doctors')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM doctors')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/doctors/query1', endpoint='query1')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT * from Doctors
        WHERE (first_name LIKE 'M%%' AND last_name NOT LIKE 'M%%')
           OR (first_name LIKE 'L%%' AND last_name NOT LIKE 'L%%')
           OR (first_name NOT LIKE 'M%%' AND last_name LIKE 'M%%')
           OR (first_name NOT LIKE 'L%%' AND last_name LIKE 'L%%')'''
                )
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/patients', endpoint='patients')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT patient.*, syndicate.name as syndicate_name 
        FROM patients patient
        FULL OUTER JOIN syndicates syndicate ON patient.syndicate_id=syndicate.id
        WHERE patient.id IS NOT NULL''')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/reports', endpoint='reports')
def api_home():
    patient_id = request.args.get('patient_id', type=int)
    doctor_id = request.args.get('doctor_id', type=int)
    user_type = 'patient' if patient_id is not None else 'doctor' if doctor_id is not None else None
    if user_type is None:
        abort(400, 'Please pass a patient/doctor id')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(f'''
        SELECT
            CONCAT(patient.first_name, ' ', patient.last_name) as patient_name,
            CONCAT(doctor.first_name, ' ', doctor.last_name) as doctor_name,
            report.diagnosis, report.additional_notes, report.needs_follow_up, report.date
        FROM Reports report, Patients patient, Doctors doctor
        WHERE report.{user_type}_id = %s AND report.patient_id=patient.id AND doctor.id=report.doctor_id; ''',
                (patient_id if user_type == 'patient' else doctor_id,))
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/nurses', endpoint='nurses')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM nurses')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)
