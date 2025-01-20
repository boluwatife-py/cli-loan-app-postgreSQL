import getpass
from fn import is_valid_email, is_valid_phone_number
from colorama import Fore, Style, Back
import questionary


def home(request):
    try:
        response = ['Login', 'Create a new account', 'Admin', 'View About']
        if request in response:
            if request == 'Login':
                login()
            elif request == 'Create a new account':
                signup()
            elif request == 'Admin':
                admin()
            elif request == 'View About':
                about()
                
        else:
            return {'success': False, 'message': "Invalid input"}
            
    except:
        return {'success': False, 'message': "Invalid input"}
    
    
def login():
    def identifier():
        identifier = input('Enter your email or phone number >>>  ')
        if is_valid_email(identifier):
            identifier_type = 'email'
        elif is_valid_phone_number(identifier):
            identifier_type = 'phone-number'
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid email or phone number :(" + Style.RESET_ALL)
            print(Fore.BLUE + "Renter your email or password" + Style.RESET_ALL)
            print(Fore.MAGENTA + Back.LIGHTCYAN_EX + "press exit to quit")
    
    identifier()
        
        
    pin = getpass.getpass('Enter your password >>>   ')
    
def signup():
    pass

def admin():
    pass

def about():
    print(
    """
    
    """
    )