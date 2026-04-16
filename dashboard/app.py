"""⭐ SALES ANALYTICS - PROFESSIONAL DASHBOARD"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Sales Analytics", layout="wide")

C1, C2, C3, C4 = "#0f3460", "#16213e", "#e94560", "#00d4ff"

st.markdown(f"""<style>
.header {{background: linear-gradient(135deg, {C1} 0%, {C2} 100%); padding: 40px; border-radius: 15px; color: white; margin-bottom: 30px;}}
.metric {{background: linear-gradient(135deg, #1a5f7a 0%, {C1} 100%); padding: 25px; border-radius: 12px; color: white; text-align: center;}}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/sales_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')

df = load_data()
st.markdown(f'<div class="header"><h1>💼 Sales Performance Dashboard</h1><p>Advanced Analytics & Intelligence</p></div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric"><p>Total Revenue</p><h3>${df["revenue"].sum():,.0f}</h3></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric"><p>Avg Deal</p><h3>${df["deal_size"].mean():,.0f}</h3></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric"><p>Total Deals</p><h3>{len(df)}</h3></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric"><p>Cycle Days</p><h3>{df["sales_cycle_days"].mean():.0f}</h3></div>', unsafe_allow_html=True)

st.divider()

t1, t2, t3, t4 = st.tabs(["📈 Trends", "👥 Reps", "🔮 Forecast", "📊 Details"])

with t1:
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['revenue'].sum()
    c1, c2 = st.columns(2)
    
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[str(m) for m in monthly.index], y=monthly.values, fill='tozeroy', line=dict(color=C4, width=3)))
        fig.update_layout(title="Monthly Revenue", height=400, plot_bgcolor='rgba(0,0,0,.05)')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        monthly_count = df.groupby('month').size()
        fig = px.bar(x=[str(m) for m in monthly_count.index], y=monthly_count.values, title="Monthly Deals", color=monthly_count.values, color_continuous_scale='Blues')
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,.05)')
        st.plotly_chart(fig, use_container_width=True)

with t2:
    rep_data = df.groupby('sales_rep').agg({'revenue': 'sum', 'deal_size': 'mean'}).sort_values('revenue', ascending=False)
    c1, c2 = st.columns(2)
    
    with c1:
        fig = px.bar(x=rep_data.index, y=rep_data['revenue'], title="Revenue by Rep", color=rep_data['revenue'], color_continuous_scale='Greens')
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,.05)')
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        fig = px.bar(x=rep_data.index, y=rep_data['deal_size'], title="Avg Deal by Rep", color=rep_data['deal_size'], color_continuous_scale='Oranges')
        fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,.05)')
        st.plotly_chart(fig, use_container_width=True)

with t3:
    monthly_rev = df.groupby('month')['revenue'].sum()
    growth = monthly_rev.pct_change().mean()
    last = monthly_rev.iloc[-1]
    forecast = [last * (1+growth)**i for i in range(1, 5)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[str(m) for m in monthly_rev.index], y=monthly_rev.values, name='Historical', line=dict(color=C4)))
    fig.add_trace(go.Scatter(x=['Q2','Q3','Q4','Q1-25'], y=forecast, name='Forecast', line=dict(color=C3, dash='dash')))
    fig.update_layout(title="Revenue Forecast", height=450, plot_bgcolor='rgba(0,0,0,.05)')
    st.plotly_chart(fig, use_container_width=True)

with t4:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(values=df.groupby('product_category')['revenue'].sum().values, names=df.groupby('product_category')['revenue'].sum().index, title="Revenue by Category")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(values=df.groupby('customer_segment')['revenue'].sum().values, names=df.groupby('customer_segment')['revenue'].sum().index, title="Revenue by Segment")
        st.plotly_chart(fig, use_container_width=True)
    
    csv = df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "sales.csv", "text/csv")
