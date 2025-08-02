# Quick Start Guide

Welcome to the ETSM Dashboard! This guide will get you up and running in under 10 minutes.

## 🎯 What You'll Learn

- Setting up your environment
- Running the dashboard locally
- Understanding the main features
- Making your first API call

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Anthropic API Key** from [console.anthropic.com](https://console.anthropic.com/)
- **Git** (for version control)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🚀 Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-org/etsm-dashboard.git
cd etsm-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔑 Step 2: Configure API Key

Create a `.env` file in the root directory:

```bash
# Create environment file
touch .env
```

Add your API key to `.env`:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

**⚠️ Security Note**: Never commit your `.env` file to version control. It's already in `.gitignore`.

## 🏃‍♂️ Step 3: Launch the Dashboard

```bash
# Start the application
streamlit run src/dashboard.py
```

The dashboard will open automatically at `http://localhost:8501`

## 📊 Step 4: Explore the Dashboard

### Main Sections

1. **API Usage Analytics**
   - View real-time API consumption
   - Track growth trends
   - Monitor account health

2. **Strategy Boards**
   - Manage expansion opportunities
   - Track strategic initiatives
   - Monitor pipeline revenue

3. **AI Insights**
   - Get intelligent recommendations
   - View risk assessments
   - Access strategic insights

4. **Account Overview**
   - Multi-dimensional health assessment
   - Growth trend analysis
   - Performance indicators

## 🎯 Step 5: Make Your First API Call

1. Navigate to the **AI Insights** section
2. Click on **"Generate Strategic Insights"**
3. Select an account from the dropdown
4. Click **"Generate"** to see AI-powered recommendations

## 🔧 Step 6: Customize Your Experience

### Personalize Dashboard

- **Date Range**: Adjust the time period for analytics
- **Account Filter**: Focus on specific accounts
- **Metrics**: Choose which KPIs to display

### Configure Alerts

- Set up usage thresholds
- Configure growth alerts
- Enable risk notifications

## 📈 Step 7: Production Deployment

Ready to deploy? Follow the [Deployment Guide](../technical/deployment.md) for production setup.

## 🆘 Need Help?

- **Documentation**: Browse the full [documentation index](../README.md)
- **Issues**: Check [Common Issues](../troubleshooting/common-issues.md)
- **Support**: Contact the development team

## 🎉 Congratulations!

You're now ready to use the ETSM Dashboard! 

**Next Steps:**
- Read the [Dashboard Overview](../user-guides/dashboard-overview.md)
- Explore [API Analytics](../user-guides/api-analytics.md)
- Set up [Monitoring](../admin/monitoring.md) for production

---

*Need more detailed information? Check out the [Installation Guide](installation.md) for advanced setup options.* 