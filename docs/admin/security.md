# Security Guide

This guide covers security best practices, configuration, and monitoring for the ETSM Dashboard in production environments, embodying Anthropic's commitment to safety and our values.

## 🔒 Security Overview

### Security Principles Aligned with Our Values
- **Act for the global good**: Security measures that protect humanity's interests
- **Hold light and shade**: Comprehensive risk assessment with opportunity recognition
- **Ignite a race to the top on safety**: Industry-leading security practices
- **Be helpful, honest, and harmless**: Transparent security with harm prevention
- **Put the mission first**: Security that serves our core mission

### Security Framework
```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│ 🌐 Network Security │ 🔐 Application Security │ 📊 Data Security │
│                     │                        │                 │
│ 🔑 Access Control   │ 🛡️ Threat Protection   │ 🔒 Privacy       │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 Network Security

### HTTPS/TLS Configuration
```toml
# .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### Security Headers
```python
# Add security headers
import streamlit as st

# Security headers configuration
st.set_page_config(
    page_title="ETSM Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom security headers
st.markdown("""
<style>
    /* Security-focused CSS */
    .stApp {
        /* Prevent clickjacking */
        position: relative;
    }
</style>
""")
```

### CORS Configuration
```python
# Configure CORS for production
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://app.streamlit.io"
]

CORS_ALLOWED_METHODS = ["GET", "POST"]
CORS_ALLOWED_HEADERS = ["Content-Type", "Authorization"]
```

## 🔐 Application Security

### API Key Management

#### Environment Variables
```bash
# Production environment variables
ANTHROPIC_API_KEY=your_production_api_key
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

#### Secure API Key Handling
```python
import os
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()

# Validate API key presence
def validate_api_key():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("API key not configured. Please set ANTHROPIC_API_KEY environment variable.")
        st.stop()
    return api_key

# Secure API calls
def secure_api_call(prompt, model="claude-sonnet-4-20250514"):
    api_key = validate_api_key()
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Add rate limiting
    if not check_rate_limit():
        st.error("Rate limit exceeded. Please try again later.")
        return None
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json={
                "model": model,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        return response.json()
    except Exception as e:
        st.error(f"API call failed: {str(e)}")
        return None
```

### Input Validation
```python
import re
from typing import Optional

def validate_input(input_text: str) -> Optional[str]:
    """Validate user input for security - embodying 'be helpful, honest, and harmless'"""
    
    # Check for SQL injection patterns
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)",
        r"(\b(UNION|EXEC|EXECUTE|SCRIPT)\b)",
        r"(--|/\*|\*/|xp_)",
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return "Invalid input detected"
    
    # Check for XSS patterns
    xss_patterns = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
    ]
    
    for pattern in xss_patterns:
        if re.search(pattern, input_text, re.IGNORECASE):
            return "Invalid input detected"
    
    # Check length limits
    if len(input_text) > 10000:
        return "Input too long"
    
    return None

def sanitize_output(text: str) -> str:
    """Sanitize output to prevent XSS - ensuring we're harmless"""
    import html
    
    # HTML encode special characters
    text = html.escape(text)
    
    # Remove any remaining script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE)
    
    return text
