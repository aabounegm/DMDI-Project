"""
DMD Project Phase 3 Script Population.

BS18-04: Abdelrahman Abounegm, Georgiy Stepanov, Vitaliy Korbashov,
    Pavel Tishkin, Yulia Chukanova.
"""

# Interactive Python script for an automatic and pseudo-random population of the database.
# It provides sample data for each table (Task 4.a).
# The result of this program is an "Output.sql" file,
# created in the same directory (from where the program was launched),
# containing textual sequence of INSERT instructions to fill in the tables in the database with sample data.

# Following files are required in the same directory with the program for a proper work:
# "FirstNames.txt", "LastNames.txt", "DoctorSpecialities.txt", "Jobs.txt", "Syndicates.txt",
# "ECRelations.txt", "Diagnoses.txt", "AdditionalNotes.txt".

from random import randint, choice  # to generate pseudo-random numerical data
from datetime import datetime  # to generate datetime in isoformat

loremIpsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit aliqua.'


def generateBool():
    """Generate either `true` or `false`."""
    return randint(0, 1) == 1


LicenseIDs = set()


def generateLicenseID():
    """Generate unique license_id."""
    t = randint(100102, 997997)
    while t in LicenseIDs:
        t = randint(100102, 997997)
    LicenseIDs.add(t)
    return t


phnumbers = set()


def generatePhnumber():
    """Generate unique phone_number in string surrounded by single quotes (format: '+79...')."""
    t = randint(100300201, 999799797)
    while t in phnumbers:
        t = randint(100300201, 999799797)
    phnumbers.add(t)
    return f"'+79{t}'"


def generateRoom():
    """Generate (non-unique) room in string surrounded by single quotes."""
    room = randint(1, 5) * 100 + randint(1, 78)
    t = randint(1, 10)
    letter = ''
    # note that either 'A', 'B', 'C' or nothing can be added in the end of the three-digit number:
    if t <= 2:
        letter = 'A'
    elif t == 3:
        letter = 'B'
    elif t == 4:
        letter = 'C'
    return f"'{room:d}{letter}'"


bloodTypes = ('A', 'B', 'AB', 'O')


def generateBlood():
    """Generate 1 of 6 possible blood types, surrounded by single quotes."""
    blood_type = choice(bloodTypes)
    Rh = '+' if randint(0, 1) else '-'
    return f"'{blood_type}{Rh}'"


def generateECName():
    """Generate Patients' emergency_contact_name (which is 'Name Surname')."""
    return choice(firstnames)[0:-1] + ' ' + choice(lastnames)[1:]


def generateNumSyndicate():
    """Generate the number of Syndicate to which the Person belongs to."""
    if randint(0, 3):
        return str(randint(1, numSyndicates))
    return 'null'


def generateICAmount():
    """Generate Inventory_Change amount."""
    t = randint(-10, 10)
    while t == 0:
        t = randint(-10, 10)
    return t


def generateDOB():
    """Generate Patient's date_of_birth in format 'yyyy.mm.dd' in string surrounded by single quotes."""
    month = randint(1, 12)
    if month == 2:
        day = randint(1, 28)
    else:
        day = randint(1, 30)
    return f"'{randint(1950, 2015)}.{month:02d}.{day:02d}'"


def generateMinute():
    """Generate a string from "00" to "55" divisible by 5."""
    t = randint(0, 11) * 5
    return f"{t:02d}"


def generateDateTime():
    """Generate date and time for Appointment in isoformat using datetime.isoformat()."""
    return datetime(
        randint(2010, 2019), randint(1, 12), randint(1, 28), randint(7, 19),
        int(generateMinute())).isoformat()


def generateTime1():
    """Generate the time from which a person starts working in the morning (from '07:00' to '10:55'), in string surrounded by single quotes."""
    hour = randint(7, 10)
    return f"'{hour:02d}:{generateMinute()}'"


