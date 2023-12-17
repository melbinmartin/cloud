from flask import Flask, request, render_template, redirect, url_for
import pymysql
import pymysql.cursors

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'database-2.cqjks2qufaje.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'Covid19'

def get_db_connection():
    return pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           db=app.config['MYSQL_DB'],
                           cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        _state = request.form['State_Name']
        _date = request.form['Date_of_Record']
        _samples = request.form['No_of_Samples']
        _deaths = request.form['No_of_Deaths']
        _positive = request.form['No_of_Positive']
        _negative = request.form['No_of_Negative']
        _discharge = request.form['No_of_Discharge']
        
        # validate received values
        if _state and _date and _samples and _deaths and _positive and _negative and _discharge:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Covid_details(State_Name, Date_of_Record, No_of_Samples, No_of_Deaths, No_of_Positive, No_of_Negative, No_of_Discharge) VALUES(%s, %s, %s, %s, %s, %s, %s)", (_state, _date, _samples, _deaths, _positive, _negative, _discharge))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('index'))
        else:
            return 'Error: Missing form data. Please fill out all fields.', 400
    except Exception as e:
        print(e)
        return f'An error occurred: {e}', 500

@app.route('/cases')
def cases():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Covid_details ORDER BY No_of_Positive ASC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('cases.html', cases=rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
