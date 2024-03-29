from flask import Blueprint, jsonify, request, abort
import psycopg2
import psycopg2.extras
import os

api = Blueprint('api', __name__, url_prefix='/api')
conn = psycopg2.connect(os.getenv('DATABASE_URL'))


@api.route('/doctors/', endpoint='doctors')
def get_doctors():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM doctors')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/doctors/working_hours', endpoint='doctors_working_hours')
def get_doctors_hours():
    doctor_id = request.args.get('doctor_id', type=int)
    if doctor_id is None:
        abort(400, 'Please select a valid doctor')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        'SELECT * FROM doctor_working_hours WHERE doctor_id = %s', (doctor_id,))
    results = cur.fetchall()
    cur.close()
    for row in results:
        row['start_time'] = str(row['start_time'])
        row['end_time'] = str(row['end_time'])
    return jsonify(results)


@api.route('/doctors/query1', endpoint='query1')
def query1():
    patient_id = request.args.get('patient_id', type=int)
    if patient_id is None:
        abort(400, 'Please select a valid patient')
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT DISTINCT
                        Doctors.*
                    FROM
                        Doctors, Appointments,
                        (
                            SELECT DISTINCT
                                Patients.id AS patient_id,
                                Appointments.date AS appointment_date
                            FROM
                                Appointments,
                                Patients
                            WHERE
                                Patients.id = %s AND Patients.id = Appointments.patient_id
                                AND Appointments.date < NOW()
                                AND Patients.gender = 'f'
                            ORDER BY
                                date
                                DESC LIMIT 1
                        ) AS Patient_last_visit
                    WHERE
                    (
                        (first_name LIKE 'M%%' OR first_name LIKE 'L%%') != (last_name LIKE 'M%%' OR last_name LIKE 'L%%')
                    )
                    AND
                        Appointments.doctor_id = Doctors.id
                    AND
                        Appointments.patient_id = Patient_last_visit.patient_id
                    AND
                        Appointments.date::DATE = Patient_last_visit.appointment_date::DATE''',
                (patient_id,)
                )
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/doctors/query2', endpoint='query2')
def query2():
    doctor_id = request.args.get('doctor_id', type=int)
    one_doctor = ''
    if doctor_id is not None:
        one_doctor = f'AND Doctors.id = {doctor_id}'
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(f'''SELECT
                    Slots.doctor_id,
                    Slots.doctor_first_name,
                    Slots.doctor_last_name,
                    Slots.weekday,
                    Slots.hours,
                    COUNT(*) AS total_num,
                    COUNT(*) / 52.0 AS average_num
                FROM
                (
                    SELECT
                        Doctors.id AS doctor_id,
                        Doctors.first_name AS doctor_first_name,
                        Doctors.last_name AS doctor_last_name,
                        EXTRACT(DOW FROM Appointments.date) AS weekday,
                        EXTRACT(HOUR FROM Appointments.date) AS hours
                    FROM
                        Doctors, Appointments
                    WHERE
                        Appointments.doctor_id = Doctors.id AND
                        (Appointments.DATE >= NOW() - INTERVAL'1 YEAR')
                        AND (Appointments.DATE <= NOW())
                        {one_doctor}
                ) AS Slots
                GROUP BY
                    Slots.doctor_id,
                    Slots.doctor_first_name,
                    Slots.doctor_last_name,
                    Slots.weekday,
                    Slots.hours
                ORDER BY
                    total_num DESC;''',
                )
    results = cur.fetchall()
    cur.close()
    for item in results:
        item['average_num'] = float(item['average_num'])
    return jsonify(results)


@api.route('/query4', endpoint='query4')
def query4():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT SUM
                    (
                    CASE
                        WHEN (Slots_2.patient_age >= 50) THEN
                            CASE
                                WHEN (Slots_2.appointments >=3) THEN
                                    500*Slots_2.appointments
                                ELSE
                                    400*Slots_2.appointments
                            END
                        ELSE
                            CASE
                                WHEN (Slots_2.appointments >=3) THEN 250*Slots_2.appointments
                                ELSE 200*Slots_2.appointments
                            END
                    END
                    )
                    FROM
                    (
                    SELECT
                        Slots.patient_id,
                        Slots.patient_age,
                        COUNT(*) as appointments
                    FROM
                    (
                        SELECT
                            Patients.id AS patient_id,
                            (EXTRACT (YEARS FROM NOW())) -
                            (EXTRACT( YEARS FROM Patients.date_of_birth))
                                as patient_age
                        FROM
                            Patients, Appointments
                            WHERE
                                Appointments.patient_id = Patients.id AND
                                (Appointments.DATE >= NOW() - INTERVAL'1 Month') AND
                                (Appointments.DATE <= NOW())
                    ) AS Slots
                    GROUP BY
                        Slots.patient_id,
                        Slots.patient_age
                    ) AS Slots_2;'''
                )
    result = cur.fetchone()
    result['sum'] = float(result['sum'] or 0)
    cur.close()
    return jsonify(result)


