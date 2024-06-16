from flask import Flask, render_template, request,redirect,url_for,flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__)


# Configure MySQL connection
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='root'
app.config['MYSQL_DB'] = 'hrms'
mysql = MySQL(app)
app.secret_key='your_secret_key'

# Function to create database and table if they don't exist
def create_database():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(app.config['MYSQL_DB']))
        cur.execute("USE {}".format(app.config['MYSQL_DB']))
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_info(
                user_name VARCHAR(20) PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL
            )
        """)
        mysql.connection.commit()
        cur.close()

# Ensure the database and table are created when the app starts
create_database()

@app.route('/')
def Home():
    return render_template('Home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_info WHERE email = %s AND password=%s", (email,password))
        user = cur.fetchone()
        cur.close()
                                     
        # if user and check_password_hash(user[1], password):
        #     # Here, user['password'] is hashed password from the database
        #     return redirect(url_for('success'))
        if user:
            flash('succesufull logged in','success')
            return redirect(url_for('Home'))
        # else:
        #     error = "Invalid email or password"
        #     return render_template('login.html', error=error)
        else:
            flash('Incorrect email/password','error')
            return render_template('Home.html')
        
    return render_template('Home.html')

@app.route('/success')
def success():
    return "Login successful!"

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_info WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            cur.close()  # Close the cursor if the user already exists
            flash('User already exists! Please log in.','error')
            return redirect(url_for('signup'))
        else:
            # Insert the new user into the database
            cur.execute("INSERT INTO user_info(user_name, email, password) VALUES (%s, %s, %s)",(username, email, password))
            mysql.connection.commit()
            cur.close()  # Close the cursor after the operation is complete
            flash('Registration successful! Please login.','success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/att')
def att():
   if request.method == 'GET':

            cur = mysql.connection.cursor()

            cur.execute("SELECT * FROM attendence")

            user = cur.fetchall()
            cur.close()

            return render_template("att.html", user=user)
   return render_template("att.html")



@app.route('/dash')
def dash():
    return render_template('dash.html')


@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if request.method == 'POST':
        user_id = request.form['user_id']
        today = datetime.now().date()
        cur = mysql.connection.cursor()
        cur.execute("SELECT last_updated FROM attendence WHERE id = %s", (user_id,))
        result = cur.fetchone()

        if result:
            last_updated = result[0]
            if last_updated < today:
        
        # Example SQL (ensure you have an appropriate table structure)
                query = "update attendence set days=days+1, last_updated=%s where id=%s"
                cur.execute(query, (today,user_id,))
        
                mysql.connection.commit()
                cur.close()
        
                flash('Attendance marked successfully!', 'success')
            else:
                flash('Attendance already marked', 'error')

        return redirect(url_for('att'))
@app.route('/payroll')
def payroll():
    if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute("SELECT id,name,days,salary_perday,days*salary_perday FROM attendence")
            user = cur.fetchall()
            cur.close()
            return render_template("payroll.html", user=user)
    return render_template('payroll.html')
if __name__ == '__main__':
    app.run(debug=True)
