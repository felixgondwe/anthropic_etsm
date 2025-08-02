# Common Issues & Troubleshooting

This guide covers the most common issues encountered when using the ETSM Dashboard and provides step-by-step solutions.

## 🚨 Critical Issues

### Application Won't Start

#### Symptoms
- Dashboard fails to load
- Error messages in console
- Blank screen or timeout

#### Solutions

**1. Check Environment Variables**
```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Check all environment variables
env | grep STREAMLIT
```

**2. Verify Dependencies**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check for version conflicts
pip list | grep streamlit
```

**3. Check Port Availability**
```bash
# Check if port 8501 is available
lsof -i :8501

# Kill process if needed
kill -9 $(lsof -t -i:8501)
```

**4. Debug Mode**
```bash
# Run with debug information
streamlit run src/dashboard.py --logger.level debug
```

### API Connection Issues

#### Symptoms
- "API key not configured" error
- Timeout errors
- Rate limit exceeded messages

#### Solutions

**1. Verify API Key**
```python
# Test API key validity
import requests

def test_api_key():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return "API key not found"
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.anthropic.com/v1/models",
            headers=headers,
            timeout=10
        )
        return f"Status: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**2. Check Network Connectivity**
```bash
# Test API endpoint
curl -H "x-api-key: $ANTHROPIC_API_KEY" \
     https://api.anthropic.com/v1/models

# Check DNS resolution
nslookup api.anthropic.com
```

**3. Rate Limiting**
```python
# Implement exponential backoff
import time
import random

def api_call_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = call_anthropic_api(prompt)
            return response
        except Exception as e:
            if "rate limit" in str(e).lower():
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            else:
                raise e
    raise Exception("Max retries exceeded")
```

## ⚠️ Performance Issues

### Slow Loading Times

#### Symptoms
- Dashboard takes >10 seconds to load
- Charts render slowly
- Data processing delays

#### Solutions

**1. Optimize Data Processing**
```python
# Use caching for expensive operations
@st.cache_data(ttl=3600)
def load_usage_data():
    # Expensive data loading
    return data

# Optimize DataFrame operations
def optimize_dataframe(df):
    # Use appropriate dtypes
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('category')
    
    # Remove unnecessary columns
    df = df.dropna(how='all')
    
    return df
```

**2. Reduce API Calls**
```python
# Cache API responses
@st.cache_data(ttl=1800)
def cached_api_call(prompt):
    return call_anthropic_api(prompt)

# Batch API calls
def batch_api_calls(prompts):
    results = []
    for prompt in prompts:
        results.append(cached_api_call(prompt))
    return results
```

**3. Optimize Charts**
```python
# Use efficient chart configurations
def create_optimized_chart(data):
    fig = px.line(
        data,
        x='date',
        y='value',
        render_mode='svg',  # Faster rendering
        height=400
    )
    return fig
```

### Memory Issues

#### Symptoms
- Application crashes
- High memory usage
- Slow performance

#### Solutions

**1. Monitor Memory Usage**
```python
import psutil
import gc

def monitor_memory():
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    st.write(f"Memory usage: {memory_mb:.2f} MB")
    
    if memory_mb > 500:  # 500MB threshold
        gc.collect()  # Force garbage collection
```

**2. Optimize Data Storage**
```python
# Use efficient data types
def optimize_data_types(df):
    # Convert to smaller dtypes
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('category')
        elif df[col].dtype == 'float64':
            df[col] = df[col].astype('float32')
    
    return df
```

## 🔧 Configuration Issues

### Environment Variables Not Loading

#### Symptoms
- "API key not configured" errors
- Missing configuration values
- Default values being used

#### Solutions

**1. Check .env File**
```bash
# Verify .env file exists
ls -la .env

# Check file contents (without exposing secrets)
head -n 1 .env
```

**2. Load Environment Variables**
```python
# Force reload environment variables
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Verify loading
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    st.success("API key loaded successfully")
else:
    st.error("API key not found")
```

**3. Production Environment**
```bash
# Set environment variables directly
export ANTHROPIC_API_KEY=your_key_here
export STREAMLIT_SERVER_PORT=8501

# Verify in application
echo $ANTHROPIC_API_KEY
```

### Configuration File Issues

#### Symptoms
- Custom themes not applied
- Server settings ignored
- Browser behavior unexpected

#### Solutions

**1. Verify Config File**
```toml
# .streamlit/config.toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

**2. Check File Location**
```bash
# Verify config file location
find . -name "config.toml"

# Check file permissions
ls -la .streamlit/config.toml
```

## 📊 Data Issues

### Missing or Incorrect Data

#### Symptoms
- Empty charts
- Incorrect calculations
- Missing data points

#### Solutions

**1. Validate Data Sources**
```python
def validate_data(data):
    """Validate data integrity"""
    if data is None or data.empty:
        st.error("No data available")
        return False
    
    # Check for required columns
    required_columns = ['date', 'value', 'account_id']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        return False
    
    return True
```

**2. Handle Missing Data**
```python
def handle_missing_data(df):
    """Handle missing data gracefully"""
    # Fill missing values
    df = df.fillna(0)
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Interpolate time series data
    if 'date' in df.columns:
        df = df.sort_values('date')
        df = df.interpolate(method='time')
    
    return df
```

**3. Data Refresh**
```python
# Force data refresh
if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()
```

### Chart Rendering Issues

#### Symptoms
- Charts not displaying
- Incorrect chart types
- Missing data points

#### Solutions

**1. Debug Chart Data**
```python
def debug_chart_data(data):
    """Debug chart data issues"""
    st.write("Data shape:", data.shape)
    st.write("Data columns:", data.columns.tolist())
    st.write("Data types:", data.dtypes.to_dict())
    st.write("Sample data:", data.head())
