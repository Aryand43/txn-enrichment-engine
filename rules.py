# rules.py

# Define ordered regex rules for transaction enrichment.
# Each rule is a tuple: (regex_pattern, merchant_class, transaction_class, is_credit_card, reason)
# Regex will be applied to both 'TransactionName' and 'NormalizedEntity' in a case-insensitive manner.

ENRICHMENT_RULES = [
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

