💻 Program Flow (Expense Tracker Project)

🔹 Run main.py
 → The program starts.

🔹 Load data
 → Load existing users and transactions from JSON files.

🔹 Login Screen
 → User enters username and password.
 → Validate credentials.
 → If valid → proceed to the main menu.

🔹 Main Menu
 → Display options (Add Transaction, View Transactions, Reports, etc.).
 → User selects an option.

🔹 User chooses (1) Add Transaction
 → Prompt for details: amount, category, date, description, type (income/expense).
 → Validate inputs.

🔹 Save Transaction
 → Store the transaction in memory.
 → Automatically update the JSON file (auto-save enabled).

🔹 Return to Main Menu
 → Display the main options again.

🔹 User chooses (3) Reports → Dashboard
 → Generate and display a financial summary:
  • Total Income
  • Total Expenses
  • Net Balance

🔹 Exit Program
 → When the user exits, trigger auto-save again to ensure all data is saved.
 → Display a goodbye message and close the application.