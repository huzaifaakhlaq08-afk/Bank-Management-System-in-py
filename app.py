import json
import random
import string
from pathlib import Path
import streamlit as st

class Bank:
    DATABASE = "data.json"

    @classmethod
    def _load_data(cls):
        """Safely loads data from the JSON database file."""
        if Path(cls.DATABASE).exists():
            try:
                with open(cls.DATABASE, "r") as fs:
                    return json.load(fs)
            except Exception as err:
                st.error(f"Error loading database: {err}")
                return []
        return []

    @classmethod
    def _save_data(cls, data):
        """Saves current data back to the JSON file."""
        try:
            with open(cls.DATABASE, "w") as fs:
                json.dump(data, fs, indent=4)
        except Exception as err:
            st.error(f"Failed to save data: {err}")

    @classmethod
    def _generate_account_number(cls):
        """Generates a unique 7-character alphanumeric account ID."""
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$&*%^", k=1)
        id_list = alpha + num + spchar
        random.shuffle(id_list)
        return "".join(id_list)

    @classmethod
    def create_account(cls, name, age, email, pin):
        """Creates a new user account with validation."""
        if age < 18:
            return False, "You must be at least 18 years old to open an account."
        if not (pin.isdigit() and len(pin) == 4):
            return False, "PIN must be a valid 4-digit number."

        data = cls._load_data()

        # Check if email already exists in the database
        for account in data:
            if account.get("email", "").lower() == email.strip().lower():
                return False, "An account with this Email Address already exists!"

        account_number = cls._generate_account_number()

        new_account = {
            "name": name,
            "age": age,
            "email": email.strip(),
            "pin": int(pin),
            "account_number": account_number,
            "balance": 0.0,
        }

        data.append(new_account)
        cls._save_data(data)
        return True, new_account

    @classmethod
    def authenticate(cls, acc_number, pin):
        """Validates credentials and returns account data if matched."""
        if not pin.isdigit():
            return None
        data = cls._load_data()
        for account in data:
            acc_id = account.get("account_number") or account.get("account number")
            if acc_id == acc_number and account.get("pin") == int(pin):
                return account
        return None

    @classmethod
    def deposit(cls, acc_number, pin, amount):
        """Deposits specified amount within limits."""
        if amount <= 0 or amount > 15000:
            return False, "Deposit amount must be between 1 and 15,000 PKR."

        data = cls._load_data()
        for account in data:
            acc_id = account.get("account_number") or account.get("account number")
            if acc_id == acc_number and account.get("pin") == int(pin):
                account["balance"] += amount
                cls._save_data(data)
                return True, account["balance"]
        return False, "Authentication failed. Account not found or incorrect PIN."

    @classmethod
    def withdraw(cls, acc_number, pin, amount):
        """Withdraws funds if sufficient balance is available."""
        if amount <= 0:
            return False, "Amount must be greater than zero."

        data = cls._load_data()
        for account in data:
            acc_id = account.get("account_number") or account.get("account number")
            if acc_id == acc_number and account.get("pin") == int(pin):
                if account["balance"] < amount:
                    return False, "Insufficient funds."
                account["balance"] -= amount
                cls._save_data(data)
                return True, account["balance"]
        return False, "Authentication failed. Account not found or incorrect PIN."

    @classmethod
    def update_details(cls, acc_number, pin, new_name, new_email, new_pin):
        """Updates optional account details."""
        data = cls._load_data()

        # Check if new email is already used by someone else
        if new_email.strip():
            for account in data:
                if account.get("email", "").lower() == new_email.strip().lower():
                    acc_id = account.get("account_number") or account.get("account number")
                    if acc_id != acc_number:
                        return False, "This new email is already registered with another account."

        for account in data:
            acc_id = account.get("account_number") or account.get("account number")
            if acc_id == acc_number and account.get("pin") == int(pin):
                if new_name.strip():
                    account["name"] = new_name.strip()
                if new_email.strip():
                    account["email"] = new_email.strip()
                if new_pin.strip():
                    if not (new_pin.isdigit() and len(new_pin) == 4):
                        return False, "New PIN must be exactly 4 digits."
                    account["pin"] = int(new_pin)

                cls._save_data(data)
                return True, "Account details successfully updated."
        return False, "Authentication failed."

    @classmethod
    def delete_account(cls, acc_number, pin):
        """Permanently removes account from database."""
        data = cls._load_data()
        for i, account in enumerate(data):
            acc_id = account.get("account_number") or account.get("account number")
            if acc_id == acc_number and account.get("pin") == int(pin):
                del data[i]
                cls._save_data(data)
                return True, "Account deleted successfully."
        return False, "Authentication failed. Account not found or incorrect PIN."


