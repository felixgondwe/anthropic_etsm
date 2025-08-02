import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ETSM Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'Enterprise Technical Success Manager Dashboard - Powered by Anthropic'
    }
)

# Custom CSS for better styling and readability
st.markdown("""
<style>
    /* Simple, robust text visibility */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Force all text to be black on white background */
    .stMarkdown, .stText, .stSelectbox, .stTextArea, .stButton, 
    .stMetric, .stDataFrame, .stExpander, .stAlert, .stSidebar {
        color: #000000 !important;
    }
    
    /* Force textarea to be readable */
    .stTextArea textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Force selectbox to be readable */
    .stSelectbox select {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Force button text to be readable */
    .stButton button {
        color: #000000 !important;
    }
    
    /* Force sidebar to be light with dark text */
    .stSidebar {
        background-color: #ffffff !important;
        border-right: 1px solid #e9ecef !important;
    }
    
    .stSidebar * {
        color: #000000 !important;
    }
    
    /* Force metric text to be readable */
    .metric-container, .metric-container * {
        color: #000000 !important;
    }
    
    /* Force dataframe text to be readable */
    .dataframe, .dataframe * {
        color: #000000 !important;
    }
    
    /* Force expander text to be readable */
    .streamlit-expanderHeader {
        color: #000000 !important;
    }
    
    /* Force alert text to be readable */
    .stAlert {
        color: #000000 !important;
    }
    
    /* Force all metric values to be readable */
    .stMetric, .stMetric * {
        color: #000000 !important;
    }
    
    /* Force success/error/warning messages to be readable */
    .stSuccess, .stError, .stWarning {
        color: #000000 !important;
    }
    
    .stSuccess *, .stError *, .stWarning * {
        color: #000000 !important;
    }
    
    /* Anthropic branding - matching official website */
    .anthropic-header {
        background: #ffffff;
        color: #000000;
        padding: 30px 20px;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .anthropic-logo {
        font-size: 2rem;
        margin-bottom: 15px;
        color: #000000;
    }
    
    .anthropic-tagline {
        font-size: 1.2rem;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 20px;
    }
    
    .powered-by {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    .claude-badge {
        display: inline-block;
        background: #000000;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 3px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .anthropic-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        margin-bottom: 10px;
    }
    
    .anthropic-subtitle {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 400;
    }
    
    .strategy-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .strategy-card h3 {
        color: #000000;
        margin-bottom: 10px;
        font-size: 1.2rem;
    }
    
    .strategy-card p {
        color: #000000;
        margin: 5px 0;
    }
    
    .prompt-card, .response-card {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
</style>
""", unsafe_allow_html=True)



# Anthropic branding header with Try Claude button
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("")  # Empty column for spacing