def generateTime2():
    """Generate the time from which a person has lunch-break (from '12:00' to '13:55'), in string surrounded by single quotes."""
    return f"'{randint(12, 13)}:{generateMinute()}'"


def generateTime3():
    """Generate the time from which a person starts working in the evening (till which has lunch-break), that is from '15:00' to '16:55', in string surrounded by single quotes."""
    return f"'{randint(15, 16)}:{generateMinute()}'"


def generateTime4():
    """Generate the time till which a person works in the evening (the end of a workday), that is from '18:00' to '22:55', in string surrounded by single quotes."""
    return f"'{randint(18, 22)}:{generateMinute()}'"


print('DMD Project Phase 3 Script Population by Abdelrahman Abounegm, Georgiy Stepanov,')
print('Vitaliy Korbashov, Pavel Tishkin, Yulia Chukanova - BS18-04.')
print('This program generates a sequence of INSERT queries')
print('to fill in the tables in the database with pseudo-random sample data.\n')
fout = open('Output.sql', 'w')  # create an Output file with INSERT queries
with open('data/FirstNames.txt', 'r') as fnames:  # import list of First Names:
    firstnames = [f"'{row.strip()}'" for row in fnames]
# import list of Last Names:
with open('data/LastNames.txt', 'r') as flastnames:
    lastnames = [f"'{row.strip()}'" for row in flastnames]
# import list of Doctors' specialities:
with open('data/DoctorSpecialities.txt', 'r') as fspecialists:
    specialists = [f"'{row.strip()}'" for row in fspecialists]
with open('data/Jobs.txt', 'r') as fjobs:  # import list of Jobs:
    jobs = [f"'{row.strip()}'" for row in fjobs]
# import list of emergency_contact_relation:
with open('data/ECRelations.txt', 'r') as frelations:
    relations = [f"'{row.strip()}'" for row in frelations]
# import list of Diagnoses:
with open('data/Diagnoses.txt', 'r') as fdiagnoses:
    diagnoses = [f"'{row.strip()}'" for row in fdiagnoses]
# import list of Additional_Notes:
with open('data/AdditionalNotes.txt', 'r') as faddnotes:
    AdditionalNotes = [f"'{row.strip()}'" for row in faddnotes]

