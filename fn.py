from datetime import datetime
from dateutil import parser
from datetime import date
import re
from progress.bar import Bar
import time
from colorama import Fore, Style
from fpdf import FPDF
import os


# REGULAR EXPRESSION TO VERIFY EMAIL
def is_valid_email(email):
    """Basic email format validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


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
        
        if age >= 18 and age <= 90:
            return {'success': True, 'message': 'Age successfully verified'} 
        else:
            return {'success': False, 'message': 'User is less than 18 or greater than 90 years old', 'type': 0}
    
    except (ValueError, TypeError):
        return {'success': False, 'message': f'{dob_input} is an invalid date format/input', 'type': 1}
    
    
def is_valid_phone_number(phone_number_input):
    """
    VALIDATES THE PHONE NUMBER IF IT IS IN THE RIGHT FORMAT.
    
    THIS FUNCTION VERIFIES IT FOR NIGERIAN PHONE NUMBER.
    """
        
    #NESTED IF CHECK IF NUMBER IS IN THIS FORMAT "080********"
    if phone_number_input.startswith('0'):
        if len(phone_number_input) == 11:
            if phone_number_input[1] in ['8', '7', '9']:
                if phone_number_input[2] in ['0', '1']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
        
    #CHECKS IF NUMBER IS IN THIS FORMAT "+23480********"
    elif phone_number_input.startswith('+234'):
        if len(phone_number_input) == 14:
            if phone_number_input[4] in ['8', '7', '9']:
                if phone_number_input[5] in ['0', '1']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        False
                
  
def is_valid_fullname(fullname):
    pattern = r"^[a-zA-Z-' ]{2,}$"
    return bool(re.match(pattern, fullname))


# Success Progress Bar (Green)
class SuccessBar(Bar):
    message = Fore.GREEN + "Success" + Style.RESET_ALL
    fill = Fore.GREEN + "█" + Style.RESET_ALL
    bar_prefix = Fore.GREEN + "" + Style.RESET_ALL
    bar_suffix = Fore.GREEN + "" + Style.RESET_ALL
    suffix = ''

# Error Progress Bar (Red)
class ErrorBar(Bar):
    message = Fore.RED + "Error" + Style.RESET_ALL
    fill = Fore.RED + "█" + Style.RESET_ALL
    bar_prefix = Fore.RED + "" + Style.RESET_ALL
    bar_suffix = Fore.RED + "" + Style.RESET_ALL
    suffix = ''


def show_progress(bar_class, duration=3):
    """Show a progress bar using the given bar class, completing in 3 seconds."""
    steps = 100
    interval = duration / steps
    with bar_class(max=steps) as bar:
        for _ in range(steps):
            time.sleep(interval)
            bar.next()
            
def generate_transaction_history_pdf(transaction_data, file_path, user_name):
    try:
        # Check if transaction data was successfully retrieved
        if not transaction_data["success"]:
            print(f" Error: {transaction_data['message']}")
            return

        transactions = transaction_data["data"]
        if not transactions:
            print(" No transactions to generate a PDF for.")
            return

        
        if not os.path.exists(file_path):
            print(f" The directory '{file_path}' does not exist.")
            return

        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt=f"{user_name} Transaction History".title(), ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", style="B", size=8)
        pdf.cell(40, 10, txt="Type", border=1, align="C")
        pdf.cell(40, 10, txt="Amount", border=1, align="C")
        pdf.cell(50, 10, txt="Date", border=1, align="C")
        pdf.cell(30, 10, txt="Sender", border=1, align="C")
        pdf.cell(30, 10, txt="Receiver", border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", size=6)
        for transaction in transactions:
            pdf.cell(40, 10, txt=transaction["type"], border=1, align="C")
            pdf.cell(40, 10, txt=transaction['amount'], border=1, align="C")
            pdf.cell(50, 10, txt=transaction["date"], border=1, align="C")
            pdf.cell(30, 10, txt=transaction["sender"], border=1, align="C")
            pdf.cell(30, 10, txt=transaction["receiver"], border=1, align="C")
            pdf.ln()

        # Save PDF
        file_name = f"{user_name}_transaction_history.pdf"
        path = os.path.join(file_path, file_name)
        pdf.output(path)
        print(Fore.GREEN + Style.BRIGHT + f" Transaction history saved successfully to {path}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + Style.DIM + f" An error occurred while generating the PDF: {e}" + Style.RESET_ALL)