with col2:
    st.markdown("""
    <div class="anthropic-header">
        <div class="anthropic-logo">🤖</div>
        <div class="anthropic-title">ETSM Dashboard</div>
        <div class="anthropic-subtitle">Enterprise Technical Success Manager Platform</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: right; margin-top: 20px;">
        <a href="https://claude.ai/new" target="_blank">
            <button style="
                background-color: #000000;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            ">Chat w/Claude</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Anthropic API function
def call_anthropic_api(prompt, model="claude-sonnet-4-20250514"):
    """Call Anthropic's API to generate insights"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return "API key not found. Please check your .env file."
    
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": model,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            return f"API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error calling API: {str(e)}"

# Mock data generation
def generate_api_usage_data():
    """Generate realistic API usage data"""
    companies = ['Acme Corp', 'Zenith PLC', 'Global Dynamics', 'TechStart Inc', 'DataFlow Ltd']
    
    data = []
    for company in companies:
        base_usage = random.randint(50000, 2000000)
        for month in range(1, 13):
            # Add realistic growth/decline patterns
            if company == 'Acme Corp':
                usage = base_usage * (1 + 0.15 * month)  # Growing
            elif company == 'Zenith PLC':
                usage = base_usage * (1 - 0.05 * month)  # Declining
            else:
                usage = base_usage * (1 + random.uniform(-0.1, 0.1) * month)  # Variable
            
            data.append({
                'Company': company,
                'Month': f'2024-{month:02d}',
                'API_Calls': max(0, int(usage)),
                'Revenue': usage * 0.001,  # Mock revenue calculation
                'Use_Cases': random.randint(1, 5)
            })
    
    return pd.DataFrame(data)

def generate_strategy_data():
    """Generate strategy board data"""
    strategies = [
        {
            'Account': 'Acme Corp',
            'Strategy': 'Expand AI-Powered Analytics',
            'Status': 'In Progress',
            'Priority': 'High',
            'Expected_Revenue': 150000,
            'Timeline': 'Q2 2024',
            'Key_Stakeholder': 'Sarah Chen (CTO)',
            'Description': 'Implement advanced analytics using Claude API for customer insights'
        },
        {
            'Account': 'Zenith PLC',
            'Strategy': 'Optimize Document Processing',
            'Status': 'Planning',
            'Priority': 'Critical',
            'Expected_Revenue': 80000,
            'Timeline': 'Q1 2024',
            'Key_Stakeholder': 'Jennifer Kim (CEO)',
            'Description': 'Address declining usage with new document processing use case'
        },
        {
            'Account': 'Global Dynamics',
            'Strategy': 'Launch Customer Service Bot',
            'Status': 'Completed',
            'Priority': 'Medium',
            'Expected_Revenue': 120000,
            'Timeline': 'Q1 2024',
            'Key_Stakeholder': 'David Thompson (CTO)',
            'Description': 'Successfully implemented AI-powered customer service solution'
        },
        {
            'Account': 'TechStart Inc',
            'Strategy': 'Content Generation Platform',
            'Status': 'In Progress',
            'Priority': 'High',
            'Expected_Revenue': 200000,
            'Timeline': 'Q3 2024',
            'Key_Stakeholder': 'Alex Rodriguez (VP Product)',
            'Description': 'Building automated content generation for marketing materials'
        },
        {
            'Account': 'DataFlow Ltd',
            'Strategy': 'Data Analysis Automation',
            'Status': 'Planning',
            'Priority': 'Medium',
            'Expected_Revenue': 95000,
            'Timeline': 'Q2 2024',
            'Key_Stakeholder': 'Lisa Wang (VP Engineering)',
            'Description': 'Automate data analysis workflows using Claude API'
        }
    ]
    return pd.DataFrame(strategies)

# Load data
usage_df = generate_api_usage_data()
strategy_df = generate_strategy_data()

# Main dashboard
st.markdown('<h1 class="main-header">📊 ETSM Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #000000;">Enterprise Technical Success Manager Platform</p>', unsafe_allow_html=True)

# Check for API key (only show error if missing, not success message)
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    st.error("⚠️ **API Key Missing!** Please create a `.env` file in the project root with your Anthropic API key:")
    st.code("ANTHROPIC_API_KEY=your_api_key_here")
    st.info("Get your API key from: https://console.anthropic.com/")

# Sidebar navigation
st.sidebar.title("Menu")
page = st.sidebar.selectbox(
    "Select Dashboard:",
    ["Account Analysis", "API Usage Dashboard", "Strategy Boards", "Account Overview"]
)

if page == "API Usage Dashboard":
    st.subheader("📈 API Usage Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_usage = usage_df['API_Calls'].sum()
        st.metric("Total API Calls", f"{total_usage:,}", delta="+15% this quarter")
    
    with col2:
        avg_growth = usage_df.groupby('Company')['API_Calls'].apply(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]).mean()
        st.metric("Average Growth", f"{avg_growth:.1%}", delta="+2.3% this month")
    
    with col3:
        active_accounts = usage_df['Company'].nunique()
        st.metric("Active Accounts", active_accounts, delta="+1 this quarter")
    
    with col4:
        total_revenue = usage_df['Revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}", delta="+12% this quarter")
    
    # Usage trends
    st.subheader("📊 Usage Trends by Company")
    
    fig = px.line(usage_df, x='Month', y='API_Calls', color='Company',
                  title="Monthly API Usage Trends",
                  color_discrete_map={
                      'Acme Corp': '#1f77b4',      # Blue
                      'Zenith PLC': '#ff7f0e',      # Orange
                      'Global Dynamics': '#2ca02c',  # Green
                      'TechStart Inc': '#d62728',    # Red
                      'DataFlow Ltd': '#9467bd'      # Purple
                  })
    fig.update_layout(
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12)
    )
    fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
    fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
    st.plotly_chart(fig, use_container_width=True)
    
    # Usage comparison
    col1, col2 = st.columns(2)
    
    with col1:
        latest_usage = usage_df.groupby('Company')['API_Calls'].last().sort_values(ascending=True)
        fig = px.bar(x=latest_usage.values, y=latest_usage.index, orientation='h',
                    title="Current API Usage by Company",
                    color=latest_usage.values,
                    color_continuous_scale='Blues')
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12)
        )
        fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
        fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        growth_rates = usage_df.groupby('Company').apply(
            lambda x: (x['API_Calls'].iloc[-1] - x['API_Calls'].iloc[0]) / x['API_Calls'].iloc[0]
        ).sort_values(ascending=True)
        
        fig = px.bar(x=growth_rates.values, y=growth_rates.index, orientation='h',
                    title="Growth Rates by Company",
                    color=growth_rates.values,
                    color_continuous_scale='RdYlGn')
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12)
        )
        fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
        fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Strategy Boards":
    st.subheader("🎯 Strategy Boards")
    
    # Strategy overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_revenue = strategy_df['Expected_Revenue'].sum()
        st.metric("Total Pipeline", f"${total_revenue:,}", delta="+$50K this month")
    
    with col2:
        in_progress = len(strategy_df[strategy_df['Status'] == 'In Progress'])
        st.metric("In Progress", in_progress, delta="+2 this quarter")
    
    with col3:
        completed = len(strategy_df[strategy_df['Status'] == 'Completed'])
        st.metric("Completed", completed, delta="+1 this month")
    
    # Strategy cards
    st.subheader("📋 Active Strategies")
    
    for _, strategy in strategy_df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="strategy-card">
                <h3>{strategy['Account']} - {strategy['Strategy']}</h3>
                <p><strong>Status:</strong> {strategy['Status']} | <strong>Priority:</strong> {strategy['Priority']}</p>
                <p><strong>Expected Revenue:</strong> ${strategy['Expected_Revenue']:,} | <strong>Timeline:</strong> {strategy['Timeline']}</p>
                <p><strong>Key Stakeholder:</strong> {strategy['Key_Stakeholder']}</p>
                <p><strong>Description:</strong> {strategy['Description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategy status visualization
    st.subheader("📊 Strategy Status Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_counts = strategy_df['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    title="Strategy Status Distribution",
                    color_discrete_map={
                        'In Progress': '#1f77b4',    # Blue
                        'Planning': '#ff7f0e',        # Orange
                        'Completed': '#2ca02c',       # Green
                        'On Hold': '#d62728'          # Red
                    })
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        priority_counts = strategy_df['Priority'].value_counts()
        fig = px.bar(x=priority_counts.index, y=priority_counts.values,
                    title="Strategy Priority Distribution",
                    color_discrete_map={
                        'High': '#d62728',        # Red
                        'Medium': '#ff7f0e',      # Orange
                        'Low': '#2ca02c',         # Green
                        'Critical': '#9467bd'     # Purple
                    })
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12)
        )
        fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
        fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#000000')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Account Analysis":
    st.subheader("📊 Account Analysis")
    
    if not api_key:
        st.warning("⚠️ API key required for account analysis. Please set up your API key first.")
    else:
        st.markdown("""
        ### AI-Powered Strategic Insights
        
        Analyze account data and generate strategic recommendations for account management and growth opportunities.
        """)
        
        # Account analysis prompt
        default_prompt = f"""
        As an ETSM, analyze these accounts and provide strategic insights:
        
        Companies: {list(usage_df['Company'].unique())}
        Usage Patterns: {usage_df.groupby('Company')['API_Calls'].apply(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]).to_dict()}
        Current Usage: {usage_df.groupby('Company')['API_Calls'].last().to_dict()}
        
        Provide strategic analysis on:
        1. **Resource Allocation**: Where to invest time and budget
        2. **Risk Management**: Which accounts need immediate attention
        3. **Growth Strategy**: Which opportunities to prioritize
        4. **Strategic Action**: Single most important next step
        5. **Timeline**: When to act (Immediate/30 days/90 days)
        
        Format as a strategic account analysis for ETSM decision-making.
        """
        
        # Prompt input
        prompt = st.text_area(
            "Account Analysis Prompt:",
            value=default_prompt,
            height=200,
            help="Customize the prompt for different account analysis scenarios"
        )
        
        # Use Claude Sonnet 4 model
        model = "claude-sonnet-4-20250514"
        
        # Generate button
        if st.button("🚀 Analyze Accounts", type="primary"):
            if prompt.strip():
                with st.spinner("Calling Anthropic API..."):
                    # Call API and capture raw response
                    import traceback
                    try:
                        api_url = "https://api.anthropic.com/v1/messages"
                        api_headers = {
                            "x-api-key": api_key,
                            "content-type": "application/json",
                            "anthropic-version": "2023-06-01"
                        }
                        api_data = {
                            "model": model,
                            "max_tokens": 1000,
                            "messages": [
                                {"role": "user", "content": prompt}
                            ]
                        }
                        api_response = requests.post(api_url, headers=api_headers, json=api_data)
                        raw_response = api_response.text
                        if api_response.status_code == 200:
                            result = api_response.json()
                            response = result['content'][0]['text']
                        else:
                            response = f"API Error: {api_response.status_code} - {api_response.text}"
                    except Exception as e:
                        response = f"Error calling API: {str(e)}\n{traceback.format_exc()}"
                        raw_response = response
                    
                    # Display results
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.markdown("### 📝 Prompt")
                        st.markdown(f"""
                        <div class="prompt-card">
                            <strong>Model:</strong> {model}<br>
                            <strong>Prompt:</strong><br>
                            {prompt}
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown("### 📊 Strategic Analysis")
                        st.markdown(f"""
                        <div class="response-card">
                            {response}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Debug info (collapsed by default)
                    with st.expander("Show raw API response (debug)"):
                        st.code(raw_response, language="json")
            else:
                st.error("Please enter a prompt before generating.")
        


elif page == "Account Overview":
    st.subheader("👥 Account Overview")
    
    # Account summary table
    account_summary = usage_df.groupby('Company').agg({
        'API_Calls': ['sum', 'mean'],
        'Revenue': 'sum',
        'Use_Cases': 'max'
    }).round(2)
    
    account_summary.columns = ['Total API Calls', 'Avg Monthly Calls', 'Total Revenue', 'Use Cases']
    account_summary = account_summary.reset_index()
    
    st.dataframe(account_summary, use_container_width=True)
    
    # Account health indicators
    st.subheader("🏥 Account Health Indicators")
    
    for company in usage_df['Company'].unique():
        company_data = usage_df[usage_df['Company'] == company]
        growth_rate = (company_data['API_Calls'].iloc[-1] - company_data['API_Calls'].iloc[0]) / company_data['API_Calls'].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"{company} - Current Usage", f"{company_data['API_Calls'].iloc[-1]:,}")
        
        with col2:
            st.metric(f"{company} - Growth Rate", f"{growth_rate:.1%}")
        
        with col3:
            if growth_rate > 0.1:
                st.success("✅ Healthy Growth")
            elif growth_rate < -0.05:
                st.error("⚠️ Declining Usage")
            else:
                st.warning("🔄 Stable Usage")



# Footer
st.markdown("---")
st.markdown("""
<div class="powered-by">
    <div style="margin-bottom: 10px;">
        <span class="claude-badge">Claude</span>
        <strong style="margin: 0 10px;">Powered by Anthropic</strong>
        <span class="claude-badge">Sonnet 4</span>
    </div>
    <p style="margin: 0; color: #6b7280;">Enterprise Technical Success Manager Dashboard</p>
    <p style="margin: 5px 0 0 0; font-size: 0.8rem; color: #6b7280;">API Usage Analytics • Strategy Boards • AI-Powered Insights • Executive Decisions</p>
</div>
""", unsafe_allow_html=True)
