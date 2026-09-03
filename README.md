# GST Calculator
A command-line tool that calculates GST on products and prints a bill, handling intra-state vs inter-state tax.

GST rates are calculated based on the categories it fall under if it doesnt meet as per the list a default rate of 18% is taken into consideration

'''python
gst_rates = {
    "essentials": 5,
    "standard": 12,
    "electronics": 18,
    "luxury": 28,
    "misc": 18
}
'''

## What it does
- Takes product details (name, price, category, sale type)
- Looks up the GST rate by category
- Splits tax correctly: CGST+SGST for same-state, IGST for different-state
- Prints a formatted bill

## How to run
python src/main.py

## How to test
Adding two test cases to check on interstate and intrastate categorization and to check total value

python -m pytest

## Next steps
- Save bills to a database (persistence)
- Monthly summary of total sales and GST