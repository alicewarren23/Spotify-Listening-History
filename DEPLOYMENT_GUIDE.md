# Streamlit Community Cloud Deployment Guide

## 🚀 Deploy Your Spotify Dashboard to Streamlit Cloud (FREE)

### Prerequisites
- GitHub repository (which you already have!)
- Streamlit Community Cloud account

### Step 1: Prepare Your Repository

Your repository needs these files (✅ already done):
- `spotify_dashboard.py` - Your main app
- `requirements.txt` - Dependencies
- `DASHBOARD_README.md` - Documentation

### Step 2: Add Secrets Configuration

Create a `.streamlit/secrets.toml` file for your Google Sheets credentials:

```toml
# .streamlit/secrets.toml
[google_sheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "your-private-key"
client_email = "your-client-email"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
```

### Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `alicewarren23/Spotify-Listening-History`
5. Set main file path: `spotify_dashboard.py`
6. Click "Deploy!"

### Step 4: Add Secrets in Streamlit Cloud

1. In your deployed app, click the hamburger menu (⚙️)
2. Go to "Settings" → "Secrets"
3. Paste your secrets.toml content
4. Save

Your app will be live at: `https://spotify-dashboard-[random].streamlit.app/`

### Benefits:
- ✅ FREE hosting
- ✅ Automatic SSL (HTTPS)
- ✅ Auto-deploys when you push to GitHub
- ✅ Easy secrets management
- ✅ Custom domain support
- ✅ Perfect for Streamlit apps
