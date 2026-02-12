# VirtualMukti MVP - Technical Summary

**AI-Powered Addiction Recovery Platform for Indian Users**

---

## Problem Statement

India faces a growing addiction crisis, particularly in Tier 2/3 cities and rural areas, where:
- Stigma prevents people from seeking help
- Professional treatment is expensive and inaccessible
- Privacy concerns deter users from traditional support systems
- Language barriers limit access to recovery resources

## Solution: VirtualMukti

An anonymous, AI-powered recovery platform providing:
1. **Privacy-First Support** - No phone/Aadhaar required
2. **AI Relapse Prediction** - LSTM-based risk assessment
3. **Multilingual CBT Chatbot** - Hindi/Hinglish/English support
4. **Low-Bandwidth Design** - Optimized for rural connectivity

---

## MVP Architecture

### Technology Stack

**Backend (Python/FastAPI)**
- FastAPI for REST APIs
- MongoDB for data storage with AES-256 encryption
- TensorFlow/Keras for LSTM model
- Google Gemini 3 Flash for chatbot
- JWT authentication with httpOnly cookies

**Frontend (React/TypeScript)**
- React 18 with TypeScript
- Vite for fast development
- Axios for API calls
- Minimal UI for MVP testing

**Security & Privacy**
- AES-256 encryption for demographics
- bcrypt password hashing
- Anonymous UUID identifiers
- No PII collection (no phone/Aadhaar)
- NDHM-style privacy compliance

### System Architecture

```
┌─────────────────────────────────────────────┐
│           Frontend (React)                   │
│  Login/Register | Dashboard | Chatbot       │
└─────────────────┬───────────────────────────┘
                  │ HTTPS/JWT
┌─────────────────▼───────────────────────────┐
│           Backend (FastAPI)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Auth   │  │    ML    │  │ Chatbot  │  │
│  │ Service  │  │ Service  │  │ Service  │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌─────▼─────┐  ┌───▼────┐
│MongoDB │  │   LSTM    │  │ Gemini │
│(Data)  │  │  Model    │  │  API   │
└────────┘  └───────────┘  └────────┘
```

---

## AI Components

### 1. LSTM Relapse Prediction Model

**Purpose:** Predict relapse risk (0-100 score) based on user activity patterns

**Architecture:**
- Sequential LSTM: 64 → 32 units
- Input: 30-day sequence of 6 features
- Output: Risk score (0-100)
- Dropout layers for regularization

**Features Used:**
1. `mood_score` (1-10)
2. `craving_intensity` (1-10)
3. `triggers_count` (daily)
4. `flows_completed` (daily recovery exercises)
5. `chatbot_engagement` (sessions)
6. `recovery_streak` (consecutive days)

**Training:**
- Synthetic data generation (1000 samples)
- Auto-trains on first prediction
- Risk levels: Low (<30), Moderate (30-70), High (≥70)

**Explainability:**
- Top 2 contributing risk factors
- Feature importance weights
- Human-readable explanations in user's language
- Protective factors identification

**Intervention Trigger:**
- High risk (≥70) flags user for proactive support
- Generates actionable recommendations

### 2. CBT Chatbot (Gemini 3 Flash)

**Purpose:** Provide evidence-based CBT support in Hindi/Hinglish/English

**CBT Techniques:**
- Cognitive Reframing: Challenge negative thoughts
- Behavioral Activation: Encourage positive activities
- Trigger Identification: Recognize and manage triggers
- Coping Strategies: Healthy alternatives to substance use

**Features:**
- Auto language detection (Hindi/Hinglish/English)
- Crisis keyword detection (12 keywords)
- Culturally sensitive responses for Indian context
- Concise responses (2-3 sentences)
- NIMHANS helpline integration for crisis

**Crisis Detection:**
- Keywords: suicide, kill myself, आत्महत्या, etc.
- Immediate helpline information
- Escalation flag for follow-up

---

## Current MVP Features

### ✅ Implemented

**Authentication:**
- Anonymous registration (no phone/Aadhaar)
- JWT-based session management
- Encrypted demographic storage

**AI Relapse Prediction:**
- LSTM model with 6 features
- 30-day activity analysis
- Risk score with explanation
- Top 2 contributing factors

