from bottle import post, request
import re
from datetime import datetime

@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS')
    question = request.forms.get('QUEST')
    username = request.forms.get('USERNAME', 'User')
    
    if not mail or not question:
        return "Error: Please fill in all fields (email and question)."
    
    is_valid = True
    
    if mail.count('@') != 1:
        is_valid = False

    if mail.count('.') != 1:
        is_valid = False
    
    if is_valid:
        parts = mail.split('@')
        local = parts[0]
        domain = parts[1]
        
        if len(local) == 0:
            is_valid = False
        
        elif len(domain) == 0:
            is_valid = False
        
        elif '.' not in domain:
            is_valid = False
        
        elif domain[0] == '.' or domain[-1] == '.':
            is_valid = False
        
        else:
            last_dot = domain.rfind('.')
            if len(domain[last_dot + 1:]) < 2:
                is_valid = False
    
    if not is_valid:
        return "Error: Invalid email format. Please enter a valid email address (e.g., name@example.com)."
    
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"