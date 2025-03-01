import csv
from flask import Flask, jsonify, render_template, request
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

    # Filter users with more than a certain number of messages
    valid_users = {user: count for user, count in user_message_count.items() if count > 10}

    if not valid_users:
        return None, None, []  # No valid users

    # Filter messages that are over 5 characters and belong to valid users
    valid_messages = [(user, msg) for user, msg in messages if len(msg) > 5 and user in valid_users]

    if not valid_messages:
        return None, None, []  # No valid messages

    # Randomly select a valid message and its user
    selected_user, selected_message = random.choice(valid_messages)

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

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    username = data.get('username')
    score = data.get('score')

    if not username or score is None:
        return jsonify({'success': False, 'error': 'Invalid data'})

    # Save the score to a file
    with open('scores.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, score])

    return jsonify({'success': True})

@app.route('/get_high_scores')
def get_high_scores():
    scores = []
    if os.path.exists('scores.csv'):
        with open('scores.csv', mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2:  # Ensure there are two columns
                    username, score = row
                    scores.append({'username': username, 'score': score})
    
    # Sort scores in descending order
    scores.sort(key=lambda x: int(x['score']), reverse=True)
    
    # Limit to top 10 scores
    top_scores = scores[:10]
    
    return jsonify({'scores': top_scores})

if __name__ == '__main__':
    app.run(host='0.0.0.0')