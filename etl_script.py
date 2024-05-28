"""
ETL Script: Extract data from a CSV file, transform it, and load it into a PostgreSQL database.
"""

import logging
import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
import yaml

# Ensure you have the required packages
# pip install pandas sqlalchemy psycopg2 pyyaml

# Logging configuration
logging.basicConfig(filename='etl_log.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def log_and_print(message, level=logging.INFO):
    """
    Log and print a message.

    :param message: The message to log and print
    :param level: The logging level
    """
    if level == logging.INFO:
        logging.info(message)
    elif level == logging.ERROR:
        logging.error(message)
    elif level == logging.WARNING:
        logging.warning(message)
    print(message)

def extract_data(file_path):
    """
    Extract data from a CSV file.

    :param file_path: Path to the CSV file
    :return: DataFrame with the extracted data
    """
    try:
        log_and_print(f"Starting data extraction from {file_path}")
        df = pd.read_csv(file_path)
        log_and_print("Data extraction completed successfully")
        return df
    except FileNotFoundError as e:
        log_and_print(f"File not found: {e}", level=logging.ERROR)
        raise
    except pd.errors.EmptyDataError as e:
        log_and_print(f"Empty data error: {e}", level=logging.ERROR)
        raise
    except Exception as e:
        log_and_print(f"Error during data extraction: {e}", level=logging.ERROR)
        raise

def transform_data(df):
    """
    Transform the extracted data.

    :param df: DataFrame with the extracted data
    :return: DataFrame with the transformed data
    """
    try:
        log_and_print("Starting data transformation")
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].astype(float)
        
        # Data validation
        if df['amount'].isnull().any() or df['date'].isnull().any():
            raise ValueError("Data contains null values after transformation")
        
        # Additional data quality checks
        if (df['amount'] < 0).any():
            raise ValueError("Amount column contains negative values")
        
        df_cleaned = df.dropna()
        log_and_print("Data transformation completed successfully")
        return df_cleaned
    except ValueError as e:
        log_and_print(f"Value error: {e}", level=logging.ERROR)
        raise
    except Exception as e:
        log_and_print(f"Error during data transformation: {e}", level=logging.ERROR)
        raise

def load_data(df, db_url, table_name):
    """
    Load the transformed data into a PostgreSQL database.

    :param df: DataFrame with the transformed data
    :param db_url: Database connection URL
    :param table_name: Name of the target table
    """
    try:
        log_and_print(f"Starting data load into {table_name} table")
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        log_and_print("Data load completed successfully")
    except Exception as e:
        log_and_print(f"Error during data load: {e}", level=logging.ERROR)
        raise

def load_config(config_file):
    """
    Load configuration from a YAML file.

    :param config_file: Path to the configuration file
    :return: Configuration dictionary
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            log_and_print("Configuration loaded successfully")
            return config
    except Exception as e:
        log_and_print(f"Error loading configuration file: {e}", level=logging.ERROR)
        raise

def main():
    """
    Main function to orchestrate the ETL process.
    """
    parser = argparse.ArgumentParser(description='ETL Script')
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
        file_path = config.get('file_path', 'data.csv')
        db_url = config.get('db_url', 'postgresql://user:password@localhost:5432/mydatabase')
        table_name = config.get('table_name', 'transactions')
    else:
        file_path = 'data.csv'
        db_url = os.getenv('DB_URL', 'postgresql://user:password@localhost:5432/mydatabase')
        table_name = 'transactions'

    # Replace environment variables in db_url
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_url = db_url.replace('${DB_USER}', db_user).replace('${DB_PASS}', db_pass)

    df = extract_data(file_path)
    df_cleaned = transform_data(df)
    load_data(df_cleaned, db_url, table_name)

if __name__ == "__main__":
    main()
