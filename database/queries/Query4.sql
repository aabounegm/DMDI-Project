SELECT SUM
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
) AS Slots_2;
