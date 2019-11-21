from flask import Blueprint, jsonify, request, abort
import psycopg2
import psycopg2.extras
import os

api = Blueprint('api', __name__, url_prefix='/api')
conn = psycopg2.connect(os.getenv('DATABASE_URL'))


@api.route('/doctors/', endpoint='doctors')
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


@api.route('/patients/', endpoint='patients')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT patient.*, syndicate.name as syndicate_name
        FROM patients patient
        JOIN syndicates syndicate on patient.syndicate_id=syndicate.id
	    ORDER BY patient.id;''')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/patients/query3', endpoint='query3')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT
                Slots_3.patient_id,
                Slots_3.full_name
            FROM 
            (
                SELECT
                    Slots_2.patient_id,
                    Slots_2.full_name,
                    COUNT(*) as week_count
                FROM
                (
                SELECT
    				Slots.patient_id,
    				Slots.week,
    				Slots.full_name,
    				COUNT(*) as appointments_count
                FROM
                (
                    SELECT
    	  				Patients.id AS patient_id,
                        Extract(WEEK FROM Appointments.date) AS week,
                        Patients.first_name || ' ' || Patients.last_name AS full_name
                    FROM
                        Patients, Appointments
                    WHERE
                        Appointments.patient_id = Patients.id AND 
                        (Appointments.DATE >= NOW() - INTERVAL'1 MONTH') AND
                        (Appointments.DATE <= NOW())
                ) 
                AS Slots
    			GROUP BY
	    			Slots.patient_id,
   	    			Slots.full_name,
                    Slots.week 
            ) 
                AS Slots_2
                WHERE
                    Slots_2.appointments_count >= 2
                GROUP BY
                    Slots_2.patient_id,
                    Slots_2.full_name	
            )
            AS Slots_3
            WHERE
                Slots_3.week_count >= EXTRACT (WEEK FROM  NOW()) - EXTRACT 
            (WEEK FROM  NOW() - INTERVAL'1 MONTH') + 1;
''')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/reports/', endpoint='reports')
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


@api.route('/nurses/', endpoint='nurses')
def api_home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM nurses')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)
