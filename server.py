import csv
from flask import Flask, jsonify, render_template
import os
import random

app = Flask(__name__)

def load_all_messages(file_path='all_messages.csv'):
    messages = []
    user_message_count = {}

    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            user_name = row['user_name']
            message = row['message']
            messages.append((user_name, message))

            # Count messages for each user
            if user_name in user_message_count:
                user_message_count[user_name] += 1
            else:
                user_message_count[user_name] = 1

    return messages, user_message_count

def get_message_and_guesses():
    messages, user_message_count = load_all_messages()  # Load messages and user counts

    # Filter users with more than 9 messages
    valid_users = {user: count for user, count in user_message_count.items() if count > 25}

    if not valid_users:
        return None, None, []  # No valid users

    # Randomly select a user from valid users
    selected_user = random.choice(list(valid_users.keys()))

    # Filter messages for the selected user
    user_messages = [msg for user, msg in messages if user == selected_user]

    # Randomly select a valid message from the user's messages
    selected_message = None
    while True:  # Keep trying indefinitely
        selected_message = random.choice(user_messages)
        if len(selected_message) > 5:  # Check if the message length is greater than 5
            break
        # If the message is too short, continue the loop to select another message

    # Pick 4 random usernames for guesses (excluding the chosen username)
    remaining_users = [u for u in valid_users.keys() if u != selected_user]
    guesses = random.sample(remaining_users, 3)
    # Insert the correct username at a random position
    guesses.insert(random.randint(0, len(guesses)), selected_user)

    return selected_message, selected_user, guesses

def get_user_blurb(username):
    blurb_file_path = f'user_blurbs/{username}_blurb.txt'
    if os.path.exists(blurb_file_path):
        with open(blurb_file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_message')
def get_message():
    message, username, guesses = get_message_and_guesses()
    blurb = get_user_blurb(username)  # Get the blurb for the correct username
    print(message)
    print(username)
    print(guesses)
    return jsonify({'message': message, 'guesses': guesses, 'username': username, 'blurb': blurb})

if __name__ == '__main__':
    app.run(host='0.0.0.0')