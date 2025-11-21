# Deploying to Render

This guide shows how to deploy the Flask Profile app to [Render](https://render.com) for free.

## Prerequisites

- GitHub account with repository pushed (✅ Already done)
- [Render](https://render.com) account (free)

## Deployment Steps

### 1. Connect GitHub to Render

1. Go to https://render.com and sign up/log in
2. Click **New +** → **Web Service**
3. Select **Connect a repository**
4. Authorize Render to access your GitHub account
5. Search for and select `Flask-Profile-app` repository

### 2. Configure the Service

Render will auto-detect the configuration from `render.yaml`, but here's what it will use:

- **Name:** `flask-profile-app`
- **Environment:** `Python 3.11`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn run:app`
- **Instance Type:** Free (shared CPU, 0.5 GB RAM)

### 3. Deploy

1. Click **Create Web Service**
2. Render will automatically build and deploy
3. Wait for the build to complete (~2-3 minutes)
4. Your app will be live at: `https://flask-profile-app.onrender.com`

## Auto-Deploy on Push

Once connected, every push to the `main` branch will trigger an automatic deployment.

## Environment Variables (Optional)

If needed, add environment variables in Render dashboard:
- **FLASK_ENV:** `production` (auto-set)
- **SECRET_KEY:** Generate a secure key (optional for production)

To generate a secret key in Python:
```python
import secrets
secrets.token_hex(32)
```

Then add it to Render dashboard under **Environment** → add `SECRET_KEY`.

## Database Considerations

**Current Setup:**
- SQLite database stored locally on the server
- Data persists per deployment but is reset on free tier restarts

**For Production (Persistent Data):**
- Upgrade to paid tier (persists data)
- Or connect PostgreSQL (free tier available)

To use PostgreSQL instead, update `app/__init__.py`:
```python
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
```

## Monitoring

- View logs: https://dashboard.render.com → Select service → **Logs**
- Monitor health: Render dashboard shows uptime and resource usage

## Free Tier Limits

- **Compute:** Shared CPU, 0.5 GB RAM
- **Uptime:** Spun down after 15 minutes of inactivity (cold start ~30 seconds)
- **Build time:** Up to 750 hours/month

## Troubleshooting

### Build Failed
- Check logs for dependency errors
- Ensure `requirements.txt` is in root directory
- Verify Python version compatibility

### App Won't Start
- Check `run.py` syntax
- Verify Flask app factory in `app/__init__.py`
- Review error logs in Render dashboard

### Database Not Persisting
- Free tier databases reset on restart
- Use PostgreSQL addon or upgrade to paid tier

## Next Steps

1. Deploy to Render following the steps above
2. Test the app at your Render URL
3. Share the deployed URL with others
4. Make code changes, push to GitHub → Auto-deploys

---

**Render Documentation:** https://render.com/docs
