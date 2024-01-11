from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from flask_cors import CORS  # Import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Configuration
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
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

@app.route('/api/create_user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        print("Received data:", json.dumps(data, indent=2))

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        query = """
            INSERT INTO User (Username, Password, User_created, First_name, Last_name)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (data['Username'], data['Password'], datetime.utcnow(), data['First_name'], data['Last_name']))

        cnx.commit()
        cursor.close()

        return jsonify({"message": "User created successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
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
            # Join selected values into a single string or format based on your needs
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

    
# Update the /api/user_data route in your Flask backend
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

        # Assuming you have tables named Radio and Checkbox
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