```

### Session Management
```python
import hashlib
import time
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id: str) -> str:
        """Create a secure session"""
        session_id = hashlib.sha256(
            f"{user_id}{time.time()}{os.urandom(16)}".encode()
        ).hexdigest()
        
        self.sessions[session_id] = {
            "user_id": user_id,
            "created": datetime.now(),
            "last_activity": datetime.now(),
            "expires": datetime.now() + timedelta(hours=8)
        }
        
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        """Validate session and update activity"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        
        # Check expiration
        if datetime.now() > session["expires"]:
            del self.sessions[session_id]
            return False
        
        # Update last activity
        session["last_activity"] = datetime.now()
        return True
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if current_time > session["expires"]
        ]
        
        for sid in expired_sessions:
            del self.sessions[sid]

# Initialize session manager
session_manager = SessionManager()
```

## 🛡️ Threat Protection

### Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        current_time = time.time()
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < self.window_seconds
        ]
        
        # Check rate limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(current_time)
        return True

# Initialize rate limiter
rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)

def check_rate_limit() -> bool:
    """Check if current request is within rate limits"""
    # Use IP address or session ID as identifier
    identifier = "default"  # In production, use actual IP or session
    return rate_limiter.is_allowed(identifier)
```

### DDoS Protection
```python
def detect_ddos(ip_address: str, request_count: int) -> bool:
    """Detect potential DDoS attacks - protecting against harm"""
    
    # Simple DDoS detection
    if request_count > 1000:  # More than 1000 requests per minute
        return True
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r"\.\./",  # Directory traversal
        r"<script",  # XSS attempts
        r"union\s+select",  # SQL injection
    ]
    
    return False  # Implement actual detection logic
```

### Logging and Monitoring
```python
import logging
from datetime import datetime

# Configure security logging
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler('security.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

# Add handler to logger
security_logger.addHandler(file_handler)

def log_security_event(event_type: str, details: dict):
    """Log security events - being honest about our security posture"""
    security_logger.info(f"SECURITY_EVENT: {event_type} - {details}")

def log_api_call(api_endpoint: str, success: bool, error_message: str = None):
    """Log API calls for security monitoring"""
    details = {
        "endpoint": api_endpoint,
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "user_agent": st.get_user_agent(),
        "ip_address": "client_ip"  # In production, get actual IP
    }
    
    if error_message:
        details["error"] = error_message
    
    log_security_event("API_CALL", details)
```

## 📊 Data Security

### Data Encryption
```python
from cryptography.fernet import Fernet
import base64

class DataEncryption:
    def __init__(self):
        # In production, use environment variable for key
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()

# Initialize encryption
data_encryption = DataEncryption()
```

### Data Sanitization
```python
def sanitize_data(data: dict) -> dict:
    """Sanitize data before storage or transmission - ensuring harm prevention"""
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potentially dangerous characters
            sanitized[key] = re.sub(r'[<>"\']', '', value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_data(value)
        else:
            sanitized[key] = value
    
    return sanitized
```

### Privacy Compliance
```python
class PrivacyCompliance:
    def __init__(self):
        self.data_retention_days = 90
        self.pii_fields = ['email', 'phone', 'address']
    
    def mask_pii(self, data: dict) -> dict:
        """Mask personally identifiable information - protecting user privacy"""
        masked_data = data.copy()
        
        for field in self.pii_fields:
            if field in masked_data:
                value = masked_data[field]
                if isinstance(value, str) and len(value) > 2:
                    masked_data[field] = value[0] + '*' * (len(value) - 2) + value[-1]
        
        return masked_data
    
    def anonymize_data(self, data: dict) -> dict:
        """Anonymize data for analytics"""
        # Remove or hash identifying information
        anonymized = data.copy()
        
        # Hash user identifiers
        if 'user_id' in anonymized:
            anonymized['user_id'] = hashlib.sha256(
                anonymized['user_id'].encode()
            ).hexdigest()[:8]
        
        return anonymized

# Initialize privacy compliance
privacy_compliance = PrivacyCompliance()
```

## 🔑 Access Control

### Authentication
```python
import hashlib
import secrets

class Authentication:
    def __init__(self):
        self.users = {}  # In production, use database
        self.salt = secrets.token_hex(16)
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        return hashlib.sha256(
            (password + self.salt).encode()
        ).hexdigest()
    
    def verify_password(self, username: str, password: str) -> bool:
        """Verify user password"""
        if username not in self.users:
            return False
        
        stored_hash = self.users[username]['password_hash']
        input_hash = self.hash_password(password)
        
        return stored_hash == input_hash
    
    def create_user(self, username: str, password: str, role: str = 'user'):
        """Create new user account"""
        password_hash = self.hash_password(password)
        
        self.users[username] = {
            'password_hash': password_hash,
            'role': role,
            'created': datetime.now(),
            'last_login': None
        }

# Initialize authentication
auth = Authentication()
```

### Authorization
```python
from enum import Enum
from typing import List

class Permission(Enum):
    READ_DASHBOARD = "read_dashboard"
    WRITE_STRATEGY = "write_strategy"
    ADMIN_USERS = "admin_users"
    EXPORT_DATA = "export_data"

class Authorization:
    def __init__(self):
        self.role_permissions = {
            'admin': [perm.value for perm in Permission],
            'manager': [
                Permission.READ_DASHBOARD.value,
                Permission.WRITE_STRATEGY.value,
                Permission.EXPORT_DATA.value
            ],
            'user': [
                Permission.READ_DASHBOARD.value
            ]
        }
    
    def has_permission(self, username: str, permission: str) -> bool:
        """Check if user has specific permission"""
        if username not in auth.users:
            return False
        
        user_role = auth.users[username]['role']
        user_permissions = self.role_permissions.get(user_role, [])
        
        return permission in user_permissions
    
    def require_permission(self, permission: str):
        """Decorator to require specific permission"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # In production, get current user from session
                current_user = "current_user"  # Get from session
                
                if not self.has_permission(current_user, permission):
                    st.error("Access denied. Insufficient permissions.")
                    return None
                
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Initialize authorization
authorization = Authorization()
```

## 📈 Security Monitoring

### Security Metrics
```python
class SecurityMetrics:
    def __init__(self):
        self.metrics = {
            'failed_logins': 0,
            'api_errors': 0,
            'suspicious_requests': 0,
            'data_exports': 0
        }
    
    def increment_metric(self, metric: str):
        """Increment security metric"""
        if metric in self.metrics:
            self.metrics[metric] += 1
    
    def get_security_report(self) -> dict:
        """Generate security report - being honest about our security posture"""
        return {
            'metrics': self.metrics,
            'timestamp': datetime.now().isoformat(),
            'alerts': self.check_alerts()
        }
    
    def check_alerts(self) -> List[str]:
        """Check for security alerts"""
        alerts = []
        
        if self.metrics['failed_logins'] > 10:
            alerts.append("High number of failed login attempts")
        
        if self.metrics['api_errors'] > 50:
            alerts.append("High number of API errors")
        
        if self.metrics['suspicious_requests'] > 5:
            alerts.append("Suspicious activity detected")
        
        return alerts

