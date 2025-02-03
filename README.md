# Loan System App

## 📌 Introduction
The **Loan System App** is a robust financial management platform designed to facilitate **loans, secure money transfers, user financial tracking, and admin management**. The system ensures **seamless transactions**, **secure user management**, and **detailed financial reporting**.

## 🚀 Features
### 🔹 User Features
- **Register & Manage Financial Account**
- **Send Money to Other Users**
- **Apply for Loans & Make Repayments**
- **View Transaction History (Loans, Transfers, Deposits)**
- **Search for Users by Name, Email, or Phone Number**

### 🔹 Admin Features
- **Fetch Users with Pagination**
- **Search & Select Users for Actions**
- **Delete Users or Promote to Admin**
- **View Loan System Financial Balance & Total Loans Given**

---

## ⚙️ Installation & Setup
### Prerequisites
- Python 3.8+
- PostgreSQL
- Required Python Libraries (install via `pip`)

### Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/loan-system-app.git
   cd loan-system-app
   ```
2. **Create & Activate Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure the Database** (PostgreSQL required)
   ```sh
   psql -U your_user -d your_database -f schema.sql
   ```
5. **Run the Application**
   ```sh
   python app.py
   ```

---

## 🛠 Usage Guide
### 🎯 1. User Account Management
- Users automatically get financial accounts upon first transaction.
- Accounts track **balance, loans, and transactions**.

```python
get_or_create_user_financial(user_id)
```

### 💳 2. Send Money
- Ensures **sufficient balance** before processing transfers.
- Secure transactions recorded in **transfer history**.

```python
send_money(self, amount, receiver_id)
```

### 📜 3. View Transaction History
- Displays all **debits, credits, and transfers**.

```python
get_transaction_history(self)
```

### 🔍 4. Search Users (Admin Only)
- Find users by **name, email, or phone number**.

```python
search_user_interactive(self)
```

### 📂 5. Paginated User Management (Admin Only)
- View users **10 at a time** with a **next page option**.

```python
select_user_paginated(self, page_size=10)
```

### ⚙️ 6. Admin Actions on Users
- Select a user and choose to **delete or promote to admin**.

```python
_select_users(self)
```

### 🏦 7. View Loan System Financial Balance
- Shows **total system balance** and **loans issued**.

```python
show_loan_system_balance(self)
```

---

## 📌 Database Schema Overview
- `Users` – Stores user details.
- `UserFinancials` – Tracks account balance and loan data.
- `Loans` – Handles loan applications and repayments.
- `Transactions` – Logs all financial transactions.
- `transfer_history` – Stores peer-to-peer money transfers.

---

## 🛠 Technologies Used
- **Backend:** Python, PostgreSQL
- **Libraries:** psycopg2, questionary (CLI interactivity)
- **Security:** Input validation, SQL parameterized queries

---

## 📜 License
This project is licensed under the MIT License.

---

## 📞 Support & Contributions
Feel free to **fork, modify, or contribute** to this project! For issues, open a ticket on **GitHub Issues** or contact us.

---

🚀 **Built for efficiency, security, and seamless user experience!**

