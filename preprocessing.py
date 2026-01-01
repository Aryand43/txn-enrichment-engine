import pandas as pd
import numpy as np

def read_data(file_path):
    """
    Reads the Excel file into a pandas DataFrame.
    """
    df = pd.read_excel(file_path)
    return df

def parse_dates(df, date_columns):
    """
    Parses specified columns as dates, handling potential errors.
    """
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def fix_excel_overflow(df, numeric_columns):
    """
    Fixes Excel overflow cells ('########') by coercing to numeric safely.
    """
    for col in numeric_columns:
        # Replace '########' with NaN and then convert to numeric
        df[col] = df[col].replace('########', np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def convert_credit_debit(df, credit_col, debit_col, new_amount_col):
    """
    Converts Credit and Debit columns into a single signed amount column.
    Credit amounts are positive, Debit amounts are negative.
    """
    df[new_amount_col] = df[credit_col].fillna(0) - df[debit_col].fillna(0)
    return df

def normalize_text_fields(df, text_columns, noise_patterns=None):
    """
    Normalizes text fields by lowercasing and stripping specified noise patterns.
    """
    if noise_patterns is None:
        noise_patterns = ['electronic', 'web auth']

    for col in text_columns:
        df[col] = df[col].astype(str).str.lower().str.strip()
        for pattern in noise_patterns:
            df[col] = df[col].str.replace(pattern, '', regex=False).str.strip()
    return df

def flag_credit_debit(df, amount_col, credit_flag_col, debit_flag_col):
    """
    Flags transactions as credit or debit based on the signed amount.
    """
    df[credit_flag_col] = (df[amount_col] > 0).astype(int)
    df[debit_flag_col] = (df[amount_col] < 0).astype(int)
    return df

def validate_schema(df, expected_columns, numeric_cols, date_cols):
    """
    Validates the DataFrame schema to ensure clean and consistent output.
    Raises an error if the schema does not match.
    """
    # Check for expected columns
    if not all(col in df.columns for col in expected_columns):
        missing = [col for col in expected_columns if col not in df.columns]
        raise ValueError(f"Missing expected columns: {missing}")

    # Check for correct dtypes (basic validation)
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(f"Column '{col}' is not numeric.")
    for col in date_cols:
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            raise TypeError(f"Column '{col}' is not datetime.")

    return df

def preprocess_data(file_path):
    """
    Orchestrates the preprocessing pipeline for the transaction data.
    """
    # Define column names based on assumed input structure
    date_cols = ['TransactionDate']
    amount_col = 'TransactionAmountUSD'
    description_cols = ['TransactionName', 'NormalizedEntity']

    # Define output column names
    new_amount_col = 'SignedAmount'
    credit_flag_col = 'IsCredit'
    debit_flag_col = 'IsDebit'
    
    # 1. Read Data
    df = read_data(file_path)

    # 2. Parse Dates
    df = parse_dates(df, date_cols)


    # 5. Normalize text fields
    # Assign the existing amount column to new_amount_col as it's already signed
    df[new_amount_col] = df[amount_col]

    # 3. Normalize text fields
    df = normalize_text_fields(df, description_cols)

    # 4. Flag credit vs debit
    df = flag_credit_debit(df, new_amount_col, credit_flag_col, debit_flag_col)

    # 6. Flag credit vs debit
    df = flag_credit_debit(df, new_amount_col, credit_flag_col, debit_flag_col)

    # Define the expected final schema for validation
    expected_columns = date_cols + description_cols + [amount_col, new_amount_col, credit_flag_col, debit_flag_col, 'TransactionClassification', 'MerchantClassification', 'IsCreditCardExpense']
    numeric_cols = [amount_col, new_amount_col, credit_flag_col, debit_flag_col, 'IsCreditCardExpense']

    # 7. Validate and enforce a clean, consistent schema
    df = validate_schema(df, expected_columns, numeric_cols, date_cols)

    return df

if __name__ == "__main__":
    # Example usage:
    try:
        cleaned_df = preprocess_data("Data.xlsx")
        print("\nPreprocessing complete. Cleaned DataFrame head:")
        print(cleaned_df.head())
        cleaned_df.to_csv("cleaned_data.csv", index=False)
        print("\nCleaned data saved to cleaned_data.csv")
    except Exception as e:
        print(f"\nAn error occurred during preprocessing: {e}")