# --- STREAMLIT UI IMPLEMENTATION ---

st.set_page_config(page_title="Banking Application", page_icon="🏦", layout="centered")

st.title("🏦 Banking Management System")

menu = [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "Account Details",
    "Update Profile",
    "Delete Account",
]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Create Account":
    st.subheader("Account Registration")
    with st.form("create_acc_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        email = st.text_input("Email Address")
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Create Account")

        if submit:
            if not name or not email:
                st.warning("Please fill out all required fields.")
            else:
                success, response = Bank.create_account(name, age, email, pin)
                if success:
                    st.success("Account created successfully!")
                    st.json(response)
                    st.info("⚠️ Please save your account number securely.")
                else:
                    st.error(f"Failed: {response}")

elif choice == "Deposit Money":
    st.subheader("Deposit Funds")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
    amount = st.number_input("Deposit Amount (PKR)", min_value=1.0, max_value=15000.0, step=100.0)

    if st.button("Deposit"):
        success, response = Bank.deposit(acc_num, pin, amount)
        if success:
            st.success(f"Deposit Successful! Updated Balance: {response:,.2f} PKR")
        else:
            st.error(f"Error: {response}")

elif choice == "Withdraw Money":
    st.subheader("Withdraw Funds")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
    amount = st.number_input("Withdrawal Amount (PKR)", min_value=1.0, step=100.0)

    if st.button("Withdraw"):
        success, response = Bank.withdraw(acc_num, pin, amount)
        if success:
            st.success(f"Withdrawal Successful! Remaining Balance: {response:,.2f} PKR")
        else:
            st.error(f"Error: {response}")

elif choice == "Account Details":
    st.subheader("View Profile Details")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("4-Digit PIN", type="password", max_chars=4)

    if st.button("Fetch Details"):
        user_data = Bank.authenticate(acc_num, pin)
        if user_data:
            st.write("### Account Summary")
            st.write(f"**Name:** {user_data['name']}")
            st.write(f"**Email:** {user_data['email']}")
            st.write(f"**Age:** {user_data['age']}")
            acc_id = user_data.get('account_number') or user_data.get('account number')
            st.write(f"**Account Number:** `{acc_id}`")
            st.write(f"**Balance:** {user_data['balance']:,.2f} PKR")
        else:
            st.error("Invalid Account Number or PIN.")

elif choice == "Update Profile":
    st.subheader("Modify Profile Information")
    acc_num = st.text_input("Current Account Number")
    pin = st.text_input("Current 4-Digit PIN", type="password", max_chars=4)

    st.write("---")
    st.caption("Leave blank any fields you do not wish to change.")
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_pin = st.text_input("New 4-Digit PIN", type="password", max_chars=4)

    if st.button("Update Details"):
        success, message = Bank.update_details(acc_num, pin, new_name, new_email, new_pin)
        if success:
            st.success(message)
        else:
            st.error(f"Error: {message}")

elif choice == "Delete Account":
    st.subheader("Close Account")
    st.warning("Warning: This action is permanent and cannot be undone.")
    acc_num = st.text_input("Account Number")
    pin = st.text_input("4-Digit PIN", type="password", max_chars=4)

    confirm = st.checkbox("I confirm that I want to delete this account permanently.")

    if st.button("Delete Account"):
        if not confirm:
            st.warning("Please check the confirmation box to proceed.")
        else:
            success, message = Bank.delete_account(acc_num, pin)
            if success:
                st.success(message)
            else:
                st.error(f"Error: {message}")