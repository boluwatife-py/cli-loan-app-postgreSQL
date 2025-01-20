import getpass
from fn import is_valid_email, is_valid_phone_number, is_date_of_birth_valid, is_valid_fullname, show_progress, ErrorBar, SuccessBar
from colorama import Fore, Style, Back, init
import questionary
import sys
from auth import login, signup
import os
import platform



init()
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

class Pages:
    def __init__(self):
        pass

    def main(self):
        clear_screen()
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Login",
                "Create a new account",
                "Admin",
                "View About",
                "Quit"
            ],
        ).ask()
        self.home(action)

    def home(self, request):
        try:
            response = ['Login', 'Create a new account', 'Admin', 'View About', 'Quit']
            if request in response:
                if request == 'Login':
                    self._login()
                elif request == 'Create a new account':
                    self._signup()
                elif request == 'Admin':
                    self.admin()
                elif request == 'View About':
                    self.about()
                elif request == 'Quit':
                    quit()
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid input" + Style.RESET_ALL)
                self.main()
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"An error occurred: {e}" + Style.RESET_ALL)
            self.main()

    def _login(self):
        while True:
            identifier = input('Enter your email or phone number (or type "exit" to quit) >>> ')
            if identifier.lower() in ['exit', 'quit', 'end', 'break']:
                self.main()
            elif is_valid_email(identifier):
                identifier_type = 'email'
                break
            elif is_valid_phone_number(identifier):
                identifier_type = 'phone-number'
                break
            else:
                print(is_valid_phone_number(identifier))
                print(Fore.RED + Style.BRIGHT + "Invalid email or phone number :(" + Style.RESET_ALL)
                print(Fore.BLUE + "Please re-enter your email or phone number" + Style.RESET_ALL)
                
        pin = getpass.getpass('Enter your pin >>> ')
        log = login(password=pin, **{identifier_type: identifier})
        
        if log['success'] == False:
            print(Fore.RED + Style.BRIGHT +  log['message'] + Style.RESET_ALL)
            show_progress(bar_class=ErrorBar, duration=2)
            self.main()
        else:
            print(Fore.GREEN + Style.BRIGHT + log['message'] + Style.RESET_ALL)
            show_progress(bar_class=SuccessBar)
            
        
    def _signup(self):
        while True:
            fullname = input('Enter your full name >>> ')
            if is_valid_fullname(fullname):
                break
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid full name :(" + Style.RESET_ALL)
                print(Fore.BLUE + "Please re-enter your full name" + Style.RESET_ALL)

        while True:
            email = input('Enter your email >>> ')
            if is_valid_email(email):
                break
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid email :(" + Style.RESET_ALL)
                print(Fore.BLUE + "Please re-enter your email" + Style.RESET_ALL)

        while True:
            phone_number = input('Enter your phone number >>> ')
            if is_valid_phone_number(phone_number):
                break
            else:
                print(Fore.RED + Style.BRIGHT + "Invalid phone number :(" + Style.RESET_ALL)
                print(Fore.BLUE + "Please re-enter your phone number" + Style.RESET_ALL)

        while True:
            dob = input('Enter your date of birth (YYYY-MM-DD) >>> ')
            _dob = is_date_of_birth_valid(dob)
            if _dob['success'] == True:
                break
            else:
                print(Fore.RED + Style.BRIGHT + f"{_dob["message"]}" + Style.RESET_ALL)
                if _dob['type'] == 0:
                    self.home()
                else:
                    print(Fore.BLUE + "Please re-enter your date of birth" + Style.RESET_ALL)

        while True:
            password = getpass.getpass('Create 4 digit pin >>> ')
            confirm_password = getpass.getpass('Re-enter pin >>> ')
            
            if password != confirm_password:
                print(Fore.RED + Style.BRIGHT + "Pin don't match" + Style.RESET_ALL)
            else:
                __signup = signup(name=fullname, email=email, phone_number=phone_number, dob=dob, password=password)
                
                if __signup['success']:
                    print(Fore.GREEN + Style.BRIGHT + "Signup successful!" + Style.RESET_ALL)
                    show_progress(bar_class=SuccessBar)
                    break
                else:
                    print(Fore.RED + Style.BRIGHT + f"{__signup['message']}" + Style.RESET_ALL)
                    show_progress(bar_class=ErrorBar, duration=2)
                    self.main()

















    def admin(self):
        # TO DO: implement admin functionality
        pass

    def about(self):
        # TO DO: implement about functionality
        print("About page")
        
    def quit(self):
        print("Exiting...")
        sys.exit(0)

