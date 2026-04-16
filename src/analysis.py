"""Sales analysis functions"""
import pandas as pd
import numpy as np

def rep_performance(df):
    """Analyze individual sales rep performance"""
    return df.groupby('sales_rep').agg({
        'revenue': ['sum', 'mean'],
        'deal_size': 'mean',
        'sales_cycle_days': 'mean'
    }).round(2)

def monthly_trends(df):
    """Calculate monthly revenue trends"""
    df['month'] = df['date'].dt.to_period('M')
    return df.groupby('month')['revenue'].agg(['sum', 'count', 'mean']).round(2)

def forecast_revenue(df, periods=4):
    """Simple trend-based revenue forecast"""
    monthly = monthly_trends(df)
    last_revenue = monthly['sum'].iloc[-1]
    avg_growth = monthly['sum'].pct_change().mean()
    
    forecast = []
    for i in range(1, periods + 1):
        forecast.append(last_revenue * (1 + avg_growth) ** i)
    
    return forecast
