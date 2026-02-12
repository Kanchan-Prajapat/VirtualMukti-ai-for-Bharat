# VirtualMukti Frontend Components

Minimal React components for MVP testing.

## Components Created

### 1. LoginRegister Page (`src/pages/LoginRegister.tsx`)

**Features:**
- Toggle between login and register forms
- Login: username + password
- Register: username, password, demographics, language preference
- Displays API response as JSON
- Stores user_id in localStorage
- Link to dashboard after successful auth

**API Calls:**
- `POST /api/auth/login`
- `POST /api/auth/register`

### 2. Dashboard Page (`src/pages/Dashboard.tsx`)

**Features:**
- Displays user information (raw JSON)
- Displays relapse risk prediction (raw JSON)
- Logout button
- Link to chatbot
- Refresh prediction button

**API Calls:**
- `GET /api/auth/me` - User info
- `GET /api/ml/relapse-risk` - Prediction
- `POST /api/auth/logout` - Logout

### 3. Chatbot Page (`src/pages/Chatbot.tsx`)

**Features:**
- Simple message input (textarea)
- Displays conversation history
- Shows crisis detection flag
- Shows detected language
- Back to dashboard link

**API Calls:**
- `POST /api/chatbot/message`

## Routing

Simple routing in `App.tsx`:
- `/` - Login/Register
- `/dashboard` - Dashboard
- `/chatbot` - Chatbot

No React Router - uses basic state and window.location.

## Styling

Minimal CSS in `index.css`:
- Basic layout
- Simple form styling
- No animations
- No complex layouts
- No charts or visualizations

## Usage

1. Start backend:
```bash
cd backend
python -m backend.main
```

2. Start frontend:
```bash
cd frontend
npm run dev
```

3. Open browser to `http://localhost:3000`

## Testing Flow

1. Register new user
2. View dashboard with user info and prediction
3. Go to chatbot
4. Send messages in English/Hindi/Hinglish
5. Test crisis detection with keywords
6. Logout

## Notes

- All responses displayed as raw JSON
- No error boundaries
- No loading states (just text)
- No form validation beyond required fields
- No styling beyond basic layout
- Authentication via httpOnly cookies
- User ID stored in localStorage (for reference only)
