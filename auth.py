from db import is_email_in_db, is_phone_number_in_db, validate_password, bcrypt, create_user
from fn import is_valid_email, is_date_of_birth_valid, is_valid_phone_number

def authenticate_user(identifier, identifier_type, password):
    if identifier_type == 'email':
        user = is_email_in_db(identifier)
    elif identifier_type == 'phone-number':
        user = is_phone_number_in_db(identifier)
    else:
        return {'success': False, 'user': None, 'message': 'Request unsuccessful, error from our end'}

    if user['success']:
        next = validate_password(password=password, user_id=user)
        if next['success'] == True:
            return {'success': True, 'user': user, 'message': 'Login successful'}
        else:
            return next
    else:
        return {'success': False, 'user': None, 'message': f'{identifier_type.capitalize()} not found, try signing up'}


def login(password, **kwargs):
    if 'email' in kwargs:
        return authenticate_user(kwargs['email'], 'email', password)
    elif 'phone-number' in kwargs:
        return authenticate_user(kwargs['phone-number'], 'phone-number', password)
    else:
        return {'success': False, 'user': None, 'message': 'No valid login identifier provided'}


def signup(**kwargs):
    name = kwargs.get('name')
    email = kwargs.get('email')
    password = kwargs.get('password')
    dob = kwargs.get('dob')
    phone_number = kwargs.get('phone_number')


    # VERIFICATION IF THE INPUTS ARE AVAILABLE
    if not name or not email or not password or not dob or not phone_number:
        return {'success': False, 'message': 'All input are required'}
    
    
    # SECOND VERIFICATION FOR THE DATE OF BIRTH
    _dob = is_date_of_birth_valid(dob)
    if _dob['success' == False]:
        return {f'success': False, 'message': {_dob["message"]}}
    
    
    # SECOND VERIFICATION FOR THE EMAIL
    if not is_valid_email(email):
        return {'success': False, 'message': f'{email} is not a valid email address'}
    
    #SECOND VERIFICATION FOR THE PHONE NUMBER
    if not is_valid_phone_number(phone_number_input=phone_number):
        return {'success': False, 'message': f'{phone_number} is not a valid phone number'}
    
    #SECOND VERIFICATION FOR PASSWORD
    if not len(password) == 4:
        return {'success': False, 'message': 'pin must be 4 digits'}
    

    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user = create_user(name=name, email=email, password=password, dob=dob, phone_number=phone_number)
    if user['success'] == True:
        print('Account created successfully')