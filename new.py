from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from flask_cors import CORS  # Import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

try:
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(30) NOT NULL,
            Password VARCHAR(60) NOT NULL,
            User_created TIMESTAMP NOT NULL,
            First_name VARCHAR(20),
            Last_name VARCHAR(40)
        )
    """)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied. Check username and password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    if 'cnx' in locals():
        cnx.close()

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view endpoint

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Query the user by ID from the User table
        query = "SELECT * FROM User WHERE ID = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            user = User(user_data[0])  # Assuming the first column is the user ID
            cursor.close()
            return user

    except Exception as e:
        print(str(e))

    finally:
        if 'cnx' in locals():
            cnx.close()

    return None  # Return None if user not found or an error occurred

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Check if the username exists in the database
        check_user_query = "SELECT ID, Password FROM User WHERE Username = %s"
        cursor.execute(check_user_query, (data['username'],))
        user_data = cursor.fetchone()

        if not user_data:
            # User not found, return authentication failure status
            cursor.close()
            return jsonify({"error": "Invalid credentials"}), 401

        user_id, hashed_password = user_data

        # Validate the password using Flask-Login's check_password_hash
        if login_user(User(user_id), remember=True) and current_user.is_authenticated and \
                current_user.check_password_hash(hashed_password, data['password']):
            cursor.close()
            return jsonify({"message": "Login successful"})
        else:
            # Incorrect password, return authentication failure status
            logout_user()  # Logout in case of incorrect password
            cursor.close()
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/api/create_user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        print("Received data:", json.dumps(data, indent=2))

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Check if the username already exists
        existing_user_query = "SELECT ID FROM User WHERE Username = %s"
        cursor.execute(existing_user_query, (data['Username'],))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return jsonify({"error": "Username already exists. Please choose a different username."}), 400

        # Insert the new user
        insert_user_query = """
            INSERT INTO User (Username, Password, User_created, First_name, Last_name)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_user_query, (data['Username'], data['Password'], datetime.utcnow(), data['First_name'], data['Last_name']))
        cnx.commit()

        # Log in the user after successful registration
        user = User(cursor.lastrowid)  # Assuming lastrowid contains the ID of the newly created user
        login_user(user)

        cursor.close()

        return jsonify({"message": "User created successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

    
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})
    
# Radio table route
@app.route('/api/radio_questions', methods=['GET'])
def get_radio_questions():
    # Fetch questions from a separate Python file (questions.py)
    from questions import radio_questions
    return jsonify(radio_questions)

# Checkbox table route
@app.route('/api/checkbox_questions', methods=['GET'])
def get_checkbox_questions():
    # Fetch questions from a separate Python file (questions.py)
    from questions import checkbox_questions
    return jsonify(checkbox_questions)

# Submit radio answers to the database
@app.route('/api/submit_radio_answers', methods=['POST'])
def submit_radio_answers():
    try:
        data = request.get_json()

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        for question_id, answer_value in data.items():
            query = """
                INSERT INTO Radio (UserID, QuestionID, Value, Created, Version)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (1, question_id, answer_value, datetime.utcnow(), 1))  # Replace 1 with actual user ID

        cnx.commit()
        cursor.close()

        return jsonify({"message": "Radio answers submitted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
# Submit checkbox answers to the database
@app.route('/api/submit_checkbox_answers', methods=['POST'])
def submit_checkbox_answers():
    try:
        data = request.get_json()

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        for question_id, selected_values in data.items():
            # Join selected values into a single string
            combined_values = ', '.join(selected_values)

            query = """
                INSERT INTO Checkbox (UserID, QuestionID, Value, Created, Version)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (1, question_id, combined_values, datetime.utcnow(), 1))  # Replace 1 with actual user ID

        cnx.commit()
        cursor.close()

        return jsonify({"message": "Checkbox answers submitted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/user_data', methods=['GET'])
def get_user_data():
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        if 'username' in request.args:
            # Search for a specific user by username
            query = "SELECT * FROM User WHERE Username LIKE %s"
            cursor.execute(query, ('%' + request.args['username'] + '%',))
        else:
            # Fetch all users
            query = "SELECT * FROM User"
            cursor.execute(query)

        data = cursor.fetchall()

        user_data = [{'ID': row[0], 'Username': row[1], 'Password': row[2], 'User_created': row[3], 'First_name': row[4], 'Last_name': row[5]} for row in data]

        cursor.close()

        return jsonify(user_data)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/user_answers', methods=['GET'])
def get_user_answers():
    try:
        username = request.args.get('username')

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Check if the user exists
        cursor.execute("SELECT ID FROM User WHERE Username = %s", (username,))
        user_id = cursor.fetchone()

        if not user_id:
            # User not found, return 404 status
            return jsonify({"error": "User not found"}), 404

        # 
        query = """
            SELECT r.QuestionID, r.Value AS RadioAnswer, c.Value AS CheckboxAnswer
            FROM Radio r
            LEFT JOIN Checkbox c ON r.QuestionID = c.QuestionID
            WHERE r.UserID = %s OR c.UserID = %s
        """

        cursor.execute(query, (user_id[0], user_id[0]))
        data = cursor.fetchall()

        user_answers = [{'QuestionID': row[0], 'RadioAnswer': row[1], 'CheckboxAnswer': row[2]} for row in data]

        cursor.close()

        return jsonify(user_answers)

    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)
