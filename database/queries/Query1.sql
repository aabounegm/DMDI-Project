SELECT DISTINCT
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
			Patients.id = 1 AND Patients.id = Appointments.patient_id
			AND Appointments.date < NOW()
		ORDER BY
			date
			DESC LIMIT 1
	) AS Patient_last_visit
WHERE
(
	(first_name LIKE 'M%' AND last_name NOT LIKE 'M%')
	OR
	(first_name LIKE 'L%' AND last_name NOT LIKE 'L%')
	OR
	(first_name NOT LIKE 'M%' AND last_name LIKE 'M%')
	OR
	(first_name NOT LIKE 'L%' AND last_name LIKE 'L%')
)
AND
	Appointments.doctor_id = Doctors.id
AND
	Appointments.patient_id = Patient_last_visit.patient_id
AND
	Appointments.date::DATE = Patient_last_visit.appointment_date::DATE