**CBT Chatbot:**
- Gemini 3 Flash integration
- Hindi/Hinglish/English support
- Crisis detection
- CBT-tuned responses

**Frontend:**
- Login/Register page
- Dashboard with user info and prediction
- Chatbot interface

### 🚧 Not Yet Implemented (Future Roadmap)

**Recovery Features:**
- Daily recovery flows (breathing, meditation, journaling)
- Progress tracking and streaks
- Milestone celebrations (7, 30, 90 days)

**Emergency Support:**
- SOS button with immediate resources
- Crisis coping strategies
- NMK (rehabilitation center) lookup via Google Maps
- 24-hour follow-up scheduling

**Advanced Features:**
- Firebase realtime chat
- Message history persistence
- Offline PWA functionality
- Multi-language UI translation
- Model retraining pipeline
- Admin dashboard

---

## Data Privacy & Security

**Privacy-First Design:**
- Anonymous UUIDs (no real names)
- No phone numbers or Aadhaar
- Location limited to city/district
- AES-256 encryption for sensitive data
- Data deletion on request

**Security Measures:**
- bcrypt password hashing
- JWT with httpOnly cookies
- TLS 1.3 for data in transit
- Input validation and sanitization
- Rate limiting on endpoints

**Compliance:**
- NDHM-style privacy guidelines
- User consent required
- No third-party data sharing
- Complete data deletion capability

---

## Technical Highlights

**Scalability:**
- Async MongoDB operations (Motor)
- Stateless API design
- Horizontal scaling ready

**Performance:**
- LSTM prediction: <2 seconds
- Chatbot response: <3 seconds
- Low-bandwidth optimized

**Maintainability:**
- Repository pattern for data access
- Service layer for business logic
- Pydantic models for validation
- Comprehensive error handling

---

## Demo Flow

1. **Register** anonymously with demographics
2. **View Dashboard** with user info
3. **Get Prediction** - LSTM generates risk score with explanation
4. **Chat with Bot** - Send message in Hindi/Hinglish/English
5. **Crisis Detection** - Test with crisis keywords
6. **Logout** - Session cleared

---

## Future Roadmap

### Phase 1 (Current MVP)
✅ Anonymous authentication
✅ LSTM relapse prediction
✅ CBT chatbot
✅ Basic frontend

### Phase 2 (Next 2-4 weeks)
- Daily recovery flows
- SOS emergency support
- NMK center lookup
- Progress tracking

### Phase 3 (1-2 months)
- Firebase realtime chat
- Offline PWA support
- Model retraining automation
- Advanced analytics

### Phase 4 (3-6 months)
- Mobile app (React Native)
- Community features
- Peer support groups
- Integration with treatment centers

---

## Impact Potential

**Target Users:**
- 18-45 years old
- Tier 2/3 cities & rural India
- Alcohol, cannabis, opioid addiction
- 100M+ potential users in India

**Key Differentiators:**
- Privacy-first (no stigma)
- AI-powered personalization
- Multilingual support
- Low-cost/free access
- Culturally appropriate content

**Success Metrics:**
- User retention rate
- Recovery streak duration
- Relapse prediction accuracy
- Crisis intervention effectiveness
- User satisfaction scores

---

## Tech Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | FastAPI | REST APIs |
| Database | MongoDB | Data storage |
| ML Model | TensorFlow/Keras | LSTM prediction |
| Chatbot | Gemini 3 Flash | CBT conversations |
| Frontend | React + TypeScript | User interface |
| Auth | JWT + bcrypt | Security |
| Encryption | AES-256 | Data privacy |

---

## Contact & Resources

**GitHub:** [Repository structure ready]
**API Docs:** `http://localhost:8000/docs`
**Demo:** `http://localhost:3000`

**Key Files:**
- `backend/ml/lstm_model.py` - LSTM implementation
- `backend/services/chatbot_service.py` - Gemini integration
- `backend/services/auth_service.py` - Authentication
- `docs/DATA_MODELS.md` - Database schema
- `docs/SETUP.md` - Installation guide

---

**VirtualMukti** - Empowering recovery through AI, privacy, and compassion.
