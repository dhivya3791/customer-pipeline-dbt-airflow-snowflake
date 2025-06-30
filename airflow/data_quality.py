import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Connect to Snowflake using env vars
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PW'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA'),
    role=os.getenv('SNOWFLAKE_ROLE')
)

def fetch_table(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, conn)

def insert_flagged(df, table_name):
    # write flagged data back to snowflake table
    write_pandas(conn, df, table_name, auto_create_table=True, overwrite=False)

def check_referential_integrity(fact_df, dim_df, key_col, dim_name):
    missing_keys = fact_df[~fact_df[key_col].isin(dim_df[key_col])].copy()
    if not missing_keys.empty:
        missing_keys['issue'] = f'Missing {key_col} in {dim_name}'
    return missing_keys

def iqr_anomaly_detection(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = df[(df[column] < lower_bound) | (df[column] > upper_bound)].copy()
    if not anomalies.empty:
        anomalies['ISSUES'] = f'IQR anomaly in {column}'
    return anomalies

def run_data_quality_checks():
    fact_orders = fetch_table('FACT_ORDERS')
    dim_customers = fetch_table('DIM_CUSTOMER')
    dim_products = fetch_table('DIM_PRODUCT')

    # Referential integrity checks
    missing_customers = check_referential_integrity(fact_orders, dim_customers, 'CUSTOMER_ID', 'DIM_CUSTOMER')
    missing_products = check_referential_integrity(fact_orders, dim_products, 'PRODUCT_ID', 'DIM_PRODUCT')

    # IQR anomaly detection on quantity and price
    quantity_anomalies = iqr_anomaly_detection(fact_orders, 'QUANTITY')
    price_anomalies = iqr_anomaly_detection(fact_orders, 'UNIT_PRICE')

    # Combine all anomalies
    flagged = pd.concat([missing_customers, missing_products, quantity_anomalies, price_anomalies], ignore_index=True)

    if flagged.empty:
        print("No data quality issues detected.")
    else:
        print(f"Flagged {len(flagged)} rows for review.")
        print(flagged[['ORDER_ID', 'CUSTOMER_ID', 'PRODUCT_ID', 'QUANTITY', 'UNIT_PRICE', 'ISSUES']])

        # Write flagged rows to a Snowflake table (create if not exists)
        insert_flagged(flagged, 'FACT_ORDERS_QUALITY_FLAGS')

if __name__ == "__main__":
    run_data_quality_checks()
