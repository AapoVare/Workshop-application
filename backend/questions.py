""" radio_questions = {
    1: "What is your favorite color?",
    2: "How often do you exercise?",
    # Add more questions as needed
}
 """

radio_questions = {
    1: {
        "question": "What is your favorite color?",
        "options": ["Red", "Blue", "Green", "Other"]
    },
    2: {
        "question": "What is your favorite season?",
        "options": ["Summer", "Spring", "Autumn", "Winter"]
    },

    # Add more questions as needed
}


checkbox_questions = {
    3: {
        "question": "Which programming languages do you know?",
        "options": ["Python", "JavaScript", "Java", "C++", "Ruby"]
    },
    # Add more questions as needed
}

short_text_questions = {
    4: {
        "question": "What's your favorite meal?"
    }
}

long_text_questions = {
    5: {
        "question": "Write a short story about your favorite season and why."
    }
}


""" def print_question(question_id):
    if question_id in radio_questions:
        question = radio_questions[question_id]["question"]
        options = radio_questions[question_id]["options"]

        print(f"Question {question_id}: {question}")
        #print("Options:")
        #for i, option in enumerate(options, 1):
           # print(f"{i}. {option}")
    else:
        print("Invalid question ID. Please choose a valid ID.")

# Get user input
user_input = input("Enter a question ID: ")
try:
    question_id = int(user_input)
    print_question(question_id)
except ValueError:
    print("Invalid input. Please enter a valid number.") """