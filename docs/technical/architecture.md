# System Architecture

## Overview

The ETSM Dashboard is a modern web application built with Streamlit, designed to provide Enterprise Technical Success Managers with comprehensive insights into API usage, account health, and strategic opportunities.

## 🏗️ High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Streamlit     │    │   Anthropic     │
│                 │◄──►│   Application   │◄──►│   API           │
│   (Frontend)    │    │   (Backend)     │    │   (External)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Data Layer    │
                       │   (In-Memory)   │
                       └─────────────────┘
```

## 🧩 Component Architecture

### 1. Frontend Layer
- **Technology**: Streamlit Web Framework
- **UI Components**: Custom Streamlit components and Plotly visualizations
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Automatic data refresh and live updates

### 2. Backend Layer
- **Application Server**: Streamlit Runtime
- **Business Logic**: Python-based analytics and data processing
- **API Integration**: Anthropic API client for AI insights
- **Data Processing**: Pandas and NumPy for analytics

### 3. Data Layer
- **Data Sources**: 
  - Anthropic API (real-time)
  - Simulated data (for demonstration)
  - User-generated content
- **Data Processing**: In-memory data manipulation
- **Caching**: Streamlit session state management

### 4. External Integrations
- **Anthropic API**: AI-powered insights and recommendations
- **Authentication**: Environment-based API key management
- **Monitoring**: Application performance tracking

## 🔄 Data Flow

### 1. User Interaction Flow
```
User Action → Streamlit Event → Business Logic → Data Processing → UI Update
```

### 2. API Integration Flow
```
Dashboard Request → API Client → Anthropic API → Response Processing → UI Update
```

### 3. Data Processing Flow
```
Raw Data → Validation → Transformation → Analytics → Visualization
```

## 📊 Data Architecture

### Data Models

#### Account Data
```python
{
    "account_id": "string",
    "name": "string",
    "health_score": "float",
    "growth_rate": "float",
    "usage_trends": "array",
    "risk_factors": "array"
}
```

#### API Usage Data
```python
{
    "timestamp": "datetime",
    "account_id": "string",
    "api_calls": "integer",
    "tokens_used": "integer",
    "cost": "float",
    "endpoint": "string"
}
```

#### Strategy Data
```python
{
    "initiative_id": "string",
    "account_id": "string",
    "title": "string",
    "priority": "string",
    "status": "string",
    "expected_revenue": "float",
    "timeline": "date"
}
```

## 🔧 Technical Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit 1.28+**: Web application framework
- **Pandas 2.0+**: Data manipulation and analysis
- **Plotly 5.15+**: Interactive visualizations
- **NumPy 1.24+**: Numerical computing

### Development Tools
- **Git**: Version control
- **Make**: Build automation
- **Pytest**: Testing framework
- **Black**: Code formatting
- **Flake8**: Linting

### Production Dependencies
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment variable management
- **Streamlit-aggrid**: Advanced data grid
- **Streamlit-option-menu**: Navigation components

## 🚀 Performance Characteristics

### Scalability
- **Horizontal Scaling**: Stateless application design
- **Caching Strategy**: Session-based data caching
- **API Rate Limiting**: Configurable request throttling
- **Memory Management**: Efficient data processing

### Performance Metrics
- **Page Load Time**: < 3 seconds
- **API Response Time**: < 2 seconds
- **Concurrent Users**: 50+ simultaneous users
- **Data Processing**: Real-time analytics

## 🔒 Security Architecture

### Authentication & Authorization
- **API Key Management**: Environment-based secrets
- **Input Validation**: Comprehensive data sanitization
- **Output Encoding**: XSS prevention
- **Session Management**: Secure session handling

### Data Protection
- **Encryption**: HTTPS/TLS for data in transit
- **Sensitive Data**: Environment variable protection
- **Audit Logging**: User action tracking
- **Compliance**: GDPR and SOC2 considerations

## 📈 Monitoring & Observability

### Application Monitoring
- **Health Checks**: Application status monitoring
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Exception monitoring
- **Usage Analytics**: User behavior tracking

### Infrastructure Monitoring
- **Resource Utilization**: CPU, memory, disk usage
- **Network Performance**: Bandwidth and latency
- **Availability**: Uptime monitoring
- **Security Events**: Intrusion detection

## 🔄 Deployment Architecture

### Development Environment
```
Local Development → Git Repository → CI/CD Pipeline → Staging → Production
```

### Production Environment
- **Web Server**: Streamlit Cloud / Railway / Render
- **Database**: In-memory (stateless design)
- **CDN**: Static asset delivery
- **Load Balancer**: Traffic distribution

## 🛠️ Development Workflow

### Code Organization
```
src/
├── dashboard.py          # Main application
├── components/          # Reusable UI components
├── utils/              # Utility functions
└── data/              # Data processing modules

tests/
├── test_dashboard.py   # Application tests
└── test_utils.py      # Utility tests

docs/                  # Documentation
admin/                 # Administrative guides
```

### Development Process
1. **Feature Development**: Branch-based development
2. **Code Review**: Pull request workflow
3. **Testing**: Automated test suite
4. **Deployment**: CI/CD pipeline
5. **Monitoring**: Production monitoring

## 🔮 Future Architecture Considerations

### Planned Enhancements
- **Database Integration**: Persistent data storage
- **User Authentication**: Multi-user support
- **Real-time Updates**: WebSocket integration
- **Advanced Analytics**: Machine learning integration
- **Mobile App**: Native mobile application

### Scalability Roadmap
- **Microservices**: Service decomposition
- **Containerization**: Docker deployment
- **Cloud Native**: Kubernetes orchestration
- **Event-Driven**: Message queue integration

---

*For detailed deployment instructions, see the [Deployment Guide](deployment.md).* 