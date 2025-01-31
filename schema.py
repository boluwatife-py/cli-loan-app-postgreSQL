import psycopg2
import bcrypt
from datetime import datetime
from math import ceil
from decimal import Decimal
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(database = "LAir", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "Ilerioluwa1@",
                        port = 5432)

cur = conn.cursor()



# """
# INITIALIZING DATABASE -- CREATING TABLES
# """


# ## USER TABLE
# user_db = """CREATE TABLE Users (
#     user_id SERIAL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     phone_number VARCHAR(15) UNIQUE NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     dob DATE NOT NULL,
# );
# """
# cur.execute(user_db)


# ## LOAN TABLES
# loan_db = """CREATE TABLE Loans (
#     loan_id SERIAL PRIMARY KEY,
#     user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
#     loan_amount DECIMAL(15, 2) NOT NULL,
#     interest_rate DECIMAL(5, 2) NOT NULL, -- e.g., 5.00 for 5%
#     tenure_months INT NOT NULL, -- loan repayment period in months
#     status VARCHAR(50) DEFAULT 'Pending', -- Pending, Approved, Rejected, Repaid
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """
# cur.execute(loan_db)


# ## REPAYMENT TABLE
# repayment_db = """CREATE TABLE Repayments (
#     repayment_id SERIAL PRIMARY KEY,
#     loan_id INT REFERENCES Loans(loan_id) ON DELETE CASCADE,
#     due_date DATE NOT NULL,
#     amount_due DECIMAL(15, 2) NOT NULL,
#     amount_paid DECIMAL(15, 2) DEFAULT 0.00,
#     status VARCHAR(50) DEFAULT 'Pending', -- Pending, Paid
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """
# cur.execute(repayment_db)


# ## TRANSACTIONS TABLE
# transactions_db = """CREATE TABLE Transactions (
#     transaction_id SERIAL PRIMARY KEY,
#     user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
#     loan_id INT REFERENCES Loans(loan_id),
#     transaction_type VARCHAR(50) NOT NULL, -- Credit or Debit
#     amount DECIMAL(15, 2) NOT NULL,
#     transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """
# cur.execute(transactions_db)


# ## ADMIN TABLE
# admin_db = """CREATE TABLE Admins (
#     admin_id SERIAL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """
# cur.execute(admin_db)

# userFin = """CREATE TABLE UserFinancials (
#     financial_id SERIAL PRIMARY KEY,                  
#     user_id INT NOT NULL,                             
#     balance DECIMAL(15, 2) DEFAULT 0.00,              
#     amount_owed DECIMAL(15, 2) DEFAULT 0.00,          
#     loan_capability DECIMAL(15, 2) NOT NULL,          
#     total_loans_taken DECIMAL(15, 2) DEFAULT 0.00,    
#     last_loan_date DATE,                              
#     account_status VARCHAR(20) DEFAULT 'active',      
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
#     CONSTRAINT fk_user_financial FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
# );"""

# cur.execute(userFin)


# his = """CREATE TABLE transfer_history(
#     if SERIAL PRIMARY KEY,
#     user_id INT NOT NULL,
#     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     sender VARCHAR(255) NOT NULL,
#     receiver VARCHAR(255) NOT NULL,
#     amount DECIMAL(15, 2) NOT NULL,
#     CONSTRAINT fk_user_transaction FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE)
#     """
    
# cur.execute(his)

# ls = """
#         CREATE TABLE IF NOT EXISTS LoanSystem (
#             id SERIAL PRIMARY KEY,
#             available_funds DECIMAL(15, 2) NOT NULL,   
#             total_loans_given DECIMAL(15, 2) DEFAULT 0,
#             total_earnings DECIMAL(15, 2) DEFAULT 0,   
#             last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#         """

# ## COMMITTING THE DATA
# conn.commit()



def is_email_in_db(email):
    try:
        cur.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
        result = cur.fetchone()
        if result != None:
            return {'success':True, 'user':result[0], 'message':'Email found'}
        else:
            return {'success':False, 'user':None, 'message':'Email not found'}

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def validate_admin_password(admin, password):
    if not password or not admin:
        return {'success': False, 'user':None, 'message':'Some fields are empty.'}
        
    try:
        cur.execute(f"SELECT password FROM Admins WHERE admin_id='{admin}'")
        result = cur.fetchone()[0]
        
        if result:
            stored_password_hash = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return {'success':True, 'user':admin, 'message':'Password veriied successfully'}
            else:
                return {'success':False, 'user':None, 'message':'Wrong password.'}
        else:
            return {'success': False, 'user':None, 'message':'User not found.'}
    except psycopg2.Error as e:
        return {'success': False, 'user':None, 'message':f'Database error.{e}'}
    except Exception as e:
        return {'success': False, 'user':None, 'message': f'Unknon Error.{e}'}
        
def is_email_in_admin(email):
    try:
        cur.execute("SELECT admin_id FROM Admins WHERE email = %s", (email,))
        result = cur.fetchone()
        
        if result != None:
            return {'success':True, 'user':result[0], 'message':'Email found'}
        else:
            return {'success':False, 'user':None, 'message':'Email not found'}

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def is_phone_number_in_db(phone_number):
    try:
        cur.execute("SELECT user_id FROM Users WHERE phone_number = %s", (phone_number,))
        result = cur.fetchone()
        if result:
            return {'success':True, 'user':result[0], 'message':'Phone-number found'}
        else:
            return {'success':False, 'user':None, 'message':'Phone-number not found'}

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def query_user(**kwargs):
    try:
        if 'email' in kwargs:
            cur.execute("SELECT user_id FROM Users WHERE email = %s", (kwargs['email'],))
        elif 'phone_number' in kwargs:
            cur.execute("SELECT user_id FROM Users WHERE phone_number = %s", (kwargs['phone_number'],))
        else:
            raise ValueError("You must provide either 'email' or 'phone_number' to query the user.")

        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

    except ValueError as e:
        print(f"Value error: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def user(id):
    try:
        cur.execute("SELECT * FROM Users WHERE user_id = %s", (id,))
        dat = cur.fetchone()
        return {
            "user_id": dat[0],
            "name": dat[1],
            "email": dat[2],
            "password": dat[3],
            "dob": dat[6],
            "phone_number": dat[4]
        }
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def validate_password(user_id, password):
    if not password or not user_id:
        return {'success': False, 'user':None, 'message':'Some fields are empty.'}
        
    try:
        cur.execute(f"SELECT password FROM Users WHERE user_id='{user_id}'")
        result = cur.fetchone()[0]
        
        if result:
            stored_password_hash = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return {'success':True, 'user':user_id, 'message':'Password veriied successfully'}
            else:
                return {'success':False, 'user':None, 'message':'Wrong password.'}
        else:
            return {'success': False, 'user':None, 'message':'User not found.'}
    except psycopg2.Error as e:
        return {'success': False, 'user':None, 'message':f'Database error.{e}'}
    except Exception as e:
        return {'success': False, 'user':None, 'message': f'Unknon Error.{e}'}
    
def create_user(name, email, phone_number, password, dob):
    insert_query = """
        INSERT INTO Users (name, email, password, dob, phone_number)
        VALUES (%s, %s, %s, %s, %s) RETURNING user_id;
    """
    
    cur.execute(insert_query, (name, email, password, dob, phone_number))
    user_id = cur.fetchone()[0]
    conn.commit()
    
    return {'success': True, 'user': user_id, 'message': 'Account created successfully'}

def get_or_create_user_financial(user_id):
    """
    Get or create a financial account for a user.
    
    Args:
        conn: The psycopg2 connection object.
        user_id: The ID of the user.

    Returns:
        dict: The user's financial account details.
    """
    try:
        cur.execute("""
            SELECT * FROM UserFinancials WHERE user_id = %s;
        """, (user_id,))
        financial_account = cur.fetchone()

        # If it exists, return it
        if financial_account:
            return {
                "financial_id": financial_account[0],
                "user_id": financial_account[1],
                "balance": financial_account[2],
                "amount_owed": financial_account[3],
                "loan_capability": financial_account[4],
                "total_loans_taken": financial_account[5],
                "last_loan_date": financial_account[6],
                "account_status": financial_account[7],
                "created_at": financial_account[8],
                "updated_at": financial_account[9]
            }

        cur.execute("""
            INSERT INTO UserFinancials (
                user_id, balance, amount_owed, loan_capability, 
                total_loans_taken, account_status, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (
            user_id, 0.00, 0.00, 500000.00, 0.00, 'active', datetime.now(), datetime.now()
        ))
        
        financial_account = cur.fetchone()

        
        conn.commit()
        
        return {
            "financial_id": financial_account[0],
            "user_id": financial_account[1],
            "balance": financial_account[2],
            "amount_owed": financial_account[3],
            "loan_capability": financial_account[4],
            "total_loans_taken": financial_account[5],
            "last_loan_date": financial_account[6],
            "account_status": financial_account[7],
            "created_at": financial_account[8],
            "updated_at": financial_account[9]
        }

    except Exception as e:
        conn.rollback()
        raise e

def get_user_unpaid_loans(user_id):
    try:
        cur.execute(
            """
            SELECT 
                Loans.loan_id, Loans.loan_amount, Loans.interest_rate, Loans.tenure_months, 
                Loans.status, Loans.created_at, Repayments.amount_due, Repayments.amount_paid 
            FROM Loans
            JOIN Repayments ON Loans.loan_id = Repayments.loan_id
            WHERE Loans.user_id = %s AND Repayments.status = 'Pending'
            ORDER BY Loans.created_at DESC
            """,
            (user_id,)
        )
        loans = cur.fetchall()
        return loans

    except psycopg2.Error as e:
        return f'Database error: {e}'

    except Exception as e:
        return f"An unexpected error occurred: {e}"
    
def update_user_pin(user_id, pin):
    try:
        cur.execute("""
                    UPDATE Users
                    SET password = %s WHERE user_id = %s;
                    """, (pin, user_id))
        cur.execute("COMMIT;")
        
        return {"success": True, 'message':'pin updated successfully'}
    except Exception as e:
        return {'success': False, 'message':e}

class Transaction():
    def __init__(self, user_id, financial_id):
        self.user_id = user_id
        self.financial_id = financial_id
        
    def fund_system(self, fund_amount):
        try:
            if fund_amount <= 0:
                raise ValueError("Fund amount must be greater than 0.")
            
            cur.execute("BEGIN;")
            cur.execute("""
                UPDATE LoanSystem 
                SET available_funds = available_funds + %s, 
                    last_updated = CURRENT_TIMESTAMP;
            """, (fund_amount,))
            cur.execute("COMMIT;")
            return {'success': True, 'message': 'Funds successfully added to the system.'}
        
        except Exception as e:
            cur.execute("ROLLBACK;")
            return {'success': False, 'message': f'Error funding system: {e}'}
    
    def take_loan(self, loan_amount, repayment_date):
        try:
            if loan_amount <= 0:
                raise ValueError("Loan amount must be greater than 0.")
            
            cur.execute("BEGIN;")
            # Calculate repayment details
            repayment_date_obj = datetime.strptime(repayment_date, "%Y-%m-%d")
            current_date = datetime.now()
            days_difference = (repayment_date_obj - current_date).days
            interest_rate = 0.04
            daily_interest_rate = interest_rate / 365
            total_interest = loan_amount * daily_interest_rate * days_difference
            amount_due = loan_amount + total_interest
            tenure_months = ceil((repayment_date_obj.year - current_date.year) * 12 + (repayment_date_obj.month - current_date.month))
            
            if repayment_date_obj.day < current_date.day:
                tenure_months -= 1
                
            if tenure_months > 24:
                raise ValueError("The repayment date must be within 2 years from today. Please choose an earlier date.")
            
            
            cur.execute("""
                UPDATE UserFinancials
                SET balance = balance + %s, 
                    amount_owed = amount_owed + %s,
                    total_loans_taken = total_loans_taken + 1,
                    last_loan_date = CURRENT_DATE
                WHERE user_id = %s AND loan_capability >= %s AND amount_owed < loan_capability;
            """, (loan_amount, loan_amount, self.user_id, loan_amount))
            
            if cur.rowcount == 0:
                raise Exception("Loan eligibility criteria not met.")
            
            # Deduct from loan system funds
            cur.execute("""
                UPDATE LoanSystem
                SET available_funds = available_funds - %s,
                    total_loans_given = total_loans_given + %s,
                    last_updated = CURRENT_TIMESTAMP
                WHERE available_funds >= %s;
            """, (loan_amount, loan_amount, loan_amount))
            
            if cur.rowcount == 0:
                raise Exception("Insufficient funds in the loan system.")
            
            # Insert into Loans table
            cur.execute("""
                INSERT INTO Loans (
                    user_id, loan_amount, interest_rate, tenure_months, 
                    status, created_at
                )
                VALUES (%s, %s, 0.04, %s, 'Approved', CURRENT_TIMESTAMP)
                RETURNING loan_id;
            """, (self.user_id, loan_amount, tenure_months))
            loan_id = cur.fetchone()[0]
            
            
            # Insert into Repayments table
            cur.execute("""
                INSERT INTO Repayments (
                    loan_id, due_date, amount_due
                )
                VALUES (%s, %s, %s);
            """, (loan_id, repayment_date, amount_due))
            
            # Insert transaction record
            cur.execute("""
                INSERT INTO Transactions (
                    user_id, loan_id, transaction_type, amount, transaction_date
                )
                VALUES (%s, %s, 'Credit', %s, CURRENT_DATE);
            """, (self.user_id, loan_id, loan_amount))
            
            cur.execute("COMMIT;")
            return {'success': True, 'message': f"Loan successfully approved. Due on {repayment_date}: ₦{amount_due:.2f}"}
        
        except Exception as e:
            cur.execute("ROLLBACK;")
            return {'success': False, 'message': f"Error while processing loan: {e}"}

    def repay_loan(self, loan_id, repayment_amount):
        try:
            account = get_or_create_user_financial(self.user_id)
            if repayment_amount <= 0:
                raise ValueError("Repayment amount must be greater than 0.")
            
            repayment_amount = Decimal(repayment_amount)
            
            cur.execute("BEGIN;")
            
            cur.execute("""
                SELECT loan_amount, amount_due, amount_paid, due_date, Loans.status
                FROM Loans
                JOIN Repayments ON Loans.loan_id = Repayments.loan_id
                WHERE Loans.loan_id = %s;
            """, (loan_id,))
            loan_info = cur.fetchone()

            if not loan_info:
                raise Exception("Loan not found.")

            loan_amount, amount_due, amount_paid, due_date, loan_status = loan_info

            loan_amount = Decimal(loan_amount)
            amount_due = Decimal(amount_due)
            amount_paid = Decimal(amount_paid)

            
            if loan_status == 'Repaid':
                raise Exception("This loan has already been fully repaid.")

            
            if repayment_amount + amount_paid > amount_due:
                excess_payment = repayment_amount + amount_paid - amount_due
                repayment_amount = amount_due
                message = f"Repayment amount exceeds the amount due. ₦{excess_payment:,.2f} remains in your account."
            else:
                message = f"Repayment of ₦{repayment_amount:,.2f} successfully processed."

            
            new_amount_paid = amount_paid + repayment_amount
            new_status = 'Repaid' if new_amount_paid >= amount_due else 'Pending'

            cur.execute("""
                UPDATE Repayments
                SET amount_paid = %s, status = %s
                WHERE loan_id = %s;
            """, (new_amount_paid, new_status, loan_id))
            
            if cur.rowcount == 0:
                raise Exception("Failed to update repayment record.")

            
            cur.execute("""
                UPDATE UserFinancials
                SET amount_owed = amount_owed - %s, balance = balance - %s
                WHERE user_id = %s;
            """, (repayment_amount, repayment_amount, self.user_id))
            
            if cur.rowcount == 0:
                raise Exception("Failed to update user financials.")

            
            cur.execute("""
                UPDATE LoanSystem
                SET available_funds = available_funds + %s
                WHERE id = 1;
            """, (repayment_amount,))
            
            if cur.rowcount == 0:
                raise Exception("Failed to update loan system funds.")

            
            cur.execute("""
                INSERT INTO Transactions (user_id, loan_id, transaction_type, amount, transaction_date)
                VALUES (%s, %s, 'Debit', %s, CURRENT_DATE);
            """, (self.user_id, loan_id, repayment_amount))

            
            cur.execute("COMMIT;")

            return {'success': True, 'message': message}
        
        except Exception as e:
            cur.execute("ROLLBACK;")
            return {'success': False, 'message': f"Error while processing repayment: {e}"}

    def send_money(self, amount, receiver_id):
        try:
            if amount <= 0:
                raise ValueError("Transfer amount must be greater than 0.")

            amount = Decimal(amount)

            
            cur.execute("BEGIN;")

            
            sender_account = get_or_create_user_financial(self.user_id)

            
            receiver_account = get_or_create_user_financial(receiver_id)

            
            sender_balance = Decimal(sender_account["balance"])
            if sender_balance < amount:
                raise Exception(f"Insufficient funds. Your balance is ₦{sender_balance:,.2f}.")

            
            cur.execute("""
                UPDATE UserFinancials
                SET balance = balance - %s
                WHERE user_id = %s;
            """, (amount, self.user_id))

            
            cur.execute("""
                UPDATE UserFinancials
                SET balance = balance + %s
                WHERE user_id = %s;
            """, (amount, receiver_id))

            
            cur.execute("""
                INSERT INTO Transactions (user_id, transaction_type, amount, transaction_date)
                VALUES (%s, 'Debit', %s, CURRENT_TIMESTAMP);
            """, (self.user_id, amount))
            
            
            cur.execute("""
                INSERT INTO Transactions (user_id, transaction_type, amount, transaction_date)
                VALUES (%s, 'Credit', %s, CURRENT_TIMESTAMP);
            """, (receiver_id, amount))

            
            cur.execute("""
                INSERT INTO transfer_history (user_id, sender, receiver, amount, date_created)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
            """, (self.user_id, self.user_id, receiver_id, amount))

            
            cur.execute("COMMIT;")

            return {
                "success": True,
                "message": f"Successfully transferred ₦{amount:,.2f} to {receiver_id}."
            }

        except Exception as e:
            cur.execute("ROLLBACK;")
            return {
                "success": False,
                "message": f"Error during money transfer: {e}"
            }
      
      
    # THERE IS AN ERROR IN FETCHING USER BALANCE IN A SCENARIO WHERE THE USER DOES NOT HAVE A FINANCIAL OR THE USER DOES NOT OWE ANY AMOUNT    
    def fetch_user_balance(self):
        try:
            cur.execute(
                """
                SELECT 
                    uf.balance, 
                    COALESCE(SUM(r.amount_due - r.amount_paid), 0) AS total_outstanding_with_interest
                FROM UserFinancials uf
                LEFT JOIN Loans l ON uf.user_id = l.user_id
                LEFT JOIN Repayments r ON l.loan_id = r.loan_id
                WHERE uf.user_id = %s AND r.status = 'Pending'
                GROUP BY uf.balance;
                """,
                (self.user_id,)
            )
            result = cur.fetchone()

            if not result:
                return {"success": False, "message": "User not found or no financial data available."}

            balance, total_outstanding_with_interest = result

            return {
                "success": True,
                "balance": float(balance),
                "total_outstanding_with_interest": float(total_outstanding_with_interest)
            }

        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {e}"}

        except Exception as e:
            return {"success": False, "message": f"An unexpected error occurred: {e}"}

    # THERE IS AN ERROR ALSO IN GET TRANSACTION HISTORY, WHERE IT IS FETCHING IT TEICE. ONE FROM THE TRANSACTIONS AND ONE FOR THE TRANSFER HISTORY
    # POSSIBLE FIXING ERROR, MERGING TRANSFER HISTORY AND TRANSACTIONS TO ONE TABLE
    def get_transaction_history(self):
        try:
            cur.execute(
                """
                SELECT 
                    transaction_type,
                    amount,
                    transaction_date,
                    sender_name,
                    receiver_name
                FROM (
                    SELECT 
                        Transactions.transaction_type,
                        Transactions.amount,
                        Transactions.transaction_date,
                        CASE 
                            WHEN Transactions.transaction_type = 'Credit' AND Transactions.loan_id IS NOT NULL THEN 'CLI_LP'
                            WHEN Transactions.transaction_type = 'Debit' AND Transactions.loan_id IS NOT NULL THEN U1.name
                            ELSE U1.name
                        END AS sender_name,
                        CASE 
                            WHEN Transactions.transaction_type = 'Debit' AND Transactions.loan_id IS NOT NULL THEN 'CLI_LP'
                            WHEN Transactions.transaction_type = 'Credit' AND Transactions.loan_id IS NOT NULL THEN U2.name
                            ELSE U2.name
                        END AS receiver_name
                    FROM Transactions
                    LEFT JOIN Users AS U1 ON Transactions.user_id = U1.user_id
                    LEFT JOIN Loans ON Transactions.loan_id = Loans.loan_id
                    LEFT JOIN Users AS U2 ON Loans.user_id = U2.user_id
                    WHERE Transactions.user_id = %s

                    UNION ALL

                    
                    SELECT 
                        'Transfer' AS transaction_type,
                        transfer_history.amount,
                        transfer_history.date_created AS transaction_date,
                        U1.name AS sender_name,
                        U2.name AS receiver_name
                    FROM transfer_history
                    LEFT JOIN Users AS U1 ON transfer_history.sender::varchar = U1.user_id::varchar
                    LEFT JOIN Users AS U2 ON transfer_history.receiver::varchar = U2.user_id::varchar
                    WHERE transfer_history.user_id = %s
                ) AS combined_transactions
                ORDER BY transaction_date DESC;
                """,
                (self.user_id, self.user_id)
            )
            transactions = cur.fetchall()

            if not transactions:
                return {"success": True, "data": []}

            # Format transactions for easier readability
            formatted_transactions = []
            for transaction in transactions:
                formatted_transactions.append({
                    "type": transaction[0],
                    "amount": f"#{transaction[1]:,.2f}",
                    "date": transaction[2].strftime('%B %d, %Y, %I:%M %p'),
                    "sender": transaction[3] or "N/A",
                    "receiver": transaction[4] or "N/A"
                })

            return {"success": True, "data": formatted_transactions}

        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Error retrieving transaction history: {e}"}


class Admin():
    def get_users_paginated(self, page=1, page_size=10):
        """
        Fetch users with pagination (default: 10 users per page).
        
        Args:
            page (int): The page number (starting from 1).
            page_size (int): The number of users per page.
        
        Returns:
            dict: Contains the user list, total user count, and pagination metadata.
        """
        try:
            offset = (page - 1) * page_size
            
            # Fetch paginated users
            cur.execute("""
                SELECT user_id, name, email, phone_number, created_at
                FROM Users
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;
            """, (page_size, offset))
            users = cur.fetchall()

            # Fetch total user count
            cur.execute("SELECT COUNT(*) FROM Users;")
            total_users = cur.fetchone()[0]

            if not users:
                return {"success": True, "data": [], "total_users": total_users, "message": "No users found."}

            # Format user data
            formatted_users = [
                {
                    "user_id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "phone_number": user[3] or "N/A",
                    "created_at": user[4].strftime('%B %d, %Y, %I:%M %p')
                }
                for user in users
            ]

            return {
                "success": True,
                "data": formatted_users,
                "total_users": total_users,
                "current_page": page,
                "total_pages": (total_users + page_size - 1) // page_size  # Calculate total pages
            }

        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Error fetching users: {e}"}

    def delete_user(self, user_id):
        try:
            cur.execute(f"""DELETE FROM users WHERE user_id = {user_id}""")
            conn.commit()
            return {'success': True, 'message': 'User deleted successfully'}
        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Error fetching users: {e}"}
        
    def create_admin(self, user_id):
        try:
            cur.execute(f"""SELECT name, email, password FROM users WHERE user_id = {user_id}""")
            data = cur.fetchone()
            
            cur.execute(f"INSERT INTO admins(name, email, password) VALUES(%s, %s, %s)", (data[0], data[1], data[2]))
            conn.commit()
            
            return {'success': True, 'message': 'Admin created successfully'}
            
        except psycopg2.Error as e:
            return {"success": False, "message": f"Database error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Error fetching users: {e}"}
    
    def search_users_db(self, search_query, page=1, page_size=10):
        """
        Search for users in the database by name, email, or phone number.

        Args:
            search_query (str): The search keyword (name, email, or phone number).
            page (int): The page number for pagination.
            page_size (int): The number of results per page.

        Returns:
            dict: A dictionary containing search results, total pages, and success status.
        """
        try:
            offset = (page - 1) * page_size  # Calculate offset for pagination

            cur.execute("""
                SELECT user_id, name, email, phone_number
                FROM Users
                WHERE name ILIKE %s OR email ILIKE %s OR phone_number ILIKE %s
                ORDER BY name ASC
                LIMIT %s OFFSET %s;
            """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", page_size, offset))

            users = cur.fetchall()

            # Get total number of users matching search criteria for pagination
            cur.execute("""
                SELECT COUNT(*) FROM Users
                WHERE name ILIKE %s OR email ILIKE %s OR phone_number ILIKE %s;
            """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))

            total_users = cur.fetchone()[0]
            total_pages = -(-total_users // page_size)  # Equivalent to math.ceil()

            return {
                "success": True,
                "data": [{"user_id": u[0], "name": u[1], "email": u[2], "phone_number": u[3]} for u in users],
                "total_pages": total_pages
            }

        except Exception as e:
            return {"success": False, "message": f"Database error: {e}"}
        
    def show_loan_system(self):
        try:
            cur.execute("""
                SELECT available_funds
                FROM LoanSystem;
            """)
            loans = cur.fetchone()
            return {
                "success": True,
                "data": f"{loans[0]:,.2f}"}
        except Exception as e:
            return {"success": False, "message": f"Database error: {e}"}