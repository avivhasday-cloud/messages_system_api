

def create_user_validations(data):
    if data.get('username') is None:
        return "Username is required!"

    if data.get('email') is None:
        return "Email is required!"
    
    if data.get('password') is None:
        return "Password is required!"

    return

def write_message_validations(data):
    if data is None:
        return "Missing parameters!"
    if data.get('sender') is None:
        return "Sender is required!"

    if data.get('receiver') is None:
        return "Receiver is required!"
    
    if data.get('subject') is None:
        return "Subject is required!"
    
    if data.get('content') is None:
        return "Content is required!"

    return