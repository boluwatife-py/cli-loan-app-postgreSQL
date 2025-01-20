import action_processor
from colorama import Fore, Style, Back
import questionary




def main():
    action = questionary.select(
        "What would you like to do?",
        choices=[
            "Login",
            "Create a new account",
            "Admin",
            "View About",
        ],
    ).ask()

    action_processor.home(action)
    
main()


