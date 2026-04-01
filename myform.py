from bottle import post, request
import re
from datetime import datetime

@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS')
    question = request.forms.get('QUEST')
    username = request.forms.get('USERNAME', 'User')
    
    # Проверка заполненности полей
    if not mail or not question:
        return "Error: Please fill in all fields (email and question)."
    
    # Простая проверка email
    is_valid = True
    
    # 1. Ровно один @
    if mail.count('@') != 1:
        is_valid = False
    
    # 2. Разделяем на части
    if is_valid:
        parts = mail.split('@')
        local = parts[0]
        domain = parts[1]
        
        # 3. Локальная часть не пустая
        if len(local) == 0:
            is_valid = False
        
        # 4. Домен не пустой
        elif len(domain) == 0:
            is_valid = False
        
        # 5. В домене есть точка
        elif '.' not in domain:
            is_valid = False
        
        # 6. Домен не начинается и не заканчивается на точку
        elif domain[0] == '.' or domain[-1] == '.':
            is_valid = False
        
        # 7. После последней точки минимум 2 символа
        else:
            last_dot = domain.rfind('.')
            if len(domain[last_dot + 1:]) < 2:
                is_valid = False
    
    if not is_valid:
        return "Error: Invalid email format. Please enter a valid email address (e.g., name@example.com)."
    
    # Получение текущей даты
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"