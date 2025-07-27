import psycopg2
import csv

# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tt_project",
            user="postgres",
            password="ubaid"
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

# Create table for timeslots2
def create_timeslots_table(conn):
    try:
        cur = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS timeslots2 (
            id SERIAL PRIMARY KEY,
            start_time VARCHAR(10),
            end_time VARCHAR(10)
        );
        '''
        cur.execute(create_table_query)
        conn.commit()
        print("Timeslots2 table created successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while creating timeslots2 table: {e}")

# Create table for theory and lab slots
def create_slots_table(conn):
    try:
        cur = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS slots (
            day VARCHAR(20),
            id INT,
            slot VARCHAR(10)
        );
        '''
        cur.execute(create_table_query)
        conn.commit()
        print("Slots table created successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while creating slots table: {e}")

def create_course_table(conn):
    try:
        cur = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS course_structure (
            Semester INT,
            Course_Catagory VARCHAR(10),
            Course_Number VARCHAR(20),
            Course_title VARCHAR(50),
            Contact_Periods_LTP VARCHAR(10),
            Credits INT
        );
        '''
        cur.execute(create_table_query)
        conn.commit()
        print("Course Structure table created successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while creating Course Structure table: {e}")


def create_faculty_table(conn):
    try:
        cur = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS faculty_course (
            Semester INT,
            Course_Number VARCHAR(20),
            Faculty VARCHAR(500),
            Available_Timeslots VARCHAR(500),
            Course_Incharge VARCHAR(500)
        );
        '''
        cur.execute(create_table_query)
        conn.commit()
        print("Faculty Course table created successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while creating Faculty Course table: {e}")

def create_facultyID_table(conn):
    try:
        cur = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS faculty_id (
            Faculty_ID VARCHAR(20),
            Name VARCHAR(500)
        );
        '''
        cur.execute(create_table_query)
        conn.commit()
        print("FacultyID table created successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while creating FacultyID table: {e}")



# Insert timeslots2 from CSV
def insert_timeslots(conn, csv_file):
    try:
        cur = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                cur.execute("INSERT INTO timeslots2 (id, start_time, end_time) VALUES (%s, %s, %s)", row)
        conn.commit()
        print("Timeslots inserted successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while inserting timeslots2: {e}")

# Insert slots (T1, T2, L1M, etc.) from CSV
def insert_slots(conn, csv_file):
    try:
        cur = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                cur.execute("INSERT INTO slots (day, id, slot) VALUES (%s, %s, %s)", row)
        conn.commit()
        print("\nSlots inserted successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while inserting slots: {e}")

def insert_course(conn, csv_file):
    try:
        cur = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                cur.execute("INSERT INTO course_structure (Semester,Course_Catagory,Course_Number,Course_title,Contact_Periods_LTP,Credits) VALUES (%s, %s, %s, %s, %s, %s)", row)
        conn.commit()
        print("\nCourse Structure inserted successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while inserting Course Structure: {e}")

def insert_faculty(conn, csv_file):
    try:
        cur = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                cur.execute("INSERT INTO faculty_course (Semester,Course_Number,Faculty,Available_Timeslots,Course_Incharge) VALUES (%s, %s, %s, %s, %s)", row)
        conn.commit()
        print("\nFaculty Course inserted successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while inserting Faculty Course: {e}")


def insert_facultyID(conn, csv_file):
    try:
        cur = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                cur.execute("INSERT INTO faculty_id (Faculty_ID,Name) VALUES (%s, %s)", row)
        conn.commit()
        print("\nFacultyID inserted successfully.")
        cur.close()
    except Exception as e:
        print(f"Error while inserting FacultyID: {e}")


def display_table(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM timeslots2;")
        rows = cur.fetchall()

        print("\nTimeslots Table:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print("Error while displaying table:", e)

def display_table2(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM slots;")
        rows = cur.fetchall()

        print("\nSlots Table:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print("Error while displaying table:", e)

def display_table3_course(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM course_structure;")
        rows = cur.fetchall()

        print("\nCourse Structure Table:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print("Error while displaying table:", e)

def display_table4_faculty(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM faculty_course;")
        rows = cur.fetchall()

        print("\nFaculty Course Table:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print("Error while displaying table:", e)

def display_table5_facultyID(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM faculty_id;")
        rows = cur.fetchall()

        print("\nFaculty ID Table:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print("Error while displaying table:", e)

# Display the combined table
def display_combined_table(conn):
    try:
        cur = conn.cursor()
        query = '''
        SELECT slots.day, 
            CONCAT(timeslots2.start_time, ' - ', timeslots2.end_time) AS timeslot, 
            slots.slot
        FROM 
            slots
        JOIN 
            timeslots2 
            ON slots.id = timeslots2.id

        '''
        # ORDER BY 
        #     slots.day, 
        #     timeslots2.start_time;
        cur.execute(query)
        rows = cur.fetchall()

        print("\nCombined Table:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print(f"Error while displaying combined table: {e}")

# Display the combined table 2
def display_combined_table2(conn):
    try:
        cur = conn.cursor()


        query = '''
        WITH SplitFaculty AS (
            -- Split the 'faculty' column into individual Faculty_IDs
            SELECT 
                Semester,
                Course_Number,
                regexp_split_to_table(Faculty, ',') AS Faculty_ID
            FROM 
                faculty_course
        ),
        MappedFaculty AS (
            -- Join the split Faculty_IDs with facultyID table to get the names
            SELECT 
                sf.Semester,
                sf.Course_Number,
                f.Name
            FROM 
                SplitFaculty sf
            LEFT JOIN 
                faculty_id f ON sf.Faculty_ID = f.Faculty_ID  -- Ensure both are of the same type
        ),
        AggregatedFaculty AS (
            -- Aggregate the names back into a comma-separated string per course
            SELECT 
                Semester,
                Course_Number,
                string_agg(Name, ', ') AS Faculty_Names
            FROM 
                MappedFaculty
            GROUP BY 
                Semester, Course_Number
        )
        -- Select the final result
        SELECT 
            Semester,
            Course_Number,
            Faculty_Names AS Faculty
        FROM 
            AggregatedFaculty;


        '''
        cur.execute(query)
        rows = cur.fetchall()

        print("\nCombined Table2:")
        for row in rows:
            print(row)
        cur.close()
    except Exception as e:
        print(f"Error while displaying combined table2: {e}")

# Main function
def main():
    conn = connect_db()
    if conn is None:
        return

    # Create tables
    create_timeslots_table(conn)
    create_slots_table(conn)
    create_course_table(conn)
    create_faculty_table(conn)
    create_facultyID_table(conn)

    # Insert data into tables from CSV
    insert_timeslots(conn, 'timeslots2.csv')
    display_table(conn)

    insert_slots(conn, 'slots.csv')
    display_table2(conn)

    # Display the combined table
    display_combined_table(conn)

    insert_course(conn, 'course_structure.csv')
    display_table3_course(conn)

    insert_faculty(conn, 'faculty_course.csv')
    display_table4_faculty(conn)

    insert_facultyID(conn,'facultyID.csv')
    display_table5_facultyID(conn)

    display_combined_table2(conn)

    

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
