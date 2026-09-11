# Bank Management System (Python CLI Application)

A fully functional, object-oriented Command Line Interface (CLI) Banking Application built using Python and JSON-based persistent storage.

---

## Key Features

* **Account Creation:** Generates unique alpha-numeric account numbers with PIN security.
* **Deposits & Withdrawals:** Enforces transaction range limits (0 - 15,000 PKR) and real-time balance calculations.
* **Account Modifications:** Allows safe updates to mutable details (e.g., Name, Email, PIN) while protecting core attributes.
* **Account Deletion:** Includes interactive confirmation prompts before removing user records.
* **Data Persistence:** Utilizes native JSON file storage (`data.json`) with OOP-driven read/write operations.

---

## Repository Structure

* `Bank Manag. Proj.py` / `app.py` — Core banking operations, class logic, and CLI menu handlers.
* `data.json` — Database storage for user accounts and transaction records.

---