# Initialize security metrics
security_metrics = SecurityMetrics()
```

### Incident Response
```python
class IncidentResponse:
    def __init__(self):
        self.incidents = []
    
    def report_incident(self, incident_type: str, details: dict):
        """Report security incident - being honest about security events"""
        incident = {
            'type': incident_type,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'status': 'open'
        }
        
        self.incidents.append(incident)
        
        # Log incident
        log_security_event("INCIDENT", incident)
        
        # Send alert if critical
        if incident_type in ['data_breach', 'unauthorized_access']:
            self.send_alert(incident)
    
    def send_alert(self, incident: dict):
        """Send security alert"""
        # In production, send email/SMS alert
        st.error(f"SECURITY ALERT: {incident['type']}")
    
    def get_incident_report(self) -> dict:
        """Generate incident report"""
        return {
            'total_incidents': len(self.incidents),
            'open_incidents': len([i for i in self.incidents if i['status'] == 'open']),
            'recent_incidents': self.incidents[-10:] if self.incidents else []
        }

# Initialize incident response
incident_response = IncidentResponse()
```

## 🔄 Security Maintenance

### Regular Security Tasks
```python
def security_maintenance():
    """Perform regular security maintenance - putting the mission first"""
    
    # Clean up expired sessions
    session_manager.cleanup_expired_sessions()
    
    # Rotate API keys (if needed)
    # rotate_api_keys()
    
    # Update security metrics
    security_metrics.get_security_report()
    
    # Check for security incidents
    incident_response.get_incident_report()
    
    # Log maintenance completion
    log_security_event("MAINTENANCE", {"status": "completed"})

# Schedule security maintenance
# In production, use cron job or scheduler
```

### Security Checklist Aligned with Our Values
- [ ] **Act for the global good**: API Keys rotated regularly, environment variables used
- [ ] **Hold light and shade**: HTTPS enabled, input validation implemented
- [ ] **Be good to our users**: Output encoding to prevent XSS, secure session handling
- [ ] **Ignite a race to the top on safety**: Rate limiting prevents abuse and DDoS attacks
- [ ] **Do the simple thing that works**: Comprehensive security event logging
- [ ] **Be helpful, honest, and harmless**: Real-time security monitoring
- [ ] **Put the mission first**: Incident response plan for security incidents

---

*For deployment security, see the [Deployment Guide](../technical/deployment.md).* 