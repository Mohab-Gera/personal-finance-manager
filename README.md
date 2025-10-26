# Personal Finance Manager

A comprehensive console-based Personal Finance Manager that helps users track income, expenses, budgets, and generate financial reports. This application provides a complete solution for personal financial management with features like transaction tracking, budget management, bill reminders, and detailed financial reporting.

## 🌟 Core Features

### 1. Transaction Management
- Add, edit, view, and delete financial transactions
- Support for both income and expenses
- Categorized transactions with detailed tracking
- Multiple payment methods support
- Transaction history with date tracking
- Custom descriptions and notes

### 2. Budget Tracking System
- Set monthly budgets for different categories
- Real-time budget vs. actual spending tracking
- Budget status monitoring with percentage used
- Delete or modify existing budgets
- Visual representation of budget utilization

### 3. Bill Reminder System
- Set up recurring bill reminders
- Never miss a payment deadline
- Notification system for upcoming bills
- Track payment history
- Flexible scheduling options

### 4. Financial Reports
- Generate comprehensive financial reports
- Income vs. Expense analysis
- Category-wise spending breakdown
- Monthly and yearly summaries
- Export capabilities for external analysis

### 5. Search & Filter Functionality
- Search transactions by multiple criteria
- Filter by date range, category, or amount
- Advanced search options
- Sort and organize results

### 6. Excel Integration
- Import transactions from Excel files
- Export data for external analysis
- Standardized Excel templates
- Bulk transaction processing

## 📁 Project Structure

### Core Files and Their Functions

#### `main.py`
- Application entry point
- Main program loop
- User authentication and session management
- Menu coordination

#### `menu.py`
- Interactive menu system
- User interface handling
- Navigation between different features
- Display formatting and user prompts

#### `transactions.py`
Key features:
- `TransactionManager` class for transaction handling
- Add/Edit/Delete transaction operations
- Transaction validation and processing
- Category management (expense/income categories)
- Payment method handling

#### `budget_tracker.py`
Key features:
- Monthly budget setting and tracking
- Real-time spending monitoring
- Budget vs. Actual comparison
- Budget deletion and modification
- Percentage calculations for budget utilization

#### `billreminder.py`
Key features:
- Bill scheduling and tracking
- Reminder system implementation
- Recurring bill management
- Payment status tracking
- Due date monitoring

#### `reports.py`
Key features:
- Financial report generation
- Data aggregation and analysis
- Summary statistics
- Custom report formatting
- Export functionality

#### `search_filter.py`
Key features:
- Transaction search implementation
- Filter criteria processing
- Result sorting and organization
- Advanced search options
- Data retrieval optimization

#### `excel.py`
Key features:
- Excel file processing
- Data import/export functions
- Template management
- Data validation
- Bulk transaction processing

#### `users.py`
Key features:
- User account management
- Authentication
- Profile management
- Security implementation
- User preferences

#### `jsonhandler.py`
Key features:
- Data persistence layer
- JSON file operations
- Data structure management
- Error handling
- Data validation

#### `utility.py`
- Common utility functions
- Helper methods
- Data formatting
- Input validation
- System utilities

### Data Storage (`data/` directory)
- `users.json`: User account information
- `transactions.json`: Transaction records
- `bills.json`: Bill reminder data
- `budgets.json`: Budget tracking information

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip package manager

### Installation

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

### Running the Application
```bash
python main.py
```

## 💡 Usage Guide

### 1. First Time Setup
1. Launch the application
2. Create a new user account
3. Log in with your credentials

### 2. Managing Transactions
- Add transactions with category, amount, and date
- View transaction history
- Edit or delete existing transactions
- Import transactions from Excel

### 3. Setting Up Budgets
1. Navigate to Budget Tracker
2. Set monthly budgets for different categories
3. Monitor spending against budgets
4. View budget status and utilization
5. Delete or modify budgets as needed

### 4. Using Bill Reminders
1. Add new bill reminders
2. Set recurring schedules
3. View upcoming bills
4. Mark bills as paid

### 5. Generating Reports
1. Access the Reports section
2. Select report type
3. Choose time period
4. View or export results

### 6. Search and Filter
1. Use search function for specific transactions
2. Apply filters for detailed analysis
3. Sort and organize results
4. Export filtered data if needed

## 📊 Excel Integration

### Importing Transactions
1. Prepare Excel file according to template
2. Use Import function
3. Review and confirm transactions
4. Save imported data

Required Excel columns:
- Type (expense/income)
- Amount
- Category
- Date (YYYY-MM-DD)
- Description (optional)
- Payment Method (optional)

See `EXCEL_FORMAT_INSTRUCTIONS.md` for detailed format requirements.

## 🔒 Data Security
- Local JSON storage
- Password protection
- Data validation
- Error handling
- Regular backups recommended

## 📋 Requirements

See `requirements.txt` for complete list of dependencies.

Main requirements:
- Python 3.x
- openpyxl
- Other dependencies as listed in requirements.txt

## ⚠️ Important Notes
- Regular backups recommended
- Keep Python and dependencies updated
- Review transactions regularly
- Set realistic budgets
- Keep bill reminders up to date

## 🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests.

## 📄 License
This project is licensed under the MIT License.

All data is stored in JSON files in the `data/` directory:
- User data is automatically backed up
- Transaction data can be exported to Excel
- Regular backups are recommended

## License

This project is part of a learning exercise and is provided as-is. 
