SELECT
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