print('Enter number of Doctors you want in the database')
print("(to use the default value of 400 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numDoctors = int(input())
except Exception:
    print('Using the default value of 400...')
    numDoctors = 400
if numDoctors < 0:
    print('Using the default value of 400...')
    numDoctors = 400
for i in range(numDoctors):  # generate INSERT statements for Doctors:
    fout.write(
        f"INSERT INTO Doctors (first_name, last_name, license_id, speciality, cost, room, phone_number) VALUES ("
        f"{choice(firstnames)}, {choice(lastnames)}, {generateLicenseID()}, {choice(specialists)}, "
        f"{randint(1, 70) * 100}, {generateRoom()}, {generatePhnumber()});\n")
fout.write('\n')
# generate Working hours for each Doctor...
for doc in range(1, numDoctors + 1):
    for day in range(1, 7):  # ...on each day:
        if randint(0, 1):
            # Working hours before lunch-break:
            fout.write(
                f"INSERT INTO Doctor_Working_Hours (doctor_id, start_time, end_time, day) VALUES ("
                f"{doc}, {generateTime1()}, {generateTime2()}, {day});\n")
            # Working hours after lunch-break
            fout.write(
                f"INSERT INTO Doctor_Working_Hours (doctor_id, start_time, end_time, day) VALUES ("
                f"{doc}, {generateTime3()}, {generateTime4()}, {day});\n")

fout.write('\n')
print(numDoctors, 'Doctors and their timetable have been successfully created.\n')

print('Enter number of Nurses you want in the database')
print("(to use the default value of 1000 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numNurses = int(input())
except Exception:
    print('Using the default value of 1000...')
    numNurses = 1000
if numNurses < 0:
    print('Using the default value of 1000...')
    numNurses = 1000
for i in range(numNurses):  # generate INSERT statements for Nurses:
    fout.write(
        f'INSERT INTO Nurses (first_name, last_name, license_id, phone_number, salary) VALUES ('
        f"{choice(firstnames)}, {choice(lastnames)}, {generateLicenseID()}, "
        f"{generatePhnumber()}, {randint(100, 500) * 100});\n")
fout.write('\n')
# generate Working hours for each Nurse...

for nurse in range(1, numNurses + 1):
    for day in range(1, 6):  # ...on each day:
        if randint(0, 1):
            query = (f"INSERT INTO Nurse_Working_Hours (nurse_id, start_time, end_time, day) VALUES ("
                     f"{nurse}, {{}}, {{}}, {day});\n")

            # Working hours before lunch-break:
            fout.write(query.format(generateTime1(), generateTime2()))
            # Working hours after lunch-break
            fout.write(query.format(generateTime3(), generateTime4()))

fout.write('\n')
print(numNurses, 'Nurses and their timetable have been successfully created.\n')

print('Enter number of Staff you want in the database')
print("(to use the default value of 500 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numStaff = int(input())
except Exception:
    print('Using the default value of 500...')
    numStaff = 500
if numStaff < 0:
    print('Using the default value of 500...')
    numStaff = 500
for i in range(numStaff):  # generate INSERT statements for Staff:
    fout.write(
        f"INSERT INTO Staff (first_name, last_name, job, phone_number, salary) VALUES ("
        f"{choice(firstnames)}, {choice(lastnames)}, {choice(jobs)}, "
        f"{generatePhnumber()}, {randint(25, 5240) * 100});\n")
fout.write('\n')
# generate Working hours for each Staff...
for staff in range(1, numStaff + 1):
    for day in range(1, 6):  # ...on each day:
        if randint(0, 1):
            # Working hours before lunch-break:
            fout.write(
                f"INSERT INTO Staff_Working_Hours (staff_id, start_time, end_time, day) VALUES ("
                f"{staff}, {generateTime1()}, {generateTime2()}, {day:d});\n")
            # Working hours after lunch-break
            fout.write(
                f"INSERT INTO Staff_Working_Hours (staff_id, start_time, end_time, day) VALUES ("
                f"{staff}, {generateTime3()}, {generateTime4()}, {day:d});\n")
fout.write('\n')
print(numStaff, 'Staff and their timetable have been successfully created.\n')

print('Novelty feature: Enter number of Medical Syndicates you want in the database (max 30)')
print("(to use the default value of 30 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numSyndicates = int(input())
except Exception:
    print('Using the default value of 30...')
    numSyndicates = 30
if numSyndicates < 0 or numSyndicates > 30:
    print('Using the default value of 30...')
    numSyndicates = 30
if numSyndicates != 0:
    # generate atomic INSERT statement for Syndicates:
    with open('data/Syndicates.txt', 'r') as fsyndicates:
        fout.write("INSERT INTO Syndicates (name) VALUES ")
        names = fsyndicates.readlines()[0:numSyndicates]
        fout.write(', '.join(f"('{name.strip()}')" for name in names))
        fout.write(';\n\n')
print(numSyndicates, 'Medical Syndicates have been successfully created.\n')

print('Enter number of Patients you want in the database')
print("(To use the default value of 10000 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numPatients = int(input())
except Exception:
    print('Using the default value of 10000...')
    numPatients = 10000
if numPatients < 0:
    print('Using the default value of 10000...')
    numPatients = 10000
for i in range(numPatients):  # generate INSERT statements for Patients:
    fout.write(
        f"INSERT INTO Patients (first_name, last_name, date_of_birth, gender, blood_type, "
        f"phone_number, syndicate_id, emergency_contact_name, emergency_contact_relation, "
        f"emergency_contact_phone_number) VALUES ({choice(firstnames)}, {choice(lastnames)}, "
        f"{generateDOB()}, '{'m' if randint(0, 1) else 'f'}', {generateBlood()}, {generatePhnumber()}, {generateNumSyndicate()}, "
        f"{generateECName()}, {choice(relations)}, {generatePhnumber()});\n")
fout.write('\n')
print(numPatients, 'Patients with Emergency contacts have been successfully created.\n')

numAppointments = 50000
print('Enter number of Appointments and reports you want in the database')
print(
    f"(to use the default value of {numAppointments} for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numAppointments = int(input())
except Exception:
    print(f'Using the default value of {numAppointments}...')
if numAppointments < 0:
    numAppointments = 50000
    print(f'Using the default value of {numAppointments}...')
for i in range(numAppointments):  # generate INSERT statements for Appointmens:
    fout.write(
        f"INSERT INTO Appointments (date, doctor_id, patient_id, ailment_description) VALUES ("
        f"'{generateDateTime()}', {randint(1, numDoctors)}, {randint(1, numPatients)}, '{loremIpsum}');\n")
fout.write('\n')

# generate INSERT statements for Reports:
for i in range(numAppointments):
    fout.write(f'INSERT INTO Reports (diagnosis, additional_notes, needs_follow_up, appointment_id) '
               f"VALUES ({choice(diagnoses)}, {choice(AdditionalNotes)}, {generateBool()}, {i+1});\n")
fout.write('\n')
print(numAppointments, 'Appointments with Reports have been successfully created.\n')

print('Enter number of Notice Boards you want in the database')
print("(to use the default value of 100 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numNoticeBoards = int(input())
except Exception:
    print('Using the default value of 100...')
    numNoticeBoards = 100
if numNoticeBoards < 0:
    print('Using the default value of 100...')
    numNoticeBoards = 100
# generate INSERT statements for NoticeBoards:
for i in range(numNoticeBoards):
    fout.write(
        f"INSERT INTO Notice_Boards (name, description, creator_id) VALUES ("
        f"'Notice Board #{i + 1}', '{loremIpsum}', {randint(1, numDoctors)});\n")
fout.write('\n')
print(numNoticeBoards, 'Notice Boards have been successfully created.\n')

print('Enter number of Notices you want in the database')
print("(to use the default value of 500 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numNotices = int(input())
except Exception:
    print('Using the default value of 500...')
    numNotices = 500
if numNotices < 0:
    print('Using the default value of 500...')
    numNotices = 500
for i in range(numNotices):  # generate INSERT statements for Notices:
    fout.write(
        f"INSERT INTO Notices (board_id, title, content, date_posted, doctor_id, nurse_id) VALUES ("
        f"{randint(1, numNoticeBoards)}, 'Notice {i + 1}', '{loremIpsum}', '{generateDateTime()}', ")
    if randint(0, 2):
        fout.write(f"null, {randint(1, numNurses)});\n")
    else:
        fout.write(f"{randint(1, numDoctors)}, null);\n")
fout.write('\n')
print(numNotices, 'Notices connected to Notice Boards have been successfully created.\n')

print('Enter number of Entries you want in Doctor_Subscription (the table relates Nurses and Notice Boards)')
print("To use the default value of 150 for the stress-test, just press 'Enter': ", end='')
try:  # check the input:
    numDS = int(input())
except Exception:
    print('Using the default value of 150...')
    numDS = 150
if numDS < 0:
    print('Using the default value of 150...')
    numDS = 150
if numDS > numDoctors * numNoticeBoards:
    numDS = numDoctors * numNoticeBoards
    print('Impossible. Restricting to', numDS)
keys = set()
for i in range(numDS):  # generate INSERT statements for Doctor_Subscription:
    doc_id = randint(1, numDoctors)
    board_id = randint(1, numNoticeBoards)
    while (doc_id, board_id) in keys:
        doc_id = randint(1, numDoctors)
        board_id = randint(1, numNoticeBoards)
    keys.add((doc_id, board_id))
    fout.write(f"INSERT INTO Doctor_Subscription (doctor_id, board_id) VALUES ("
               f"{doc_id}, {board_id});\n")
fout.write('\n')
print(numDS, 'entries in Doctor_Subscription have been successfully created.\n')

print('Enter number of Entries you want in Nurse_Subscription (the table relates Doctors and Notice Boards)')
print("To use the default value of 300 for the stress-test, just press 'Enter': ", end='')
try:  # check the input:
    numNS = int(input())
except Exception:
    print('Using the default value of 300...')
    numNS = 300
if numNS < 0:
    print('Using the default value of 300...')
    numNS = 300
if numNS > numNurses * numNoticeBoards:
    numNS = numNurses * numNoticeBoards
    print('Impossible. Restricting to', numNS)
keys = set()
for i in range(numNS):  # generate INSERT statements for Nurse_Subscription:
    nurse_id = randint(1, numNurses)
    board_id = randint(1, numNoticeBoards)
    while (nurse_id, board_id) in keys:
        nurse_id = randint(1, numNurses)
        board_id = randint(1, numNoticeBoards)
    keys.add((nurse_id, board_id))
    fout.write(f"INSERT INTO Nurse_Subscription (nurse_id, board_id) VALUES ("
               f"{nurse_id}, {board_id});\n")
fout.write('\n')
print(numNS, 'entries in Nurse_Subscription have been successfully created.\n')

print('Enter number of Entries you want in Patient_Subscription (the table relates Patients and Notice Boards)')
print("To use the default value of 444 for the stress-test, just press 'Enter': ", end='')
try:  # check the input:
    numPS = int(input())
except Exception:
    print('Using the default value of 444...')
    numPS = 444
if numPS < 0:
    print('Using the default value of 444...')
    numPS = 444
if numPS > numPatients * numNoticeBoards:
    numPS = numPatients * numNoticeBoards
    print('Impossible. Restricting to', numPS)
keys = set()
for i in range(numPS):  # generate INSERT statements for Patient_Subscription:
    pat_id = randint(1, numPatients)
    board_id = randint(1, numNoticeBoards)
    while (pat_id, board_id) in keys:
        pat_id = randint(1, numPatients)
        board_id = randint(1, numNoticeBoards)
    keys.add((pat_id, board_id))
    fout.write(
        f"INSERT INTO Patient_Subscription (patient_id, board_id) VALUES ("
        f"{pat_id}, {board_id});\n")
fout.write('\n')
print(numPS, 'entries in Patient_Subscription have been successfully created.\n')

print('Novelty feature: Enter number of Discounts you want in the database')
print("(to use the default value of 200 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numDiscounts = int(input())
except Exception:
    print('Using the default value of 200...')
    numDiscounts = 200
if numDiscounts < 0:
    print('Using the default value of 200...')
    numDiscounts = 200
if numDiscounts > numDoctors * numSyndicates:
    print('Number of Discounts cannot be bigger than')
    print('(number of Doctors) * (number of Syndicates) =')
    print(numDoctors, '*', numSyndicates, '=', numDoctors * numSyndicates)
    print('Using the value of', numDoctors * numSyndicates, 'for Discounts...')
    numDiscounts = numDoctors * numSyndicates
keys = set()
for i in range(numDiscounts):  # generate INSERT statements for Discounts:
    SyndicateID = randint(1, numSyndicates)
    DoctorID = randint(1, numDoctors)
    while (SyndicateID, DoctorID) in keys:
        SyndicateID = randint(1, numSyndicates)
        DoctorID = randint(1, numDoctors)
    keys.add((SyndicateID, DoctorID))
    fout.write(f'INSERT INTO Discounts (syndicate_id, doctor_id, discount_amount) VALUES ('
               f"{SyndicateID}, {DoctorID}, {randint(1, 20) * 50});\n")
# notice that amount of discount can be bigger than the actual cost of a Doctor per hour
fout.write('\n')
print(numDiscounts, 'Discounts connecting Doctors and Syndicates have been successfully created.\n')

print('Enter number of Medicines you want in the database')
print("(to use the default value of 25 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numMedicines = int(input())
except Exception:
    print('Using the default value of 25...')
    numMedicines = 25
if(numMedicines < 0):
    print('Using the default value of 25...')
    numMedicines = 25
for i in range(numMedicines):  # generate INSERT statements for Medicines:
    fout.write(f"INSERT INTO Medicines (name, active_ingredients) VALUES ("
               f"'Medicine {i+1}', '{loremIpsum}');\n")
fout.write('\n')
print(numMedicines, 'Medicines have been successfully created.\n')

print('Enter number of Inventory Changes you want in the database')
print("(to use the default value of 100 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numIC = int(input())
except Exception:
    print('Using the default value of 100...')
    numIC = 100
if numIC < 0:
    print('Using the default value of 100...')
    numIC = 100
for i in range(numIC):  # generate INSERT statements for Inventory_Changes:
    fout.write(f'INSERT INTO Inventory_Changes (medicine_id, amount, description, nurse_id) VALUES ('
               f"{randint(1, numMedicines)}, {generateICAmount()}, '{loremIpsum}', {randint(1, numNurses)});\n")
fout.write('\n')
print(numIC, 'Inventory Changes connected to Medicines have been successfully created.\n')

# Invoices are skipped intentionally due to high complexity of correct implementation
# and uselessness for demonstration

print('Enter number of Prescriptions you want in the database')
print("(to use the default value of 500 for the stress-test, just press 'Enter'): ", end='')
try:  # check the input:
    numPrescriptions = int(input())
except Exception:
    print('Using the default value of 500...')
    numPrescriptions = 500
if numPrescriptions < 0:
    print('Using the default value of 500...')
    numPrescriptions = 500
if numPrescriptions > numMedicines * numAppointments:
    print('Number of Prescriptions cannot be bigger than')
    print('(number of Medicines) * (number of Reports [Appointments]) =')
    print(numMedicines, '*', numAppointments,
          '=', numMedicines * numAppointments)
    print('Using the value of', numMedicines *
          numAppointments, 'for Prescriptions...')
    numPrescriptions = numMedicines * numAppointments
keys = set()
# generate INSERT statements for Prescriptions:
for i in range(numPrescriptions):
    MedicineID = randint(1, numMedicines)
    ReportID = randint(1, numAppointments)
    while (MedicineID, ReportID) in keys:
        MedicineID = randint(1, numMedicines)
        ReportID = randint(1, numAppointments)
    keys.add((MedicineID, ReportID))
    fout.write(f'INSERT INTO Prescriptions (medicine_id, report_id) VALUES ('
               f"{MedicineID}, {ReportID});\n")
fout.write('\n')
print(numPrescriptions,
      'Prescriptions connecting Medicines and Reports have been successfully created.\n')

# print the report:
print('''\nScript finished. As the result, "Output.sql" file with INSERT instructions to fill in all tables''')
print('in the database with sample data was created in the same directory with the program.')
print('Your database now contains:')
print('-', numDoctors, 'Doctors and their timetable;')
print('-', numNurses, 'Nurses and their timetable;')
print('-', numStaff, 'Staff members and their timetable;')
print('-', numSyndicates, 'Medical Syndicates;')
print('-', numPatients, 'Patients and their Emergency contacts;')
print('-', numAppointments,
      'Appointments between Doctors and Patients with Reports and their schedule;')
print('-', numNoticeBoards, 'Notice Boards;')
print('-', numNotices, 'Notices connected to Notice Boards;')
print('-', numDS, 'Doctor Subscriptions;')
print('-', numNS, 'Nurse Subscriptions;')
print('-', numPS, 'Patient Subscriptions;')
print('-', numDiscounts, 'Discounts connecting Doctors and Medical Syndicates;')
print('-', numMedicines, 'Medicines;')
print('-', numIC, 'Inventory Changes connected to Medicines;')
print('-', numPrescriptions, 'Prescriptions connecting Medicines and Reports.')
print('\nCheck it out!\n')

fout.close()
