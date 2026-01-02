import pandas as pd
import re

def enrich_transactions(df):
    """
    Applies ordered regex rules to enrich transaction data with classifications and reasons.
    Rules are priority-based (first match wins).
    """

    # Initialize new columns
    df['MerchantClassification'] = 'other'
    df['TransactionClassification'] = 'other'
    df['IsCreditCardExpense'] = 0
    df['Reason'] = 'no rule matched'

    # Define ordered regex rules
    # Each rule is a tuple: (regex_pattern, merchant_class, transaction_class, is_credit_card, reason)
    # Regex will be applied to both 'TransactionName' and 'NormalizedEntity'
    rules = [
        # Credit cards (visa, mastercard, amex)
        (r'(visa|mastercard|amex|american express)', 'financial service', 'credit card payment', 1, 'credit card type matched'),
        
        # Payment gateways (stripe, paypal)
        (r'(stripe|paypal)', 'payment gateway', 'online payment', 0, 'payment gateway matched'),

        # Ecommerce (amazon, shopee)
        (r'(amazon|shopee|ebay|etsy)', 'ecommerce', 'online shopping', 0, 'ecommerce site matched'),
        
        # Salary / income (more general patterns for income, usually credit transactions)
        (r'(salary|payroll|income|deposit)', 'employer', 'income', 0, 'income keyword matched'),

        # ATM / cash (withdrawals)
        (r'(atm|cash|withdrawal)', 'bank', 'cash withdrawal', 0, 'atm/cash keyword matched'),
        
        # Example for specific merchants not covered by general categories
        (r'starbucks', 'coffee shop', 'dining', 0, 'starbucks matched'),
        (r'netflix', 'entertainment', 'subscription', 0, 'netflix matched'),

        # More general categories
        (r'restaurant|cafe|diner', 'dining', 'food & drinks', 0, 'restaurant/cafe matched'),
        (r'grocery|supermarket', 'groceries', 'food & drinks', 0, 'grocery matched'),
        (r'fuel|gas station', 'automotive', 'transportation', 0, 'fuel matched'),
        (r'telecom|phone bill', 'utilities', 'bills', 0, 'telecom matched'),
        (r'utility|electricity|water', 'utilities', 'bills', 0, 'utility matched'),
        (r'rent|mortgage', 'housing', 'bills', 0, 'housing matched'),
        (r'insurance', 'financial service', 'insurance', 0, 'insurance matched'),
        (r'travel|airline|hotel', 'travel', 'travel', 0, 'travel matched'),
        (r'hospital|clinic|pharmacy', 'health', 'healthcare', 0, 'medical matched'),
        (r'gym|fitness', 'health', 'fitness', 0, 'fitness matched'),
        (r'education|school', 'education', 'education', 0, 'education matched'),


    ]

    # Apply rules sequentially
    for pattern, merchant_class, transaction_class, is_credit_card, reason in rules:
        # Create a mask for rows where the rule has not been applied yet
        unmatched_mask = (df['Reason'] == 'no rule matched')

        # Check 'TransactionName' and 'NormalizedEntity'
        match_name = df['TransactionName'].astype(str).str.contains(pattern, case=False, na=False, regex=True)
        match_entity = df['NormalizedEntity'].astype(str).str.contains(pattern, case=False, na=False, regex=True)
        
        # Combine matches and apply only to unmatched rows
        matched_rows = unmatched_mask & (match_name | match_entity)

        df.loc[matched_rows, 'MerchantClassification'] = merchant_class
        df.loc[matched_rows, 'TransactionClassification'] = transaction_class
        df.loc[matched_rows, 'IsCreditCardExpense'] = is_credit_card
        df.loc[matched_rows, 'Reason'] = reason

    # TODO: Implement spaCy fallback for unclassified transactions
    # If 'Reason' is still 'no rule matched', apply spaCy-based classification here.

    return df

if __name__ == "__main__":
    # Example Usage (assuming a preprocessed DataFrame structure)
    data = {
        'TransactionName': [
            'VISA PAYMENT GOOGLE',
            'AMAZON WEB SERVICES',
            'PAYPAL TRANSFER',
            'SALARY DEPOSIT',
            'ATM CASH WITHDRAWAL',
            'STARBUCKS COFFEE',
            'Generic Purchase XYZ',
            'Netflix Subscription',
            'LOCAL RESTAURANT',
            'FRESH GROCERIES',
            'SHELL GAS STATION',
            'ONLINE UTILITY BILL',
            'HOME RENT PAYMENT',
            'HEALTH INSURANCE',
            'TRAVEL AGENCY BOOKING',
            'HOSPITAL VISIT',
            'GYM MEMBERSHIP FEE',
            'UNIVERSITY TUITION',
            'MasterCard Payment',
            'Stripe Inc Payment',
            'Shopee Order',
            'Income from client',
            'Cash from bank',
            'The Best Cafe',
            'Walmart Supercenter',
            'Chevron Fuel',
            'AT&T Bill',
            'Water Company Bill',
            'Mortgage Payment',
            'Geico Auto Insurance',
            'Delta Airlines Ticket',
            'Clinic Appointment',
            'Anytime Fitness',
            'Coursera Course Fee',
            'Something Unclassified'
        ],
        'NormalizedEntity': [
            'Google Pay',
            'Amazon',
            'PayPal',
            'Employer Co',
            'Bank of America',
            'Starbucks',
            'Generic Vendor',
            'Netflix',
            'Local Eatery',
            'Fresh Foods Inc',
            'Shell',
            'Power & Light',
            'Landlord',
            'Blue Cross',
            'Expedia',
            'City Hospital',
            'Anytime Fitness',
            'State University',
            'Capital One',
            'Stripe',
            'Shopee',
            'Client Payment',
            'Local Bank ATM',
            'The Best Cafe',
            'Walmart',
            'Chevron',
            'AT&T',
            'Municipal Water',
            'Bank Mortgage',
            'Geico',
            'Delta',
            'Urgent Care Clinic',
            'Anytime Fitness',
            'Coursera',
            'Unknown Entity'
        ],
        'SignedAmount': [
            -50.00, -25.50, -100.00, 2000.00, -60.00, -8.50, -15.00, -12.99, -30.00, -55.00, -40.00, -75.00, -1200.00, -150.00, -300.00, -80.00, -35.00, -500.00,
            -20.00, -45.00, -70.00, 1500.00, -100.00, -25.00, -60.00, -30.00, -80.00, -60.00, -1000.00, -120.00, -400.00, -90.00, -40.00, -600.00, -10.00
        ],
        'TransactionDate': pd.to_datetime([
            '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10', '2023-01-11', '2023-01-12', '2023-01-13', '2023-01-14',
            '2023-01-15', '2023-01-16', '2023-01-17', '2023-01-18', '2023-01-19', '2023-01-20', '2023-01-21', '2023-01-22', '2023-01-23', '2023-01-24',
            '2023-01-25', '2023-01-26', '2023-01-27', '2023-01-28', '2023-01-29', '2023-01-30', '2023-01-31', '2023-02-01', '2023-02-02', '2023-02-03',
            '2023-02-04', '2023-02-05', '2023-02-06', '2023-02-07', '2023-02-08'
        ]),
        'IsCredit': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'IsDebit': [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    dummy_preprocessed_df = pd.DataFrame(data)

    enriched_df = enrich_transactions(dummy_preprocessed_df.copy())
    print("\nEnrichment complete. Enriched DataFrame head:")
    print(enriched_df.head())

    print("\nSample of unclassified transactions:")
    print(enriched_df[enriched_df['Reason'] == 'no rule matched'].head())

