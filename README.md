# Personal Finance Manager

A comprehensive console-based Personal Finance Manager that helps users track income, expenses, savings goals, and generate financial reports.

## Features

- **Transaction Management**: Add, edit, delete, and view transactions (income/expenses)
- **Bill Reminders**: Set up recurring bill reminders
- **Budget Tracker**: Monitor spending against budgets
- **Financial Reports**: Generate detailed financial reports
- **Search & Filter**: Search and filter transactions by various criteria
- **Excel Import/Export**: Import transactions from Excel files and export data for external analysis
- **User Profiles**: Multiple user support with individual accounts

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd personal-finance-manager
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Transaction Management

- Add individual transactions manually
- Import multiple transactions from Excel files
- Export your transactions to Excel for external analysis

### Excel Import/Export

#### Importing Transactions

The system supports importing transactions from Excel files. See `EXCEL_FORMAT_INSTRUCTIONS.md` for detailed format requirements.

A sample template (`transaction_template.xlsx`) is included with the application.

Required Excel columns:
- Type (expense/income)
- Amount (positive number)
- Category (see valid categories in instructions)
- Date (YYYY-MM-DD format)
- Description (optional)
- Payment Method (optional)

#### Exporting Transactions

Export your transactions to Excel for external analysis or backup.

## File Structure

```
personal-finance-manager/
├── main.py                          # Main application entry point
├── users.py                         # User management
├── transactions.py                  # Transaction management
├── excel.py                         # Excel import/export functionality
├── billreminder.py                 # Bill reminder management
├── budget_tracker.py               # Budget tracking
├── reports.py                      # Financial reports
├── search_filter.py                # Search and filter
├── jsonhandler.py                  # JSON data handling
├── utility.py                      # Utility functions
├── menu.py                         # Main menu interface
├── data/
│   ├── users.json                  # User data
│   ├── transactions.json           # Transaction data
│   ├── bills.json                  # Bill data
│   ├── budgets.json                # Budget data
│   └── backup/                     # Data backups
├── transaction_template.xlsx       # Sample Excel template
├── EXCEL_FORMAT_INSTRUCTIONS.md    # Excel format guide
└── requirements.txt                # Python dependencies
```

## Requirements

- Python 3.x
- openpyxl (for Excel import/export)

See `requirements.txt` for all dependencies.

## Data Storage

All data is stored in JSON files in the `data/` directory:
- User data is automatically backed up
- Transaction data can be exported to Excel
- Regular backups are recommended

## License

This project is part of a learning exercise and is provided as-is. 
