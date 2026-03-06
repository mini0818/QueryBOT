import sqlite3

# Connect to the database
connection = sqlite3.connect('student.db')
cursor = connection.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Create tables
table_student = '''
CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(25),
    Class VARCHAR(25),
    Section VARCHAR(25),
    Age INT,
    Gender VARCHAR(10),
    EnrollmentDate DATE,
    Address VARCHAR(100),
    Email VARCHAR(50),
    Phone VARCHAR(15),
    Grade VARCHAR(2), 
    GPA FLOAT
);
'''

table_marks = '''
CREATE TABLE IF NOT EXISTS marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    Subject VARCHAR(50),
    Marks INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);
'''

table_student_documents = '''
CREATE TABLE IF NOT EXISTS student_documents (
    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    Photo BLOB,
    TenthMarksheet BLOB,
    TwelfthMarksheet BLOB,
    GraduationMarksheet BLOB,
    DocumentStatus VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);
'''

table_attendance = '''
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    TotalDays INT,
    PresentDays INT,
    AttendancePercentage FLOAT,
    AttendanceStatus VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);
'''

table_student_fees = '''
CREATE TABLE IF NOT EXISTS student_fees (
    fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    TotalFees FLOAT,
    FeesPaid FLOAT,
    FeesDue FLOAT,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);
'''

table_library = '''
CREATE TABLE IF NOT EXISTS library (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    BookTitle VARCHAR(100),
    IssueDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE
);
'''

# Execute table creation
cursor.execute(table_student)
cursor.execute(table_marks)
cursor.execute(table_student_documents)
cursor.execute(table_attendance)
cursor.execute(table_student_fees)
cursor.execute(table_library)

# Commit table creation
connection.commit()

# Insert data into student table
students = [
    ("Tejal", "MCA", "A", 22, "Female", "2024-01-10", "Mumbai", "tejal@email.com", "9876543210", "B", 3.5),
    ("Leela", "MBA", "B", 24, "Female", "2023-09-15", "Pune", "leela@email.com", "9876543220", "A", 3.7),
    ("Geeta", "MSC", "C", 26, "Female", "2024-03-01", "Delhi", "geeta@email.com", "9876543230", "C", 3.2),
]

cursor.executemany('''INSERT INTO student (Name, Class, Section, Age, Gender, EnrollmentDate, Address, Email, Phone, Grade, GPA)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', students)

connection.commit()

# Insert marks data
marks = [
    (1, "Data Science", 48),
    (1, "DSA", 50),
    (2, "Accounting", 55),
    (2, "Marketing", 60),
    (3, "Biology", 45),
    (3, "Chemistry", 48),
]

cursor.executemany('''INSERT INTO marks (student_id, Subject, Marks) VALUES (?, ?, ?)''', marks)

# Insert student_documents data
documents = [
    (1, None, None, None, None, "Submitted"),
    (2, "Submitted", None, "Submitted", None, "Not Submitted"),
    (3, None, "Submitted", None, None, "Submitted"),
]

cursor.executemany('''INSERT INTO student_documents (student_id, Photo, TenthMarksheet, TwelfthMarksheet, GraduationMarksheet, DocumentStatus)
                      VALUES (?, ?, ?, ?, ?, ?)''', documents)

# Insert attendance data
attendance = [
    (1, 180, 170, 94.44, "Regular"),
    (2, 180, 100, 55.55, "Defaulter"),
    (3, 180, 150, 83.33, "Regular"),
]

cursor.executemany('''INSERT INTO attendance (student_id, TotalDays, PresentDays, AttendancePercentage, AttendanceStatus)
                      VALUES (?, ?, ?, ?, ?)''', attendance)

# Insert student_fees data
fees = [
    (1, 50000, 20000, 30000),
    (2, 60000, 25000, 35000),
    (3, 40000, 15000, 25000),
]

cursor.executemany('''INSERT INTO student_fees (student_id, TotalFees, FeesPaid, FeesDue)
                      VALUES (?, ?, ?, ?)''', fees)

# Insert library data
library = [
    (1, "Data Science Handbook", "2025-01-15", "2025-02-15"),
    (2, "Marketing Essentials", "2025-01-20", "2025-02-20"),
    (3, "Biology Basics", "2025-01-22", "2025-02-22"),
]

cursor.executemany('''INSERT INTO library (student_id, BookTitle, IssueDate, ReturnDate)
                      VALUES (?, ?, ?, ?)''', library)

# Commit data insertion
connection.commit()

# Update attendance table: Set AttendanceStatus based on AttendancePercentage
cursor.execute('''
    UPDATE attendance
    SET AttendanceStatus = 
        CASE 
            WHEN AttendancePercentage < 75 THEN "Defaulter"
            ELSE "Regular"
        END
''')

# Update student_documents table: Set DocumentStatus based on document submission status
cursor.execute('''
    UPDATE student_documents
    SET DocumentStatus = 
        CASE 
            WHEN Photo IS NOT NULL AND TenthMarksheet IS NOT NULL 
                 AND TwelfthMarksheet IS NOT NULL AND GraduationMarksheet IS NOT NULL 
            THEN "All Submitted"
            ELSE "Pending"
        END
''')

# Commit updates
connection.commit()

# Function to fetch column names
def fetch_column_names(cursor):
    return [description[0] for description in cursor.description]

# Function to print table data
def print_table_data(query, cursor):
    cursor.execute(query)
    columns = fetch_column_names(cursor)
    print(f"Columns: {columns}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Print all table data
print("\nStudent Table Data:")
print_table_data('''SELECT * FROM student''', cursor)

print("\nMarks Table Data:")
print_table_data('''SELECT * FROM marks''', cursor)

print("\nStudent Documents Table Data:")
print_table_data('''SELECT * FROM student_documents''', cursor)

print("\nAttendance Table Data:")
print_table_data('''SELECT * FROM attendance''', cursor)

print("\nStudent Fees Table Data:")
print_table_data('''SELECT * FROM student_fees''', cursor)

print("\nLibrary Table Data:")
print_table_data('''SELECT * FROM library''', cursor)

# Close the connection
connection.close()
print("\nDatabase connection closed.")
