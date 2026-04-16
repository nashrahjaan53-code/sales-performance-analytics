"""Data loading utilities"""
import pandas as pd
import os

def load_sales_data(filepath='data/sales_data.csv'):
    """Load sales data from CSV"""
    if not os.path.exists(filepath):
        print(f"File {filepath} not found")
        return None
    
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')

def get_summary_stats(df):
    """Calculate summary statistics"""
    return {
        'total_revenue': df['revenue'].sum(),
        'avg_deal_size': df['deal_size'].mean(),
        'total_deals': len(df),
        'avg_sales_cycle': df['sales_cycle_days'].mean()
    }
