import getpass
from fn import is_valid_email, is_valid_phone_number, is_date_of_birth_valid, is_valid_fullname, show_progress, ErrorBar, SuccessBar
from colorama import Fore, Style, Back, init
import questionary
import sys
from auth import login, signup, is_phone_number_in_db
import os
import platform
from schema import get_or_create_user_financial, user, validate_password, Transaction, get_user_unpaid_loans
from decimal import Decimal
from questionary import Style as t
from datetime import datetime, timedelta

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

dim_style = t([
    ('question', 'fg:#424242'),
])

dim_style2 = t([
    ('question', 'fg:#424242'),
    ('answer', 'fg:#171717'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
    ('instruction', 'fg:#212121'),
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
                print(Fore.RED + Style.BRIGHT + "      Invalid email or phone number :(" + Style.RESET_ALL)
                print(Fore.BLUE + "      Please re-enter your email or phone number" + Style.RESET_ALL)
                
        pin = questionary.password('   Enter your pin >>>', qmark='',).ask()
        log = login(password=pin, **{identifier_type: identifier})
        
        if log['success'] == False:
            print(Fore.RED + Style.BRIGHT +  log['message'] + Style.RESET_ALL)
            show_progress(bar_class=ErrorBar, duration=2)
            self.main()
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
        self.user_id = u
        self.refresh_data()

    def refresh_data(self):
        self.user = user(self.user_id)
        self.finance = get_or_create_user_financial(self.user_id)
        self.loans = get_user_unpaid_loans(self.user_id)

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
                'Refresh',
                'Logout',
            ],
            qmark='',
            style=custom_style_fancy
        ).ask()
        
        if action == 'Take Loan':
            self._take_loan()
        elif action == 'Repay Loan':
            self._repay_loan()
        elif action == 'Send Money':
            self._send_money()
        elif action == 'View Balance':
            self._view_balance()
        elif action == 'Request Transaction History':
            pass
        elif action == 'Change Pin':
            pass
        elif action == 'Refresh':
            self.refresh_data()
            print('Refreshed :)')
            show_progress(SuccessBar, duration=1)
            self._user_dashboard()
        
        else:
            self.userAcc = {}
            self.userFin = {}
            Pages().main()

    def _take_loan(self):
        self.refresh_data()
        max_loan_amount = self.finance['loan_capability'] - self.finance['amount_owed']
        
        while True:
            loan_amount = questionary.text(
                f"   How much loan would you like to take (MAX ₦{max_loan_amount}) >>>",
                qmark=""
            ).ask()
            
            try:
                loan_amount = float(loan_amount)
                if loan_amount <= 0:
                    print(Fore.RED + Style.DIM + "      Loan amount must be greater than 0." + Style.RESET_ALL)
                    continue
                
                if loan_amount > max_loan_amount:
                    print(Fore.RED + Style.DIM + f"      Loan request exceeds loan capability. Maximum loan amount: ₦{max_loan_amount}" + Style.RESET_ALL)
                    if max_loan_amount == 0:
                        print(Fore.BLUE + "      Please pay off your debt." + Style.RESET_ALL)
                        questionary.press_any_key_to_continue(style=dim_style).ask()
                        self._user_dashboard()
                        
                    print(Fore.BLUE + "      Please re-enter the loan amount you would like to take." + Style.RESET_ALL)
                    continue
                break
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "    Amount should be a valid number. Please try again." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + Style.BRIGHT + f"    Unexpected error: {e}" + Style.RESET_ALL)

        while True:
            repayment_date = questionary.text(
                "   Enter the repayment date (YYYY-MM-DD) >>>",
                qmark=""
            ).ask()
            
            try:
                repayment_date_obj = datetime.strptime(repayment_date, "%Y-%m-%d")
                if repayment_date_obj <= datetime.now():
                    print(Fore.RED + Style.DIM + "    Repayment date must be in the future. Please try again." + Style.RESET_ALL)
                    continue

                current_date = datetime.now()
                days_difference = (repayment_date_obj - current_date).days
                interest_rate = 0.04
                daily_interest_rate = interest_rate / 365
                total_interest = loan_amount * daily_interest_rate * days_difference
                amount_due = loan_amount + total_interest
                
                max_repayment_date = current_date + timedelta(days=2 * 365)
                
                if repayment_date_obj > max_repayment_date:
                    print(Fore.RED + Style.DIM + f"    The repayment date cannot exceed 2 years from today ({max_repayment_date.strftime('%B %d, %Y')}). Please choose an earlier date." + Style.RESET_ALL)
                    continue
                    
                
                while True:
                    choice = questionary.select(
                        f"      Repayment Date: {repayment_date_obj.strftime('%B %d, %Y')}\n"
                        f"       Loan Amount: ₦{loan_amount}\n"
                        f"       Total Interest: ₦{total_interest:.2f}\n"
                        f"       Amount Due: ₦{amount_due:.2f}\n\n"
                        "     Would you like to proceed?",
                        choices=["     Continue", "     Change Date", "     Quit"],
                        qmark='',
                        style=dim_style2
                    ).ask()
                    
                    if choice == "     Continue":
                        print(Fore.CYAN +  Style.DIM + f"     Proceeding with repayment of ₦{amount_due:.2f} on {repayment_date_obj.strftime('%Y-%m-%d')}." + Style.RESET_ALL)
                        break

                    elif choice == "     Change Date":
                        print(Fore.CYAN  + Style.DIM + f"     Please select a new repayment date."  + Style.RESET_ALL)
                        break

                    elif choice == "     Quit":
                        self._user_dashboard()
                        break
                    
                if choice == "     Continue" or choice == "     Quit":
                    break

            except ValueError:
                print(Fore.RED + Style.DIM + "    Invalid date format. Please enter the date in YYYY-MM-DD format." + Style.RESET_ALL)

        # Ask for pin to complete transaction
        pin = questionary.password("   Enter your pin to complete transaction >>>", qmark="").ask()
        pent = validate_password(user_id=self.user['user_id'], password=pin)
        
        if pent['success']:
            transaction = Transaction(user_id=self.user['user_id'], financial_id=self.finance['financial_id']).take_loan(
                loan_amount=loan_amount,
                repayment_date=repayment_date
            )
            
            if transaction['success']:
                print(Fore.GREEN + Style.BRIGHT + transaction['message'] + Style.RESET_ALL)
                show_progress(SuccessBar, duration=2)
                questionary.press_any_key_to_continue(style=dim_style).ask()
                self._user_dashboard()
            else:
                print(Fore.RED + Style.BRIGHT + transaction['message'] + Style.RESET_ALL)
                show_progress(ErrorBar, duration=1)
                questionary.press_any_key_to_continue(style=dim_style).ask()
                self._user_dashboard()
                
                
        else:
            print(Fore.BLUE + "You entered a wrong pin :(" + Style.RESET_ALL)
            show_progress(ErrorBar, duration=0.5)
            questionary.press_any_key_to_continue(style=dim_style).ask()    
            self._user_dashboard()

    def _repay_loan(self):
        self.refresh_data()
        if not len(self.loans) >= 1:
            print(Fore.GREEN + Style.DIM + '      You did not have any pending loan.' + Style.RESET_ALL)
            questionary.press_any_key_to_continue(style=dim_style).ask()
            self._user_dashboard()
            
        while True:
            amount_to_pay = questionary.text('    How much do you want to pay >>>', qmark='').ask()
            
            try:
                amount_to_pay = Decimal(amount_to_pay)
                if amount_to_pay > self.finance['balance']:
                    print(Fore.RED + Style.DIM + f"      You don't have enough balance to pay ₦{amount_to_pay:,.2f}. (Acct Balance: ₦{self.finance['balance']:,.2f})" + Style.RESET_ALL)
                    print(Fore.BLUE + "      Please re-enter how much you would like to pay." + Style.RESET_ALL)
                else:
                    break
            except Exception as e:
                print(Fore.RED + Style.BRIGHT + '      ' + str(e) + Style.RESET_ALL)
            
        try:
            formatted_loans = {}
            for loan in self.loans:
                
                if loan[7] > 0:
                    repayment_details = f" Already paid ₦{loan[7]:,.2f}, remains ₦{loan[6] - loan[7]}"
                else:
                    repayment_details = ""
                    
                formatted_string = (
                    f"    ₦{loan[1]:,.2f} loaned {loan[5].strftime('%B %d %Y')} "
                    f"for {loan[4]} months with interest of {loan[3]:.2f}."
                    f"{repayment_details}"
                )
                formatted_loans[formatted_string] = loan[0]

            
            selected_loan = questionary.select(
                "    Select the loan you want to repay -",
                choices=list(formatted_loans.keys()),
                qmark='',
                style=dim_style2
            ).ask()

            selected_loan_id = formatted_loans[selected_loan]
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"    Unexpected error: {e}" + Style.RESET_ALL)
            return
        
        pin = questionary.password('    Enter your pin to complete transaction >>>', qmark='').ask()
        pent = validate_password(user_id=self.user['user_id'], password=pin)
            
        if pent['success'] == True:
            transaction = Transaction(user_id=self.user['user_id'], financial_id=self.finance['financial_id']).repay_loan(repayment_amount=amount_to_pay, loan_id=selected_loan_id)
            if transaction['success'] == True:
                print(Fore.GREEN + Style.BRIGHT + transaction['message'] + Style.RESET_ALL)
                show_progress(SuccessBar, duration=2)
                questionary.press_any_key_to_continue(style=dim_style).ask()
                self._user_dashboard()
            else:
                print(Fore.RED + Style.BRIGHT + transaction['message'] + Style.RESET_ALL)
                show_progress(ErrorBar, duration=1)
                questionary.press_any_key_to_continue(style=dim_style).ask()
                self._user_dashboard()
        else:
            print(Fore.BLUE + "You entered a wrong pin :(" + Style.RESET_ALL)
            show_progress(ErrorBar, duration=1)
            questionary.press_any_key_to_continue(style=dim_style).ask()
            self._user_dashboard()

    def _send_money(self):
        self.refresh_data()
        breakwords = ['exit', 'bye', 'quit', 'end', 'no']
        
        try:
            while True:
                amount = questionary.text(
                '    How much will you like to transfer?  // (or type "exit" to quit) >>>',
                qmark=""
                ).ask()
                amount = Decimal(amount)
                if amount > self.finance['balance']:
                    print(Fore.RED + Style.DIM + f"      You don't have up to ₦{amount:,.2f}. (Acct Balance: ₦{self.finance['balance']:,.2f})" + Style.RESET_ALL)
                    print(Fore.BLUE + "      Please re-enter how much you would like to transfer." + Style.RESET_ALL)
                else:
                    break
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + '      ' + str(e) + Style.RESET_ALL)
        
        try:
            while True:
                recipient_account_number = questionary.text(
                    '    Enter the recipient\'s account number(phone number) // (or type "exit" to quit) >>>',
                    qmark=""
                ).ask()
                
                prob_u = is_phone_number_in_db(recipient_account_number)    
                if recipient_account_number in breakwords:
                    self._user_dashboard()
                    break
                
                elif not is_valid_phone_number(recipient_account_number):
                    print(Fore.RED + Style.DIM + '      The account number(phone number) is not correct' + Style.RESET_ALL)
                    print(Fore.BLUE + Style.DIM + '      Please re-enter recipient\'s account number(phone number)' + Style.RESET_ALL)
                    
                elif recipient_account_number == self.user['phone_number']:
                    print(Fore.RED + Style.DIM + '      You cannot make a transfer to your self' + Style.RESET_ALL)
                    print(Fore.BLUE + Style.DIM + '      Please re-enter recipient\'s account number(phone number)' + Style.RESET_ALL)
                
                elif prob_u['success'] == False:
                    print(Fore.RED + Style.DIM + '      There is no user with this account number :(' + Style.RESET_ALL)
                    print(Fore.BLUE + Style.DIM + '      Please re-enter recipient\'s account number(phone number)' + Style.RESET_ALL)

                else:
                    break          
        except Exception as e:
            print(Fore.RED + Style.DIM + '      We encountered an error processing account number : %s', e + Style.RESET_ALL)
        
        
        print("\n   Transfer " + Fore.LIGHTBLACK_EX + f'₦{amount}' + Style.RESET_ALL + ' to \n' + Fore.LIGHTBLACK_EX + f'   {user(id=prob_u['user'])['name'].upper()}' + Style.RESET_ALL )
        
        pin = questionary.password("  Enter your pin to complete transaction // (or type \"exit\" to quit)>>>", qmark="").ask()
        
        if pin in breakwords:
            self._user_dashboard()
        
        pent = validate_password(self.user['user_id'], pin)
        if pent['success']:
            response = Transaction(user_id=self.user_id, financial_id=self.finance).send_money(amount=5000, receiver_id=prob_u['user'])
        else:
            print(Fore.BLUE + "You entered a wrong pin :(" + Style.RESET_ALL)
            show_progress(ErrorBar, duration=0.5)
            questionary.press_any_key_to_continue(style=dim_style).ask()    
            self._user_dashboard()
        
    def _view_balance(self):
        self.refresh_data()
        breakwords = ['exit', 'bye', 'quit', 'end', 'no']
        pin = questionary.password("  Enter your pin to complete transaction // (or type \"exit\" to quit)>>>", qmark="").ask()
        if pin in breakwords:
            self._user_dashboard()
        
        pent = validate_password(self.user['user_id'], pin)
        if pent['success']:
            transaction = Transaction(user_id=self.user['user_id'], financial_id=self.finance['financial_id']).fetch_user_balance()
            if transaction['success']:
                print(Fore.WHITE + Style.BRIGHT + f'\n   Account balance: ₦{transaction['balance']}\n   Amount Owed: ₦{transaction['total_outstanding_with_interest']}' + Style.RESET_ALL)
                questionary.press_any_key_to_continue(style=dim_style).ask()
                self._user_dashboard()
            else:
                print(Fore.RED + Style.DIM + '    ' + transaction['message'] + Style.RESET_ALL)
                questionary.press_any_key_to_continue(style=dim_style).ask()
                self._user_dashboard()
        else:
            print(Fore.BLUE + "You entered a wrong pin :(" + Style.RESET_ALL)
            show_progress(ErrorBar, duration=0.5)
            questionary.press_any_key_to_continue(style=dim_style).ask()    
            self._user_dashboard()
        
            