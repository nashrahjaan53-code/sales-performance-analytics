import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_sales_data, get_summary_stats
from src.analysis import rep_performance, monthly_trends, forecast_revenue

# Page config
st.set_page_config(page_title="Sales Analytics", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
df = load_sales_data('data/sales_data.csv')

if df is not None:
    st.markdown('<div class="header"><h1>📊 Sales Performance Analytics Dashboard</h1></div>', 
                unsafe_allow_html=True)
    
    # METRICS ROW
    col1, col2, col3, col4 = st.columns(4)
    stats = get_summary_stats(df)
    
    with col1:
        st.metric("Total Revenue", f"${stats['total_revenue']:,.0f}", delta="+12%")
    with col2:
        st.metric("Avg Deal Size", f"${stats['avg_deal_size']:,.0f}", delta="+5%")
    with col3:
        st.metric("Total Deals", f"{stats['total_deals']:.0f}", delta="+8")
    with col4:
        st.metric("Avg Sales Cycle", f"{stats['avg_sales_cycle']:.0f} days", delta="-2 days")
    
    st.divider()
    
    # TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "👥 Rep Performance", "🎯 Revenue Forecast", "📊 Analysis"])
    
    # TAB 1: TRENDS
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Monthly Revenue Trend (Line Chart)")
            monthly = monthly_trends(df)
            fig_line = px.line(monthly.reset_index(), x='month', y='sum',
                             markers=True, title="Revenue Over Time",
                             labels={'sum': 'Revenue ($)', 'month': 'Month'})
            fig_line.update_traces(line=dict(color='#667eea', width=3))
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.subheader("Monthly Deal Count (Bar Chart)")
            fig_bar = px.bar(monthly.reset_index(), x='month', y='count',
                           title="Deals Per Month",
                           labels={'count': 'Number of Deals', 'month': 'Month'},
                           color='count', color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue Distribution (Histogram)")
            fig_hist = px.histogram(df, x='revenue', nbins=10, title="Revenue Distribution",
                                   labels={'revenue': 'Revenue ($)'},
                                   color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.subheader("Product Category Breakdown (Pie Chart)")
            category_data = df.groupby('product_category')['revenue'].sum()
            fig_pie = px.pie(values=category_data.values, names=category_data.index,
                           title="Revenue by Product Category",
                           color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # TAB 2: REP PERFORMANCE
    with tab2:
        st.subheader("Sales Rep Performance Comparison")
        
        rep_perf = rep_performance(df)
        rep_perf_reset = rep_perf.reset_index()
        rep_perf_reset.columns = ['Sales Rep', 'Total Revenue', 'Avg Revenue', 'Avg Deal Size', 'Avg Sales Cycle']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Total Revenue by Rep (Bar Chart)")
            fig_rep_revenue = px.bar(rep_perf_reset, x='Sales Rep', y='Total Revenue',
                                    title="Total Revenue Generated",
                                    color='Total Revenue',
                                    color_continuous_scale='Viridis')
            st.plotly_chart(fig_rep_revenue, use_container_width=True)
        
        with col2:
            st.subheader("Avg Deal Size by Rep (Bar Chart)")
            fig_rep_deal = px.bar(rep_perf_reset, x='Sales Rep', y='Avg Deal Size',
                                 title="Average Deal Size",
                                 color='Avg Deal Size',
                                 color_continuous_scale='Plasma')
            st.plotly_chart(fig_rep_deal, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales Cycle Length by Rep (Scatter)")
            fig_cycle = px.scatter(rep_perf_reset, x='Sales Rep', y='Avg Sales Cycle',
                                  size='Total Revenue', title="Sales Cycle vs Revenue",
                                  hover_name='Sales Rep', hover_data=['Total Revenue'])
            st.plotly_chart(fig_cycle, use_container_width=True)
        
        with col2:
            st.subheader("Rep Performance Table")
            st.dataframe(rep_perf_reset, use_container_width=True, hide_index=True)
    
    # TAB 3: FORECASTING
    with tab3:
        st.subheader("Revenue Forecasting & Predictions")
        
        forecast = forecast_revenue(df, periods=4)
        historical = monthly_trends(df)['sum'].values
        months = ['Q2', 'Q3', 'Q4', 'Q1-2025']
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical))),
            y=historical.tolist(),
            mode='lines+markers',
            name='Historical',
            line=dict(color='#667eea', width=3)
        ))
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical)-1, len(historical) + len(forecast))),
            y=forecast,
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#FF6B6B', width=3, dash='dash')
        ))
        fig_forecast.update_layout(title="Revenue Forecast (Next 4 Quarters)",
                                   xaxis_title="Period",
                                   yaxis_title="Revenue ($)",
                                   hovermode='x unified')
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        st.subheader("Forecast Details")
        forecast_df = pd.DataFrame({
            'Quarter': months,
            'Predicted Revenue': [f"${x:,.0f}" for x in forecast]
        })
        st.table(forecast_df)
    
    # TAB 4: DETAILED ANALYSIS
    with tab4:
        st.subheader("Detailed Sales Data Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Customer Segment Performance (Pie)")
            segment_revenue = df.groupby('customer_segment')['revenue'].sum()
            fig_segment = px.pie(values=segment_revenue.values, 
                               names=segment_revenue.index,
                               title="Revenue by Customer Segment")
            st.plotly_chart(fig_segment, use_container_width=True)
        
        with col2:
            st.subheader("Deal Size Distribution (Box Plot)")
            fig_box = px.box(df, x='sales_rep', y='deal_size',
                           title="Deal Size Distribution by Rep",
                           color='sales_rep')
            st.plotly_chart(fig_box, use_container_width=True)
        
        st.subheader("Raw Data")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="sales_data.csv",
            mime="text/csv"
        )
else:
    st.error("Unable to load data. Check the data file path.")
