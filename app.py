from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

# Flask application configuration
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'database-2.cqjks2qufaje.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'Studentdatabase'

# Function to connect to the database
def get_db_connection():
    return pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           db=app.config['MYSQL_DB'],
                           cursorclass=pymysql.cursors.DictCursor)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle student data submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        student_id = request.form['Student_ID']
        name = request.form['Name']
        enrollment_date = request.form['Enrollment_Date']
        course = request.form['Course']
        email = request.form['Email']
        phone_number = request.form['Phone_Number']
        
        # Validate received values
        if student_id and name and enrollment_date and course and email and phone_number:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Student_Details(Student_ID, Name, Enrollment_Date, Course, Email, Phone_Number) VALUES(%s, %s, %s, %s, %s, %s)", (student_id, name, enrollment_date, course, email, phone_number))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            return 'Error: Missing form data. Please fill out all fields.', 400
    except Exception as e:
        return f'An error occurred: {e}', 500

# Route to view students
@app.route('/students')
def students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student_Details")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('cases.html', students=rows)

# Main function to run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
