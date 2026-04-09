from bottle import post, request
import re
from datetime import datetime
import os
import json

#import pdb

DATA_FILE = "questions.json"
user_questions = {}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS')
    question = request.forms.get('QUEST')
    username = request.forms.get('USERNAME', 'User')

    user_questions[mail] = [username, question]
    #pdb.set_trace()
    
    if not mail or not question or not username:
        return "Error: Please fill in all fields (email, question and username)."
    
    if len(question)<3 or  question.isdigit():
        return "Error: The question is not correct (too small or only digits)."

    if len(mail) > 20:
        return "Error: The email is too long (try email with less than 20 symbols)."
   

    if mail.count('@') != 1:
        return "Error: Email must contain exactly one '@' symbol."

    
    parts = mail.split('@')
    local = parts[0]
    domain = parts[1]
    
    if len(local) == 0:
        return "Error: Local part cannot be empty."
    
    if not local[0].isalpha():
        return "Error: The first char must be a letter."
    
    allowed_local_pattern = r'^[a-zA-Z][a-zA-Z0-9\.\-_+]*$'
    if not re.match(allowed_local_pattern, local):
        return "Error: Local part contains invalid characters."
    
    if len(domain) == 0:
        return "Error: Domain part cannot be empty."
    
    if '.' not in domain:
        return "Error: Domain must contain at least one dot. Example: example.com"
    
    if domain.startswith('.'):
        return "Error: Domain cannot start with a dot."
    if domain.endswith('.'):
        return "Error: Domain cannot end with a dot."
    
    if domain.count('.') != 1:
        return "Error: Domain can containt only 1 dot"
    
    last_dot = domain.rfind('.')
    tld = domain[last_dot + 1:]
    
    if len(tld) < 2:
        return "Error: Top-level domain is too short"
    if len(tld) > 6:
        return "Error: Top-level domain is too long"
    
    if not tld.isalpha():
        return "Error: Top-level domain must contain only letters"
    
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")

    data = load_data()

    if mail in data:
        data[mail]['mail'] = mail
        
        if question not in data[mail]['questions']:
            data[mail]['questions'].append(question)
    else:
        data[mail] = {
            'questions': [question]
        }  

    save_data(data)
    return f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"
