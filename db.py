import psycopg2
import bcrypt
from datetime import datetime

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
        if result:
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
        print(f"Database error: {e}")
        return {'success': False, 'user':None, 'message':'Database error.'}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {'success': False, 'user':None, 'message':'Unknon Error.'}
    
    
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
        
class Transaction():
    def __init__(self, user_id, financial_id):
        self.user_id = user_id
        self.financial_id = financial_id
        
    def fund_system(self, fund_amount):
        cur.execute("""UPDATE LoanSystem SET available_funds = available_funds + %s, last_updated = CURRENT_TIMESTAMP""", (fund_amount))
    
    def take_loan(self, loan_amount):
        try:
            if loan_amount <= 0:
                raise ValueError("Loan amount must be greater than 0.")
            
            cur.execute("BEGIN;")
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

            
            cur.execute("""
                UPDATE LoanSystem
                SET available_funds = available_funds - %s,
                    total_loans_given = total_loans_given + %s,
                    last_updated = CURRENT_TIMESTAMP
                WHERE available_funds >= %s;
            """, (loan_amount, loan_amount, loan_amount))

            
            if cur.rowcount == 0:
                raise Exception("Insufficient funds in the loan system.")

            
            cur.execute("""
                INSERT INTO Loans (
                    user_id, loan_amount, interest_rate, tenure_months, 
                    status, created_at
                )
                VALUES (%s, %s, 0.40, 12, 'Approved', CURRENT_TIMESTAMP)
                RETURNING loan_id;
            """, (self.user_id, loan_amount))
            loan_id = cur.fetchone()[0]

            
            cur.execute("""
                INSERT INTO Transactions (
                    user_id, loan_id, transaction_type, amount, transaction_date
                )
                VALUES (%s, %s, 'Credit', %s, CURRENT_DATE);
            """, (self.user_id, loan_id, loan_amount))

            
            cur.execute("COMMIT;")
            return {'success': True, 'message': 'Loan Successfull'}

        except Exception as e:
            cur.execute("ROLLBACK;")
            return {'success': False, 'message': f'Error while processing loan: {e}'}

    def repay_loan(self, repayment_amount):
        try:
            
            if repayment_amount <= 0:
                raise ValueError("Repayment amount must be greater than 0.")
            
            
            cur.execute("BEGIN;")
            
            
            cur.execute("""
                UPDATE UserFinancials
                SET balance = balance - %s, 
                    amount_owed = amount_owed - %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND balance >= %s AND amount_owed >= %s;
            """, (repayment_amount, repayment_amount, self.user_id, repayment_amount, repayment_amount))

            
            if cur.rowcount == 0:
                raise Exception("Insufficient balance or invalid repayment amount.")
            
            
            cur.execute("""
                UPDATE Repayments
                SET amount_paid = amount_paid + %s, 
                    status = CASE 
                                WHEN amount_paid + %s >= amount_due THEN 'Paid' 
                                ELSE 'Pending' 
                            END
                WHERE loan_id IN (
                    SELECT loan_id 
                    FROM Loans 
                    WHERE user_id = %s AND status = 'Approved'
                    ORDER BY created_at ASC
                    LIMIT 1
                )
                RETURNING loan_id;
            """, (repayment_amount, repayment_amount, self.user_id))
            
            
            result = cur.fetchone()
            if not result:
                raise Exception("No pending loans found to apply the repayment.")
            loan_id = result[0]

            
            cur.execute("""
                UPDATE LoanSystem
                SET available_funds = available_funds + %s, 
                    total_earnings = total_earnings + (%s * 0.05), -- Assuming 5% earnings
                    last_updated = CURRENT_TIMESTAMP;
            """, (repayment_amount, repayment_amount))

            
            cur.execute("""
                INSERT INTO Transactions (
                    user_id, loan_id, transaction_type, amount, transaction_date
                )
                VALUES (%s, %s, 'Debit', %s, CURRENT_DATE);
            """, (self.user_id, loan_id, repayment_amount))

            
            cur.execute("""
                UPDATE Loans
                SET status = 'Repaid'
                WHERE loan_id = %s AND 
                    NOT EXISTS (
                        SELECT 1 FROM Repayments 
                        WHERE loan_id = %s AND status = 'Pending'
                    );
            """, (loan_id, loan_id))

            
            cur.execute("COMMIT;")
            print(f"Repayment of {repayment_amount} successfully applied to loan {loan_id} for user {self.user_id}.")

        except Exception as e:
            cur.execute("ROLLBACK;")
            print(f"Error while processing loan repayment: {e}")
