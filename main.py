"""Main analysis script for Sales Performance Analytics"""
from src.data_loader import load_sales_data, get_summary_stats
from src.analysis import rep_performance, monthly_trends, forecast_revenue

def main():
    print("=" * 60)
    print("SALES PERFORMANCE ANALYTICS")
    print("=" * 60)
    
    # Load data
    df = load_sales_data('data/sales_data.csv')
    
    if df is None:
        return
    
    # Summary stats
    print("\n📊 SUMMARY STATISTICS:")
    stats = get_summary_stats(df)
    for key, value in stats.items():
        print(f"  {key}: ${value:,.2f}" if 'revenue' in key or 'size' in key else f"  {key}: {value:.2f}")
    
    # Rep performance
    print("\n👥 SALES REP PERFORMANCE:")
    print(rep_performance(df))
    
    # Monthly trends
    print("\n📈 MONTHLY REVENUE TRENDS:")
    print(monthly_trends(df))
    
    # Revenue forecast
    print("\n🔮 QUARTERLY REVENUE FORECAST:")
    forecast = forecast_revenue(df, periods=4)
    quarters = ['Q2', 'Q3', 'Q4', 'Q1-2025']
    for quarter, value in zip(quarters, forecast):
        print(f"  {quarter}: ${value:,.2f}")

if __name__ == "__main__":
    main()
