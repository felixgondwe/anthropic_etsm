# Production Deployment Guide

This guide covers deploying the ETSM Dashboard to production environments with enterprise-grade reliability, security, and performance.

## 🎯 Deployment Overview

### Production Requirements
- **High Availability**: 99.9% uptime target
- **Security**: Enterprise-grade security measures
- **Performance**: Sub-3-second page load times
- **Scalability**: Support for 100+ concurrent users
- **Monitoring**: Comprehensive observability

## 🏗️ Infrastructure Options

### Option 1: Streamlit Cloud (Recommended)

#### Prerequisites
- GitHub repository with application code
- Anthropic API key
- Domain name (optional)

#### Deployment Steps

1. **Prepare Repository**
   ```bash
   # Ensure all files are committed
   git add .
   git commit -m "Production deployment ready"
   git push origin main
   ```

2. **Configure Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub account
   - Click "New app"
   - Configure settings:
     - **Repository**: Select your repository
     - **Branch**: `main`
     - **Main file path**: `src/dashboard.py`
     - **Python version**: 3.11

3. **Set Environment Variables**
   ```
   ANTHROPIC_API_KEY=your_production_api_key
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=0.0.0.0
   ```

4. **Advanced Configuration**
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

#### Production Checklist
- [ ] Repository is public or connected to Streamlit Cloud
- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables configured
- [ ] Custom domain configured (optional)
- [ ] SSL certificate enabled
- [ ] Monitoring alerts set up

### Option 2: Railway

#### Prerequisites
- Railway account
- GitHub repository
- Anthropic API key

#### Deployment Steps

1. **Connect Repository**
   - Visit [railway.app](https://railway.app)
   - Connect GitHub account
   - Select repository

2. **Configure Service**
   ```json
   {
     "buildCommand": "pip install -r requirements.txt",
     "startCommand": "streamlit run src/dashboard.py --server.port $PORT --server.address 0.0.0.0",
     "healthcheckPath": "/",
     "healthcheckTimeout": 300
   }
   ```

3. **Set Environment Variables**
   ```
   ANTHROPIC_API_KEY=your_production_api_key
   PORT=8501
   ```

4. **Deploy**
   - Railway automatically detects changes
   - Deploys on every push to main branch
   - Provides custom domain

### Option 3: Render

#### Prerequisites
- Render account
- GitHub repository
- Anthropic API key

#### Deployment Steps

1. **Create Web Service**
   - Visit [render.com](https://render.com)
   - Create new Web Service
   - Connect GitHub repository

2. **Configure Build**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run src/dashboard.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment**: Python 3.11

3. **Set Environment Variables**
   ```
   ANTHROPIC_API_KEY=your_production_api_key
   PORT=8501
   ```

4. **Deploy**
   - Automatic deployment on push
   - Custom domain support
   - SSL certificate included

### Option 4: Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed
- GitHub repository

#### Deployment Steps

1. **Create Heroku App**
   ```bash
   heroku create your-etsm-dashboard
   ```

2. **Configure Buildpacks**
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set ANTHROPIC_API_KEY=your_production_api_key
   heroku config:set STREAMLIT_SERVER_PORT=$PORT
   heroku config:set STREAMLIT_SERVER_ADDRESS=0.0.0.0
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

## 🔒 Security Configuration

### Environment Variables
```bash
# Required
ANTHROPIC_API_KEY=your_production_api_key

# Optional but recommended
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

### Security Best Practices
1. **API Key Management**
   - Use environment variables only
   - Rotate keys regularly
   - Monitor usage patterns

2. **Network Security**
   - Enable HTTPS/TLS
   - Configure CORS properly
   - Use secure headers

3. **Application Security**
   - Input validation
   - Output encoding
   - Rate limiting

## 📊 Monitoring & Observability

### Application Monitoring
```python
# Add to dashboard.py for monitoring
import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

### Health Checks
```python
# Add health check endpoint
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

### Performance Metrics
- **Response Time**: < 3 seconds
- **Error Rate**: < 1%
- **Availability**: > 99.9%
- **Memory Usage**: < 512MB
- **CPU Usage**: < 80%

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Streamlit Cloud
        run: |
          # Deployment logic here
          echo "Deployment completed"
```

## 🚀 Performance Optimization

### Code Optimization
```python
# Use caching for expensive operations
@st.cache_data(ttl=3600)
def load_expensive_data():
    # Expensive data loading
    pass

# Optimize data processing
def optimize_dataframe(df):
    # Use appropriate dtypes
    # Remove unnecessary columns
    # Use efficient operations
    return df
```

### Configuration Optimization
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false
```

## 🔧 Troubleshooting

### Common Issues

1. **Application Won't Start**
   ```bash
   # Check logs
   heroku logs --tail
   
   # Verify environment variables
   heroku config
   ```

2. **API Key Issues**
   ```bash
   # Test API connection
   curl -H "x-api-key: $ANTHROPIC_API_KEY" \
        https://api.anthropic.com/v1/messages
   ```

3. **Performance Issues**
   - Check memory usage
   - Monitor API call frequency
   - Review caching strategy

### Debug Commands
```bash
# Local testing
streamlit run src/dashboard.py --server.port 8501

# Check dependencies
pip list

# Test API connection
python -c "import requests; print(requests.get('https://api.anthropic.com/v1/models').status_code)"
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement session management
- Consider database scaling

### Vertical Scaling
- Increase memory allocation
- Optimize CPU usage
- Monitor resource utilization

### Cost Optimization
- Monitor API usage
- Implement caching
- Use appropriate instance sizes

## 🔄 Maintenance

### Regular Tasks
- **Weekly**: Review performance metrics
- **Monthly**: Update dependencies
- **Quarterly**: Security audit
- **Annually**: Architecture review

### Backup Strategy
- **Code**: Git repository
- **Configuration**: Environment variables
- **Data**: Export functionality (if applicable)

---

*For development setup, see the [Development Guide](development.md).* 