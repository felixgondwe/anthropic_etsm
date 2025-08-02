# 🚀 Deployment Guide

## Option 1: Streamlit Cloud (Recommended)

### Steps:
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set the path to: `src/dashboard.py`
   - Add your environment variables:
     - `ANTHROPIC_API_KEY`: Your API key
   - Click "Deploy"

### Pros:
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built for Streamlit apps
- ✅ Easy environment variable management
- ✅ Custom domains supported

---

## Option 2: Railway

### Steps:
1. **Create Railway account** at [railway.app](https://railway.app)
2. **Connect GitHub repository**
3. **Add environment variables**:
   - `ANTHROPIC_API_KEY`: Your API key
4. **Deploy automatically**

### Pros:
- ✅ Generous free tier
- ✅ Automatic deployments
- ✅ Easy scaling

---

## Option 3: Render

### Steps:
1. **Create Render account** at [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect GitHub repository**
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run src/dashboard.py --server.port $PORT --server.address 0.0.0.0`
5. **Add environment variables**:
   - `ANTHROPIC_API_KEY`: Your API key

### Pros:
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Custom domains

---

## Option 4: Heroku

### Steps:
1. **Install Heroku CLI**
2. **Create Procfile**:
   ```
   web: streamlit run src/dashboard.py --server.port $PORT --server.address 0.0.0.0
   ```
3. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set ANTHROPIC_API_KEY=your_api_key
   git push heroku main
   ```

### Pros:
- ✅ Reliable and well-established
- ✅ Good documentation
- ✅ Custom domains

---

## Option 5: DigitalOcean App Platform

### Steps:
1. **Create DigitalOcean account**
2. **Create new App**
3. **Connect GitHub repository**
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `streamlit run src/dashboard.py --server.port $PORT --server.address 0.0.0.0`
5. **Add environment variables**

### Pros:
- ✅ Reliable infrastructure
- ✅ Good performance
- ✅ Custom domains

---

## Environment Variables Setup

For all platforms, you'll need to set:
- `ANTHROPIC_API_KEY`: Your Anthropic API key

## Security Considerations

1. **Never commit API keys** to your repository
2. **Use environment variables** for sensitive data
3. **Consider rate limiting** for API calls
4. **Monitor usage** to avoid unexpected costs

## Custom Domain Setup

Most platforms support custom domains:
1. **Add custom domain** in platform settings
2. **Update DNS records** to point to your app
3. **Configure SSL certificate** (usually automatic)

## Monitoring & Maintenance

- **Set up alerts** for downtime
- **Monitor API usage** and costs
- **Regular updates** of dependencies
- **Backup your data** if needed

---

## Quick Start Recommendation

**For fastest deployment, use Streamlit Cloud**:
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Add your API key as environment variable
4. Share your live URL!

Your app will be available at: `https://your-app-name.streamlit.app` 