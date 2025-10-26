# Excel Import Format Instructions

This document explains how to format your Excel file for importing transactions into the Personal Finance Manager.

## Required Excel Format

### Required Columns (in this exact order)

Your Excel file must have the following columns in the first row (header row):

1. **Type** - Transaction type (must be either "expense" or "income")
2. **Amount** - Transaction amount (must be a positive number)
3. **Category** - Category of the transaction (see valid categories below)
4. **Date** - Transaction date in YYYY-MM-DD format
5. **Description** - Optional description of the transaction
6. **Payment Method** - Payment method used (see valid methods below)

### Valid Values

#### Transaction Types
- `expense`
- `income`

#### Categories for Expense
- Food
- Transport
- Bills
- Shopping
- Entertainment
- Other

#### Categories for Income
- Salary
- Freelance
- Investment
- Gift
- Other

#### Payment Methods
- Cash
- Credit Card
- Debit Card
- Bank Transfer

### Date Format
Dates must be in **YYYY-MM-DD** format. Examples:
- `2025-01-15` ✓
- `2025-12-31` ✓
- `1/15/2025` ✗ (Not accepted)
- `15-01-2025` ✗ (Not accepted)

## Example Excel File

```
| Type    | Amount | Category    | Date       | Description           | Payment Method |
|---------|--------|-------------|------------|-----------------------|----------------|
| expense | 50.00  | Food        | 2025-01-15 | Grocery shopping      | Credit Card    |
| income  | 5000.00| Salary      | 2025-01-01 | Monthly salary        | Bank Transfer  |
| expense | 100.00 | Transport   | 2025-01-16 | Gas fill              | Cash           |
```

## Import Process

1. Create your Excel file with the required columns in the header row
2. Fill in your transaction data in subsequent rows
3. Make sure all required fields (Type, Amount, Category, Date) are filled
4. Save the file as `.xlsx` format
5. Use the "Import from Excel" option in the Transactions Menu
6. Enter the path to your Excel file when prompted

## Validation

Before importing, the system will validate:
- All required columns are present
- All required fields are filled
- Transaction types are valid
- Amounts are positive numbers
- Categories match the transaction type
- Dates are in the correct format (YYYY-MM-DD)
- Payment methods are valid

If validation fails, you will see detailed error messages indicating which rows have issues.

## Export Format

When you export transactions, the system creates an Excel file with these columns:
- Transaction ID
- Type
- Amount
- Category
- Date
- Description
- Payment Method

You can use exported files as templates for future imports.

## Notes

- Description and Payment Method are optional fields (will default to empty string and "Cash" respectively)
- Make sure dates are not in the future (system will reject future dates)
- The Excel file must have at least one data row (in addition to the header row)
- File must be saved in `.xlsx` format

