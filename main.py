from datetime import datetime
from dateutil import parser
from datetime import date
import re


# REGULAR EXPRESSION TO VERIFY EMAIL
def is_valid_email(email):
    """Basic email format validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

from datetime import datetime
from dateutil import parser
from datetime import date

def is_date_of_birth_valid(dob_input):
    """
    Validates the date of birth and checks if the user is 18 years or older.
    The function accepts the date of birth in various formats.

    :param dob_input: The date of birth input as a string (e.g., '1990-05-15', '15/05/1990', etc.)
    :return: A tuple (is_valid: bool, message: str)
    """
    try:
        # Parse the input date using dateutil.parser, which can handle various formats
        dob = parser.parse(dob_input).date()
        
        # Get today's date
        today = date.today()

        # Calculate age
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age >= 18:
            return {'success': True, 'message': 'Age successfully verified'}
        else:
            return {'success': False, 'message': 'User is less than 18 years old'}
    
    except (ValueError, TypeError):
        # Catch errors if the date is invalid or cannot be parsed
        return {'success': False, 'message': f'{dob_input} is an invalid date format/input'}
    
    
def is_valid_phone_number(phone_number_input):
    """
    VALIDATES THE PHONE NUMBER IF IT IS IN THE RIGHT FORMAT.
    
    THIS FUNCTION VERIFIES IT FOR NIGERIAN PHONE NUMBER.
    """
    
    #CHECKS THE LENGTH OF THE PHONE NUMBER
    if len(phone_number_input) != 14 or len(phone_number_input) != 11:
        return {'success': False, 'message': 'Invalid phone number'}
        
    #NESTED IF CHECK IF NUMBER IS IN THIS FORMAT "080********"
    if phone_number_input.startsWith('0'):
        if phone_number_input[1] in ['8', '7', '9']:
            if phone_number_input[2] in ['0', '1']:
                return {'success': True, 'message': 'Phone number was successfully verified'}
            else:
                return {'success': False, 'message': 'Invalid phone number'}
        else:
            return {'success': False, 'message': 'Invalid phone number'}
        
    #CHECKS IF NUMBER IS IN THIS FORMAT "+23480********"
    elif phone_number_input.startswith('+234'):
        if phone_number_input[4] in ['8', '7', '9']:
            if phone_number_input[5] in ['0', '1']:
                return {'success': True, 'message': 'Phone number was successfully verified'}
            else:
                return {'success': False, 'message': 'Invalid phone number'}
        else:
            return {'success': False, 'message': 'Invalid phone number'}
        
    else:
        return {'success': False, 'message': 'Invalid phone number'}
                
            