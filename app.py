from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysql221b@'
app.config['MYSQL_DB'] = 'Covid19'

mysql = MySQL(app)

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
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO Covid_details(State_Name, Date_of_Record, No_of_Samples, No_of_Deaths, No_of_Positive, No_of_Negative, No_of_Discharge) VALUES(%s, %s, %s, %s, %s, %s, %s)", (_state, _date, _samples, _deaths, _positive, _negative, _discharge))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('index'))
        else:
            return 'Error: Missing form data. Please fill out all fields.', 400
    except Exception as e:
        print(e)
        return f'An error occurred: {e}', 500

@app.route('/cases')
def cases():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Covid_details ORDER BY No_of_Positive ASC")
    rows = cursor.fetchall()
    cursor.close()

    return render_template('cases.html', cases=rows)


if __name__ == "__main__":
    app.run(debug=True)
