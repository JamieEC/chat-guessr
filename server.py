from flask import Flask, jsonify, render_template
import os
import random

app = Flask(__name__)

def get_message_and_guesses():
    user_stats = {}
    for filename in os.listdir('user_messages'):
        if filename.endswith('_messages.txt'):
            username = filename.replace('_messages.txt', '')
            with open(os.path.join('user_messages', filename), 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f)
            user_stats[username] = line_count

    # Get subset of 8 users
    user_stats = {k: v for k, v in user_stats.items() if v >= 9}
    user_stats = dict(sorted(user_stats.items(), key=lambda x: x[1], reverse=True))
    user_subset = dict(random.sample(list(user_stats.items()), min(8, len(user_stats))))

    # Pick random username from subset
    username = random.choice(list(user_subset.keys()))
    with open(f'user_messages/{username}_messages.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        valid_lines = [line.strip() for line in lines if len(line.strip()) > 5]
        message = random.choice(valid_lines)

    # Pick 4 random usernames for guesses (excluding the chosen username)
    remaining_users = [u for u in user_subset.keys() if u != username]
    guesses = random.sample(remaining_users, 4)
    # Insert the correct username at a random position
    guesses.insert(random.randint(0, len(guesses)), username)

    return message, username, guesses

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_message')
def get_message():
    message, username, guesses = get_message_and_guesses()
    print(message)
    print(username)
    print(guesses)
    return jsonify({'message': message, 'guesses': guesses, 'username': username})

@app.route('/get_5050/<correct_username>')
def get_5050(correct_username):
    _, _, guesses = get_message_and_guesses()
    incorrect_guesses = [guess for guess in guesses if guess != correct_username]
    # Randomly select two incorrect guesses
    if len(incorrect_guesses) > 2:
        incorrect_guesses = random.sample(incorrect_guesses, 2)
    return jsonify({'incorrect_guesses': incorrect_guesses})

if __name__ == '__main__':
    app.run(host='0.0.0.0')