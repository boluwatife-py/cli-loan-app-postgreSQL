def abt():
    about = """
═══════════════════════════════════════════════════════
                   🏦 LOAN SYSTEM APP 📊
═══════════════════════════════════════════════════════

Welcome to the `Loan System App`! This financial platform is designed to facilitate 
seamless `loan transactions`, `user account management`, and `secure fund transfers`. 
With an intuitive interface and robust backend, the system ensures smooth 
operations for both users and administrators.

🔹 **KEY FEATURES:**
-----------------------------------
✅ `User Registration & Financial Account Creation`  
✅ `Loan Application & Repayment`  
✅ `Secure Money Transfers Between Users`  
✅ `Transaction History & Search Functionality`  
✅ `Admin Controls for Managing Users & System Data`  
✅ `Loan System Financial Overview`  

═══════════════════════════════════════════════════════
                 📌 USER FUNCTIONS
═══════════════════════════════════════════════════════

🔹 **1. User Financial Account Management**  
   - Every user has a financial account in **`UserFinancials`**.  
   - If a user does not have one, it is **automatically created** upon the first transaction.  
   - Stores **`balance, loan capability, amount owed`**, and more.  

   📌 **Function:**
   ```python
   get_or_create_user_financial(user_id)
🔹 2. Sending Money to Other Users

Users can transfer funds securely.
Ensures sufficient balance before processing transactions.
Records transactions in Transactions and transfer_history.
📌 Function:

python
Copy
Edit
send_money(self, amount, receiver_id)
🔹 3. Transaction History

Retrieves all debits, credits, and transfers for a user.
Formats transactions neatly for better readability.
Allows filtering by sender, receiver, or loan-related transactions.
📌 Function:

python
Copy
Edit
get_transaction_history(self)
🔹 4. Searching for Users

Admins can search users by name, email, or phone number.
Results are displayed in a paginated format with a selectable menu.
📌 Function:

python
Copy
Edit
search_user_interactive(self)
═══════════════════════════════════════════════════════ 🔹 ADMIN FUNCTIONS ═══════════════════════════════════════════════════════

🔹 5. Fetching Users (Paginated)

Admins can navigate users 10 at a time.
Select users from a formatted list.
📌 Function:

python
Copy
Edit
select_user_paginated(self, page_size=10)
🔹 6. Selecting a User & Performing Admin Actions

Once a user is selected, an admin can:
✅ Delete User
✅ Make User an Admin
📌 Function:

python
Copy
Edit
_select_users(self)
🔹 7. Loan System Financial Overview

Displays the total system balance and total loans given.
Helps admins track financial performance.
📌 Function:

python
Copy
Edit
show_loan_system_balance(self)
═══════════════════════════════════════════════════════ 🎯 FINAL THOUGHTS ═══════════════════════════════════════════════════════

The Loan System App is a powerful financial platform that ensures smooth transactions, secure fund management, and efficient loan processing.

With its admin controls, automated account creation, and seamless search & selection features, it provides a robust and scalable solution for modern financial operations.

🚀 Built for efficiency, security, and seamless user experience! ═══════════════════════════════════════════════════════ """
    return about