import getpass
from fn import is_valid_email, is_valid_phone_number, is_date_of_birth_valid, is_valid_fullname, show_progress, ErrorBar, SuccessBar
from colorama import Fore, Style, Back, init
import questionary
import sys
from auth import login, signup
import os
import platform
from db import get_or_create_user_financial, user, validate_password, Transaction
import time
from questionary import Style as t

custom_style_fancy = t([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#f44336 bold'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
    ('selected', 'fg:#cc5454'),
    ('separator', 'fg:#cc5454'),
    ('instruction', ''),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])



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
            style=custom_style_fancy,
            qmark=''
        ).ask()
        self.next(action)

    def next(self, request):
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
            identifier = input('    Enter your email or phone number (or type "exit" to quit) >>> ')
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
                
        pin = questionary.password('   Enter your pin >>>', qmark='',).ask()
        log = login(password=pin, **{identifier_type: identifier})
        
        if log['success'] == False:
            print(Fore.RED + Style.BRIGHT +  log['message'] + Style.RESET_ALL)
            show_progress(bar_class=ErrorBar, duration=2)
        else:
            print(Fore.GREEN + Style.BRIGHT + log['message'] + Style.RESET_ALL)
            show_progress(bar_class=SuccessBar)
            Dashboard(u=log['user'])._user_dashboard()
            
        
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
        pass

    def about(self):
        print("About page")
        
    def quit(self):
        sys.exit(0)
        
        
        
        
class Dashboard():
    def __init__(self, u):
        self.user = user(u)
        self.finance = get_or_create_user_financial(u)
    
    def _user_dashboard(self):
        clear_screen()
        
        action = questionary.select(
            message=f"Welcome {self.user['name']}. what will you like to do?",
            choices=[
                'Take Loan',
                'Repay Loan',
                'Send Money',
                'View Balance',
                'Request Transction Gistory',
                'Change Pin',
                'Logout',
            ],
            qmark='',
            style=custom_style_fancy
        ).ask()
        
        if action == 'Take Loan':
            self._take_loan()
        elif action == 'Repay loan':
            pass
        elif action == 'Send Money':
            pass
        elif action == 'View Balance':
            pass
        elif action == 'Request Transaction History':
            pass
        elif action == 'Change Pin':
            pass
        else:
            self.userAcc = {}
            self.userFin = {}
            Pages().main()
            

        
    def _take_loan(self):
        loan_amount = questionary.text(f'   How much loan will you like to take (MAX ₦{self.finance['loan_capability']}) >>>', qmark="").ask()
        try:
            loan_amount = float(loan_amount)
        except TypeError:
            print(Fore.RED + Style.BRIGHT + 'Amount should be a number' + Style.RESET_ALL)
        except  Exception as e:
            print(Fore.RED + Style.BRIGHT + e + Style.RESET_ALL)
            
        
        while True:
            if loan_amount > self.finance['loan_capability']:
                print(Fore.RED + Style.DIM + f"Loan request exceeds loan capability. Maximum loan amount: ₦{self.finance['loan_capability']}" + Style.RESET_ALL)
                print(Fore.BLUE + "Please re-enter your email or phone number" + Style.RESET_ALL)
            else:
                break
        
        pin = questionary.password('   Enter your pin to complete transaction >>>', qmark='').ask()
        pent = validate_password(user_id=self.user['user_id'], password=pin)
        if pent['success'] == True:
            transaction = Transaction(user_id=self.user['user_id'], financial_id=self.finance['financial_id']).take_loan(loan_amount=loan_amount)
            if transaction['success'] == True:
                show_progress(SuccessBar, duration=2)
                print(Fore.GREEN + Style.BRIGHT + transaction['message'] + Style.RESET_ALL)
                time.sleep(2)
                self._user_dashboard()
            else:
                print(Fore.RED + Style.BRIGHT + transaction['message'] + Style.RESET_ALL)
                show_progress(ErrorBar, duration=1)
                self._user_dashboard
        else:
            print(Fore.BLUE + "You entered a wrong pin :(" + Style.RESET_ALL)
            show_progress(ErrorBar, duration=0.5)
            self._user_dashboard()

        # Update user financials
        

    def _repay_loan(self):
        amount_to_pay = questionary.text(f'   How much will you like to pay (Acct Balance ₦{self.finance['balance']}) >>>', qmark="").ask()