```

**2. Handle Empty Data**
```python
def create_chart_safely(data, chart_type='line'):
    """Create chart with error handling"""
    if data is None or data.empty:
        st.warning("No data available for chart")
        return None
    
    try:
        if chart_type == 'line':
            fig = px.line(data, x='date', y='value')
        elif chart_type == 'bar':
            fig = px.bar(data, x='category', y='value')
        
        return fig
    except Exception as e:
        st.error(f"Chart creation failed: {str(e)}")
        return None
```

## 🔐 Security Issues

### Authentication Problems

#### Symptoms
- Access denied errors
- Session timeout issues
- Permission errors

#### Solutions

**1. Check API Key Permissions**
```python
def verify_api_permissions():
    """Verify API key has required permissions"""
    try:
        response = call_anthropic_api("Test message")
        return True
    except Exception as e:
        if "unauthorized" in str(e).lower():
            st.error("API key is invalid or expired")
        elif "rate limit" in str(e).lower():
            st.error("Rate limit exceeded")
        else:
            st.error(f"API error: {str(e)}")
        return False
```

**2. Session Management**
```python
def check_session_validity():
    """Check if user session is valid"""
    # In production, implement proper session checking
    session_id = st.session_state.get('session_id')
    if not session_id:
        st.error("Session expired. Please refresh the page.")
        return False
    return True
```

## 🌐 Network Issues

### Connection Problems

#### Symptoms
- Network timeout errors
- Slow response times
- Connection refused errors

#### Solutions

**1. Network Diagnostics**
```python
import socket
import requests

def test_network_connectivity():
    """Test network connectivity"""
    tests = {
        "DNS Resolution": lambda: socket.gethostbyname("api.anthropic.com"),
        "HTTPS Connection": lambda: requests.get("https://api.anthropic.com", timeout=5),
        "API Endpoint": lambda: requests.get("https://api.anthropic.com/v1/models", timeout=5)
    }
    
    results = {}
    for test_name, test_func in tests.items():
        try:
            result = test_func()
            results[test_name] = "PASS"
        except Exception as e:
            results[test_name] = f"FAIL: {str(e)}"
    
    return results
```

**2. Proxy Configuration**
```python
# Configure proxy if needed
proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}

def api_call_with_proxy(prompt):
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data,
        proxies=proxies,
        timeout=30
    )
    return response
```

## 📱 Browser Issues

### Compatibility Problems

#### Symptoms
- Features not working in certain browsers
- Layout issues
- JavaScript errors

#### Solutions

**1. Browser Detection**
```python
def check_browser_compatibility():
    """Check browser compatibility"""
    user_agent = st.get_user_agent()
    
    supported_browsers = [
        'Chrome', 'Firefox', 'Safari', 'Edge'
    ]
    
    for browser in supported_browsers:
        if browser in user_agent:
            return True
    
    st.warning("Browser not fully supported. Please use Chrome, Firefox, Safari, or Edge.")
    return False
```

**2. Mobile Optimization**
```python
def optimize_for_mobile():
    """Optimize layout for mobile devices"""
    # Check if mobile device
    user_agent = st.get_user_agent()
    is_mobile = any(device in user_agent.lower() for device in ['mobile', 'android', 'iphone'])
    
    if is_mobile:
        st.markdown("""
        <style>
        .stApp {
            max-width: 100%;
            padding: 0;
        }
        </style>
        """, unsafe_allow_html=True)
```

## 🔄 Deployment Issues

### Production Deployment Problems

#### Symptoms
- App not accessible after deployment
- Environment variables not set
- Build failures

#### Solutions

**1. Deployment Checklist**
```bash
# Pre-deployment checklist
echo "Checking deployment readiness..."

# Check all files are committed
git status

# Verify requirements.txt is up to date
pip freeze > requirements.txt

# Test locally
streamlit run src/dashboard.py --server.port 8501

# Check environment variables
echo $ANTHROPIC_API_KEY
```

**2. Platform-Specific Issues**

**Streamlit Cloud:**
```bash
# Check deployment logs
# Visit share.streamlit.io and check app logs

# Verify repository connection
# Ensure repository is public or connected to Streamlit Cloud
```

**Railway:**
```bash
# Check Railway logs
railway logs

# Verify environment variables
railway variables
```

**Render:**
```bash
# Check build logs
# Visit render.com dashboard

# Verify build configuration
# Check build command and start command
```

## 📞 Getting Help

### Debug Information
```python
def generate_debug_info():
    """Generate debug information for support"""
    debug_info = {
        "streamlit_version": st.__version__,
        "python_version": sys.version,
        "platform": platform.platform(),
        "api_key_configured": bool(os.getenv('ANTHROPIC_API_KEY')),
        "session_state": dict(st.session_state),
        "user_agent": st.get_user_agent()
    }
    
    return debug_info
```

### Support Resources
- **Documentation**: Check the [main documentation](../README.md)
- **GitHub Issues**: Report bugs via GitHub
- **Community**: Ask questions in community forums
- **Technical Support**: Contact the development team

### Escalation Process
1. **Check this guide** for common solutions
2. **Search existing issues** for similar problems
3. **Create detailed bug report** with debug information
4. **Contact support** with specific error details

---

*For more detailed troubleshooting, see the [Error Codes](error-codes.md) reference.* 