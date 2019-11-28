-- MySQL 8.0

CREATE TABLE Doctors
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  license_id INT NOT NULL,
  speciality VARCHAR(40) NOT NULL,
  cost INT CHECK (cost >= 0),
  room CHAR(4) NOT NULL,
  phone_number CHAR(12) CHECK(REGEXP_LIKE(phone_number, '^\\+\\d+$'))
);

CREATE TABLE Doctor_Working_Hours
(
  id SERIAL PRIMARY KEY,
  doctor_id INT REFERENCES Doctors,
  start_time TIME,
  end_time TIME,
  day SMALLINT CHECK( day >=0 AND day <=6 )
);

CREATE TABLE Nurses
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  license_id INT NOT NULL,
  phone_number CHAR(12) CHECK(REGEXP_LIKE(phone_number, '^\\+\\d+$')),
  salary INT NOT NULL CHECK(salary >= 0)
);

CREATE TABLE Nurse_Working_Hours
(
  id SERIAL PRIMARY KEY,
  nurse_id INT REFERENCES Nurses(id),
  start_time TIME,
  end_time TIME,
  day SMALLINT CHECK( day >=0 AND day <=6 )
);

CREATE TABLE Staff
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  job VARCHAR(40) NOT NULL,
  phone_number CHAR(12) CHECK(REGEXP_LIKE(phone_number, '^\\+\\d+$')),
  salary INT NOT NULL CHECK(salary >= 0)
);

CREATE TABLE Staff_Working_Hours
(
  id SERIAL PRIMARY KEY,
  staff_id INT REFERENCES staff(id),
  start_time TIME,
  end_time TIME,
  day SMALLINT CHECK( day >=0 AND day <=6 )
);

CREATE TABLE Syndicates
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(25) NOT NULL
);

CREATE TABLE Patients
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  date_of_birth DATE NOT NULL,
  gender CHAR(1) CHECK (gender = 'm' OR gender = 'f'),
  blood_type CHAR(3) NOT NULL CHECK(REGEXP_LIKE(blood_type, '^(A|B|AB|O)(\\+|-)')),
  phone_number CHAR(12) CHECK(REGEXP_LIKE(phone_number, '^\\+\\d+$')),
  syndicate_id INT REFERENCES Syndicates(id),
  emergency_contact_name VARCHAR(40),
  emergency_contact_relation VARCHAR(25),
  emergency_contact_phone_number CHAR(12) CHECK(REGEXP_LIKE(emergency_contact_phone_number, '^\\+\\d+$'))
);

CREATE TABLE Appointments
(
  id SERIAL PRIMARY KEY,
  date TIMESTAMP NOT NULL,
  doctor_id INT NOT NULL REFERENCES Doctors(id),
  patient_id INT NOT NULL REFERENCES Patients(id),
  ailment_description TEXT
);

CREATE TABLE Reports
(
  id SERIAL PRIMARY KEY,
  diagnosis TEXT NOT NULL,
  additional_notes TEXT,
  needs_follow_up BOOLEAN NOT NULL DEFAULT false,
  date TIMESTAMP NOT NULL DEFAULT NOW(),
  appointment_id INT NOT NULL REFERENCES Appointments(id)
);

CREATE TABLE Notice_Boards
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(25) NOT NULL,
  description TEXT NOT NULL,
  creator_id INT NOT NULL REFERENCES Doctors(id)
);

CREATE TABLE Notices
(
  id SERIAL PRIMARY KEY,
  board_id INT NOT NULL REFERENCES Notice_Boards(id),
  title VARCHAR(25) NOT NULL,
  content TEXT NOT NULL,
  date_posted TIMESTAMP NOT NULL DEFAULT NOW(),
  doctor_id INT REFERENCES Doctors(id),
  nurse_id INT REFERENCES Nurses(id),
  CONSTRAINT only_one_creator CHECK( doctor_id IS NULL AND nurse_id IS NOT NULL OR doctor_id IS NOT NULL AND nurse_id IS NULL )
);

CREATE TABLE Nurse_Subscription
(
  nurse_id INT NOT NULL REFERENCES Nurses(id),
  board_id INT NOT NULL REFERENCES Notice_boards(id),
  PRIMARY KEY (board_id, nurse_id)
);

CREATE TABLE Doctor_Subscription
(
  doctor_id INT NOT NULL REFERENCES Doctors(id),
  board_id INT NOT NULL REFERENCES Notice_boards(id),
  PRIMARY KEY (board_id, doctor_id)
);

CREATE TABLE Patient_Subscription
(
  patient_id INT NOT NULL REFERENCES Patients(id),
  board_id INT NOT NULL REFERENCES Notice_boards(id),
  PRIMARY KEY (board_id, patient_id)
);

CREATE TABLE Discounts
(
  syndicate_id INT NOT NULL REFERENCES Syndicates(id),
  doctor_id INT NOT NULL REFERENCES Doctors(id),
  discount_amount INT NOT NULL DEFAULT 0 CHECK (discount_amount >= 0),
  PRIMARY KEY (syndicate_id, doctor_id)
);

CREATE TABLE Medicines
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(25) NOT NULL,
  active_ingredients VARCHAR(256)
);

CREATE TABLE Inventory_Changes
(
  id SERIAL PRIMARY KEY,
  medicine_id INT NOT NULL REFERENCES Medicines(id),
  amount INT NOT NULL,
  description TEXT,
  nurse_id INT REFERENCES Nurses(id)
);

CREATE TABLE Invoices
(
  report_id INT PRIMARY KEY REFERENCES reports(id),
  amount INT NOT NULL,
  date TIMESTAMP NOT NULL DEFAULT NOW(),
  paid BOOLEAN NOT NULL DEFAULT false,
  inventory_change_id INT REFERENCES Inventory_Changes(id)
);

CREATE TABLE Prescriptions
(
  medicine_id INT NOT NULL REFERENCES Medicines(id),
  report_id INT NOT NULL REFERENCES Reports(id),
  PRIMARY KEY (medicine_id, report_id)
);
