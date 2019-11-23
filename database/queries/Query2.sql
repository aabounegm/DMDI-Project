SELECT
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
) AS Slots
GROUP BY
	Slots.doctor_id,
	Slots.doctor_first_name,
	Slots.doctor_last_name,
	Slots.weekday,
	Slots.hours
ORDER BY
	total_num DESC;
