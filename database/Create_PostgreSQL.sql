-- PostgreSQL 12.0

CREATE TABLE Doctors
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  license_id INT NOT NULL UNIQUE,
  speciality VARCHAR(40) NOT NULL,
  cost INT NOT NULL CONSTRAINT nonnegative CHECK(cost >= 0),
  room CHAR(4) NOT NULL,
  phone_number CHAR(12) CHECK(phone_number ~ E'^\\+\\d+$')
);

CREATE TABLE Doctor_Working_Hours
(
  id SERIAL PRIMARY KEY,
  doctor_id INT NOT NULL REFERENCES Doctors,
  start_time TIME,
  end_time TIME,
  day SMALLINT CONSTRAINT in_week CHECK( day >=0 AND day <=6 )
);
CREATE INDEX doctor_index ON Doctor_Working_Hours(doctor_id);

CREATE TABLE Nurses
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  license_id INT NOT NULL UNIQUE,
  phone_number CHAR(12) CHECK(phone_number ~ E'^\\+\\d+$'),
  salary INT NOT NULL CONSTRAINT nonnegative CHECK(salary >= 0)
);

CREATE TABLE Nurse_Working_Hours
(
  id SERIAL PRIMARY KEY,
  nurse_id INT NOT NULL REFERENCES Nurses(id),
  start_time TIME,
  end_time TIME,
  day SMALLINT CONSTRAINT in_week CHECK( day >=0 AND day <=6 )
);

CREATE TABLE Staff
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  job VARCHAR(40) NOT NULL,
  phone_number CHAR(12) CHECK(phone_number ~ E'^\\+\\d+$'),
  salary INT NOT NULL CONSTRAINT nonnegative CHECK(salary >= 0)
);

CREATE TABLE Staff_Working_Hours
(
  id SERIAL PRIMARY KEY,
  staff_id INT NOT NULL REFERENCES staff(id),
  start_time TIME,
  end_time TIME,
  day SMALLINT CONSTRAINT in_week CHECK( day >=0 AND day <=6 )
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
  blood_type CHAR(3) NOT NULL CHECK(blood_type ~ E'^(A|B|AB|O)(\\+|-)'),
  phone_number CHAR(12) CHECK(phone_number ~ E'^\\+\\d+$'),
  syndicate_id INT REFERENCES Syndicates(id),
  emergency_contact_name VARCHAR(40),
  emergency_contact_relation VARCHAR(25),
  emergency_contact_phone_number CHAR(12) CHECK(emergency_contact_phone_number ~ E'^\\+\\d+$')
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
  appointment_id INT PRIMARY KEY REFERENCES Appointments(id),
  date TIMESTAMP NOT NULL DEFAULT NOW(),
  diagnosis TEXT NOT NULL,
  additional_notes TEXT,
  needs_follow_up BOOLEAN NOT NULL DEFAULT false
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
  CONSTRAINT only_one_creator CHECK( (doctor_id IS NULL) != (nurse_id IS NULL))
);

CREATE TABLE Nurse_Subscription
(
  nurse_id INT NOT NULL REFERENCES Nurses(id),
  board_id INT NOT NULL REFERENCES Notice_boards(id),
  PRIMARY KEY (nurse_id, board_id)
);

CREATE TABLE Doctor_Subscription
(
  doctor_id INT NOT NULL REFERENCES Doctors(id),
  board_id INT NOT NULL REFERENCES Notice_boards(id),
  PRIMARY KEY (doctor_id, board_id)
);

CREATE TABLE Patient_Subscription
(
  patient_id INT NOT NULL REFERENCES Patients(id),
  board_id INT NOT NULL REFERENCES Notice_boards(id),
  PRIMARY KEY (patient_id, board_id)
);

CREATE TABLE Discounts
(
  syndicate_id INT NOT NULL REFERENCES Syndicates(id),
  doctor_id INT NOT NULL REFERENCES Doctors(id),
  discount_amount INT NOT NULL CONSTRAINT nonnegative CHECK (discount_amount >= 0) DEFAULT 0,
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
  report_id INT PRIMARY KEY REFERENCES reports(appointment_id),
  amount INT NOT NULL CONSTRAINT nonnegative CHECK(amount >= 0),
  date TIMESTAMP NOT NULL DEFAULT NOW(),
  paid BOOLEAN NOT NULL DEFAULT false,
  inventory_change_id INT REFERENCES Inventory_Changes(id)
);

CREATE TABLE Prescriptions
(
  medicine_id INT NOT NULL REFERENCES Medicines(id),
  report_id INT NOT NULL REFERENCES Reports(appointment_id),
  PRIMARY KEY (medicine_id, report_id)
);
