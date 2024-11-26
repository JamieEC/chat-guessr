import csv
import glob
import os

def read_twitch_chat_files():
    # Initialize an empty dictionary to store all chat data
    chat_data = {
        'time': [],
        'user_name': [],
        'user_color': [],
        'message': []
    }
    
    # Use glob to find all files matching the pattern
    for file_name in glob.glob('raw/twitch-chat-*.csv'):
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Append each row's data to the corresponding list in the dictionary
                chat_data['time'].append(row['time'])
                chat_data['user_name'].append(row['user_name'])
                chat_data['user_color'].append(row['user_color'])
                chat_data['message'].append(row['message'])
    
    return chat_data

def get_unique_user_names(chat_data):
    # Use a set to store unique user names
    unique_user_names = set(chat_data['user_name'])
    return unique_user_names

def write_messages_to_files(chat_data):
    total_message_count = 0
    # Get unique user names
    unique_user_names = get_unique_user_names(chat_data)
    
    # Create a directory to store the message files if it doesn't exist
    os.makedirs('user_messages', exist_ok=True)
    
    # Iterate over each unique user name
    for user_name in unique_user_names:
        # Skip the username "nightbot"
        if user_name.lower() == "nightbot":
            continue
        
        print("Writing messages for user:", user_name)

        # Collect all messages for the current user
        messages = [chat_data['message'][i] for i in range(len(chat_data['user_name'])) if chat_data['user_name'][i] == user_name]
        
        # Define the file path
        file_path = os.path.join('user_messages', f"{user_name}_messages.txt")
        
        total_message_count += len(messages)

        message_count = len(messages)
        print("Message count for user", user_name, ":", message_count)

        # Write messages to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            for message in messages:
                file.write(message + '\n')
        
    print("Total message count:", total_message_count)

# Example usage
all_chat_data = read_twitch_chat_files()
write_messages_to_files(all_chat_data)