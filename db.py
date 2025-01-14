import psycopg2
import bcrypt

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
#     dob DATE NOT NULL,
#     phone_number VARCHAR(15) UNIQUE NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        return cur.fetchone()
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
        cur.execute("SELECT password FROM Users WHERE user_id = %s", (user_id,))
        result = cur.fetchone()

        if result:
            stored_password_hash = result[0]
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
        INSERT INTO Users (name, email, password, age, phone_number)
        VALUES (%s, %s, %s, %s, %s) RETURNING user_id;
    """
    
    cur.execute(insert_query, (name, email, password, dob, phone_number))
    user_id = cur.fetchone()[0]
    conn.commit()
    
    return {'success': True, 'user': user_id, 'message': 'Account created successfully'}

if __name__ == "__main__":
    pass