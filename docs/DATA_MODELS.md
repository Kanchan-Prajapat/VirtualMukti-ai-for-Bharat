# VirtualMukti Data Models

This document describes the core data models implemented for VirtualMukti.

## Overview

All data models use Pydantic for validation and are stored in MongoDB. Sensitive data (demographics) is encrypted using AES-256 encryption before storage.

## Core Models

### 1. User Model

**Location**: `backend/models/user.py`

**Purpose**: Stores anonymous user information with encrypted demographics.

**Key Fields**:
- `id`: Anonymous UUID (no PII)
- `username`: Unique username (not PII)
- `password_hash`: bcrypt hashed password
- `demographics`: Encrypted demographic information
- `recovery_streak`: Consecutive days of sobriety
- `language_preference`: Hindi, Hinglish, or English
- `addiction_type`: Alcohol, cannabis, or opioid

**Encryption**: Demographics (age, gender, location) are encrypted at rest using AES-256.

**Indexes**:
- Unique index on `username`
- Unique index on `id`
- Index on `created_at`
- Index on `last_login`

### 2. Demographics Model

**Location**: `backend/models/user.py`

**Purpose**: Stores user demographic information (encrypted when stored).

**Key Fields**:
- `age`: 18-100 years
- `gender`: User's gender
- `location`: City/district (not exact address)
- `addiction_type`: Type of addiction
- `severity`: Mild, moderate, or severe

**Privacy**: All fields except `addiction_type` and `severity` are encrypted before storage.

### 3. UserActivity Model

**Location**: `backend/models/user_activity.py`

**Purpose**: Tracks daily user activity for relapse prediction and progress monitoring.

**Key Fields**:
- `user_id`: User identifier
- `date`: Activity date
- `mood_score`: 1-10 scale
- `craving_intensity`: 1-10 scale
- `triggers_encountered`: List of triggers
- `coping_strategies_used`: List of strategies
- `flows_completed`: Recovery flow IDs
- `chatbot_sessions`: Number of sessions
- `sos_triggered`: Whether SOS was triggered

**Indexes**:
- Unique compound index on `(user_id, date)`
- Index on `user_id`
- Index on `date`

**Usage**: Used by LSTM model for relapse risk prediction.

### 4. RelapseRiskPrediction Model

**Location**: `backend/models/relapse_prediction.py`

**Purpose**: Stores LSTM model predictions with explainability.

**Key Fields**:
- `user_id`: User identifier
- `prediction_date`: When prediction was made
- `risk_score`: 0-100 (higher = more risk)
- `confidence`: 0-1 model confidence
- `top_risk_factors`: List of contributing factors with importance weights
- `protective_factors`: Factors reducing risk
- `model_version`: LSTM model version used

**Indexes**:
- Compound index on `(user_id, prediction_date)`
- Index on `user_id`
- Index on `risk_score`

**Methods**:
- `get_risk_level()`: Returns "low", "moderate", or "high"
- `requires_intervention()`: Returns True if score >= 70

### 5. RiskFactor Model

**Location**: `backend/models/relapse_prediction.py`

**Purpose**: Represents individual risk factor with importance weight.

**Key Fields**:
- `factor_name`: Name of the factor
- `importance`: 0-1 weight
- `description`: Human-readable explanation

## Repository Pattern

All database operations use the Repository pattern for clean separation of concerns.

### UserRepository

**Location**: `backend/repositories/user_repository.py`

**Key Methods**:
- `create(user_data, password_hash)`: Create new user with encrypted demographics
- `get_by_username(username)`: Retrieve user by username
- `get_by_id(user_id)`: Retrieve user by ID
- `update_last_login(user_id)`: Update login timestamp
- `update_recovery_streak(user_id, streak)`: Update recovery streak
- `delete(user_id)`: Delete user and all data
- `username_exists(username)`: Check if username is taken

**Encryption**: Automatically encrypts demographics on create and decrypts on read.

### UserActivityRepository

**Location**: `backend/repositories/user_activity_repository.py`

**Key Methods**:
- `create(user_id, activity_data)`: Create daily activity entry
- `get_by_date(user_id, date)`: Get activity for specific date
- `get_recent(user_id, days)`: Get recent activities for LSTM
- `update(user_id, date, update_data)`: Update activity entry
- `increment_chatbot_session(user_id, date)`: Increment session count
- `add_flow_completed(user_id, date, flow_id)`: Add completed flow
- `trigger_sos(user_id, date)`: Mark SOS as triggered
- `delete_user_activities(user_id)`: Delete all user activities
- `get_activity_summary(user_id, days)`: Get summary statistics

### RelapseRiskRepository

**Location**: `backend/repositories/relapse_prediction_repository.py`

**Key Methods**:
- `create(prediction)`: Store new prediction
- `get_latest(user_id)`: Get most recent prediction
- `get_by_date(user_id, date)`: Get prediction for specific date
- `get_recent(user_id, days)`: Get recent predictions for trends
- `get_high_risk_users(threshold, hours)`: Find users needing intervention
- `delete_user_predictions(user_id)`: Delete all predictions
- `get_prediction_trend(user_id, days)`: Calculate trend (improving/stable/declining)
- `get_statistics(user_id, days)`: Get prediction statistics

## Database Initialization

**Script**: `backend/init_db.py`

Run to create all indexes:
```bash
python -m backend.init_db
```

Indexes are also created automatically on application startup via `main.py`.

## Data Flow

### User Registration
1. User submits registration data
2. Password hashed with bcrypt
3. Demographics encrypted with AES-256
4. User document stored in MongoDB
5. Anonymous UUID returned

### Daily Activity Tracking
1. User logs mood, cravings, triggers
2. Activity stored with date as key
3. Upsert ensures one entry per day
4. Used by LSTM for prediction

### Relapse Prediction
1. ML Service fetches last 30 days of activity
2. LSTM model generates risk score
3. SHAP generates feature importance
4. Prediction stored with explainability
5. High risk (>70) triggers intervention

## Privacy & Security

### Encryption
- **Algorithm**: AES-256-CBC
- **Key Management**: Stored in environment variables
- **Encrypted Fields**: Demographics (age, gender, location)
- **IV**: Random 16-byte IV per encryption

### Data Deletion
All repositories support complete data deletion:
```python
# Delete all user data
await UserRepository.delete(user_id)
await UserActivityRepository.delete_user_activities(user_id)
await RelapseRiskRepository.delete_user_predictions(user_id)
```

### Anonymization
- No phone numbers or Aadhaar
- Anonymous UUIDs instead of real names
- Location limited to city/district
- Usernames are not PII

## Validation

All models use Pydantic validators:
- Age: 18-100
- Scores: 1-10
- Risk score: 0-100
- Confidence: 0-1
- Username: alphanumeric + underscore
- Password: minimum 8 characters

## Error Handling

Repositories handle common errors:
- `DuplicateKeyError`: Username already exists
- `ConnectionFailure`: MongoDB connection issues
- `ValidationError`: Invalid data format
- `ValueError`: Business logic violations

## Testing

Property-based tests (optional) validate:
- Demographic data encryption (Property 2)
- User data encryption at rest (Property 17)
- Data deletion completeness (Property 19)

## Next Steps

Remaining models to implement:
- RecoveryFlow
- ChatConversation
- SOSEvent
- NMKCenter

These will be added in later tasks as needed.
