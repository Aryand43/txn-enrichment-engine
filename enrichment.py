import pandas as pd
import re
from rules import ENRICHMENT_RULES

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

    # Apply rules sequentially
    for pattern, merchant_class, transaction_class, is_credit_card, reason in ENRICHMENT_RULES:
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
