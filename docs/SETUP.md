# VirtualMukti Setup Guide

This guide will help you set up the VirtualMukti development environment.

## Prerequisites

### Required Software
- **Python 3.10 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download](https://nodejs.org/)
- **MongoDB 6.0 or higher** - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/downloads)

### Required Accounts and API Keys
1. **Firebase Account** - [Sign up](https://firebase.google.com/)
2. **Google Cloud Account** (for Gemini API and Maps API) - [Sign up](https://cloud.google.com/)
3. **Gemini API Key** - [Get API Key](https://makersuite.google.com/app/apikey)
4. **Google Maps API Key** - [Get API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)

## Step-by-Step Setup

### 1. MongoDB Setup

#### Option A: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS/Linux
   sudo systemctl start mongod
   ```
3. Verify MongoDB is running:
   ```bash
   mongosh
   ```

#### Option B: MongoDB Atlas (Cloud)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get connection string (replace `<password>` with your password)
4. Whitelist your IP address

### 2. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Realtime Database:
   - Go to Build → Realtime Database
   - Click "Create Database"
   - Choose location and start in test mode
4. Generate service account credentials:
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Save as `firebase-credentials.json` in backend directory
5. Get Firebase config for web:
   - Go to Project Settings → General
   - Scroll to "Your apps" → Web app
   - Copy configuration values

### 3. Google Cloud APIs Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable APIs:
   - Gemini API (Generative Language API)
   - Maps JavaScript API
   - Places API
4. Create API credentials:
   - Go to APIs & Services → Credentials
   - Create API Key
   - Restrict key (optional but recommended)

### 4. Backend Setup

1. Clone repository and navigate to backend:
   ```bash
   cd backend
   ```

2. Create Python virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

5. Edit `.env` with your credentials:
   ```env
   # MongoDB
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB_NAME=virtualmukti
   MONGODB_ENCRYPTION_KEY=your-32-byte-key-here
   
   # JWT
   JWT_SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   
   # Firebase
   FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
   FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
   
   # Gemini
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-3-flash
   
   # Google Maps
   GOOGLE_MAPS_API_KEY=your-maps-api-key
   
   # Encryption
   AES_ENCRYPTION_KEY=your-aes-256-key-here
   ```

6. Generate encryption keys:
   ```python
   # Run in Python shell
   import secrets
   print(secrets.token_hex(32))  # For AES_ENCRYPTION_KEY
   print(secrets.token_hex(32))  # For JWT_SECRET_KEY
   print(secrets.token_hex(16))  # For MONGODB_ENCRYPTION_KEY
   ```

7. Place `firebase-credentials.json` in backend directory

8. Run backend:
   ```bash
   python -m backend.main
   ```

9. Verify backend is running:
   - Open browser to `http://localhost:8000`
   - Check API docs at `http://localhost:8000/docs`

### 5. Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your credentials:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   
   # Firebase (from Firebase Console)
   VITE_FIREBASE_API_KEY=your-api-key
   VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   VITE_FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
   VITE_FIREBASE_PROJECT_ID=your-project-id
   VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
   VITE_FIREBASE_APP_ID=your-app-id
   
   # Google Maps
   VITE_GOOGLE_MAPS_API_KEY=your-maps-api-key
   
   VITE_APP_ENV=development
   ```

5. Run frontend:
   ```bash
   npm run dev
   ```

6. Verify frontend is running:
   - Open browser to `http://localhost:3000`

## Verification Checklist

- [ ] MongoDB is running and accessible
- [ ] Backend starts without errors
- [ ] Backend health check returns success: `http://localhost:8000/health`
- [ ] API documentation loads: `http://localhost:8000/docs`
- [ ] Frontend starts without errors
- [ ] Frontend loads in browser: `http://localhost:3000`
- [ ] No console errors in browser developer tools

## Troubleshooting

### MongoDB Connection Issues
- Verify MongoDB is running: `mongosh`
- Check connection string in `.env`
- For Atlas: verify IP whitelist and credentials

### Firebase Issues
- Verify `firebase-credentials.json` is in correct location
- Check Firebase Database URL format
- Ensure Realtime Database is enabled in Firebase Console

### API Key Issues
- Verify API keys are active in Google Cloud Console
- Check API restrictions and quotas
- Ensure required APIs are enabled

### Port Conflicts
- Backend default: 8000 (change in `.env`: `APP_PORT`)
- Frontend default: 3000 (change in `vite.config.ts`)

### Module Import Errors
- Backend: Ensure virtual environment is activated
- Frontend: Delete `node_modules` and run `npm install` again

## Next Steps

Once setup is complete:
1. Review the spec files in `.kiro/specs/virtualmukti/`
2. Start implementing tasks from `tasks.md`
3. Run tests to verify functionality
4. Refer to API documentation for endpoint details

## Security Notes

⚠️ **Important Security Reminders:**
- Never commit `.env` files or API keys to version control
- Use strong, randomly generated keys for production
- Restrict API keys to specific domains/IPs in production
- Enable Firebase security rules before production deployment
- Use HTTPS in production (TLS 1.3)
- Regularly rotate encryption keys and credentials

## Support

For issues or questions:
1. Check this setup guide
2. Review error messages carefully
3. Consult the main README.md
4. Check the spec files for requirements and design details