@api.route('/doctors/query5', endpoint='query5')
def query5():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT
                        Doctors.*
                    FROM
                        Doctors,
                        (
                            SELECT
                                Patient_hundred.doctor_id
                            FROM
                            (
                                SELECT
                                    Patient_stability_hundred.doctor_id,
                                    COUNT(*) as patients_visited
                                FROM
                                (
                                    SELECT
                                        Doctors.id AS doctor_id,
                                        EXTRACT (YEAR FROM Appointments.date) as years
                                    FROM
                                        Patients, Appointments, Doctors
                                    WHERE
                                        Appointments.doctor_id = Doctors.id AND
                                        Appointments.patient_id = Patients.id AND
                                        (Appointments.DATE >= NOW() - INTERVAL'10 YEARS') AND
                                        (Appointments.DATE <= NOW())
                                ) AS Patient_stability_hundred
                                GROUP BY
                                    Patient_stability_hundred.doctor_id
                            ) AS Patient_hundred
                            WHERE
                                Patient_hundred.patients_visited >= 100
                        ) AS Patient_hundred_checked,
                        (
                            SELECT
                                Patient_stability_2.doctor_id
                            FROM
                            (
                                SELECT
                                    Patient_stability.doctor_id,
                                    COUNT(*) as years_stable
                                FROM
                                (
                                    SELECT
                                        Patient_stability_hundred.doctor_id,
                                        Patient_stability_hundred.years,
                                        COUNT(*) AS patients_visited
                                    FROM
                                    (
                                        SELECT
                                            Doctors.id AS doctor_id,
                                            EXTRACT (YEAR FROM Appointments.date) as years
                                        FROM
                                            Patients, Appointments, Doctors
                                        WHERE
                                            Appointments.doctor_id = Doctors.id AND
                                            Appointments.patient_id = Patients.id AND
                                            (Appointments.DATE >= NOW() - INTERVAL'10 YEARS') AND
                                            (Appointments.DATE <= NOW())
                                    ) AS Patient_stability_hundred
                                    GROUP BY
                                        Patient_stability_hundred.doctor_id,
                                        Patient_stability_hundred.years
                                ) AS Patient_stability
                                WHERE
                                    Patient_stability.patients_visited >= 5
                                GROUP BY
                                    Patient_stability.doctor_id
                            ) AS Patient_stability_2
                            WHERE
                                Patient_stability_2.years_stable >= 10
                        ) AS Patient_stability_checked
                    WHERE
                        Doctors.id = Patient_stability_checked.doctor_id AND
                        Doctors.id = Patient_hundred_checked.doctor_id;'''
                )
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/patients/', endpoint='patients')
def get_patients():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT patient.*, syndicate.name as syndicate_name
        FROM patients patient
        JOIN syndicates syndicate on patient.syndicate_id=syndicate.id
	    ORDER BY patient.id;''')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/patients/query3', endpoint='query3')
def query3():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT
                Patients.*
            FROM
            Patients,
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
                Patients.id = Slots_3.patient_id AND
                Slots_3.week_count >= EXTRACT (WEEK FROM  NOW()) - EXTRACT
            (WEEK FROM  NOW() - INTERVAL'1 MONTH') + 1;
''')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/reports/', endpoint='reports')
def get_reports():
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
            report.diagnosis, report.additional_notes, report.needs_follow_up, appointment.date
        FROM Reports report, Patients patient, Doctors doctor, Appointments appointment
        WHERE appointment.{user_type}_id = %s AND appointment.patient_id=patient.id
            AND doctor.id=appointment.doctor_id AND report.appointment_id=appointment.id
        ORDER BY appointment.date DESC;''',
                (patient_id if user_type == 'patient' else doctor_id,))
    results = cur.fetchall()
    cur.close()
    return jsonify(results)


@api.route('/nurses/', endpoint='nurses')
def get_nurses():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM nurses')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)
