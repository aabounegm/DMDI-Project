SELECT
	Doctors.id AS doctor_id,
	Doctors.first_name AS doctor_first_name,
	Doctors.last_name AS doctor_last_name
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
	Doctors.id = Patient_hundred_checked.doctor_id;