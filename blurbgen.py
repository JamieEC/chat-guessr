import google.generativeai as genai



def gemini_response(prompt):
    genai.configure(api_key="AIzaSyCWeipLRzrBZnz-R3iBzQwTvDlbrEHQNC4")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return(response.text)

def get_user_messages(username):
    with open(f'user_messages/{username}_messages.txt', 'r', encoding='utf-8') as f:
        return f.read()
    

#print(gemini_response("Explain how AI works"))
username = input("Enter username: ")
messages = (get_user_messages(username))

initial_response = gemini_response("summarise this users' personality and interests based on their messages:" + messages)
#print(initial_response)

bio = gemini_response("reduce this down to a bio of about 2 or 3 sentences : " + initial_response)
print("===============================================")
print(bio)

write_to_file = input("Would you like to write the bio to a file? (Y/N): ").strip().upper()

if write_to_file == 'Y':
    with open(f'user_blurbs/{username}_blurb.txt', 'w', encoding='utf-8') as file:
        file.write(bio)
    print(f"Bio has been written to user_blurbs/{username}_blurb.txt")
else:
    print("Exiting without writing to file.")
