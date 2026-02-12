# Design Document: VirtualMukti

## Overview

VirtualMukti is a privacy-first, AI-powered addiction recovery platform built for Indian users. The system architecture follows a three-tier design:

1. **Frontend Layer**: React-based web application optimized for low-bandwidth scenarios
2. **Backend Layer**: FastAPI services handling business logic, authentication, and API orchestration
3. **Data Layer**: MongoDB for persistent storage, Firebase for realtime features

The platform integrates multiple AI/ML components:
- **LSTM Model** (TensorFlow/Keras) for relapse risk prediction
- **Gemini 3 Flash LLM** for CBT-based conversational support
- **Google Maps API** for NMK center lookup

Key design principles:
- **Privacy by Design**: No PII collection, end-to-end encryption, anonymous sessions
- **Offline-First**: Progressive Web App (PWA) with service workers for offline capability
- **Cultural Sensitivity**: Hindi/Hinglish support with culturally appropriate content
- **Explainable AI**: Transparent model outputs with reasoning

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │   Chatbot    │  │  NMK Lookup  │      │
│  │  Component   │  │  Component   │  │  Component   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │ HTTPS/TLS 1.3
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     Auth     │  │   Recovery   │  │   Chatbot    │      │
│  │   Service    │  │   Service    │  │   Service    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  ML Service  │  │  SOS Service │  │  NMK Service │      │
│  │   (LSTM)     │  │              │  │  (Maps API)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬─────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│    MongoDB     │  │    Firebase     │  │  Gemini API    │
│  (User Data)   │  │   (Realtime)    │  │  (Chatbot LLM) │
└────────────────┘  └─────────────────┘  └────────────────┘
```

### Component Interaction Flow

**User Authentication Flow:**
1. User submits anonymous credentials (username, password)
2. Auth Service validates and creates JWT token
3. JWT stored in httpOnly cookie for session management
4. No phone/Aadhaar verification required

**Relapse Prediction Flow:**
1. Recovery Service collects user activity data (daily check-ins, mood, triggers)
2. ML Service batches data and feeds to LSTM Model
3. LSTM generates risk score (0-100) with feature importance
4. Result stored in MongoDB and displayed to user with explanation

**Chatbot Conversation Flow:**
1. User sends message via Chatbot Component
2. Message sent to Backend Chatbot Service
3. Service calls Gemini 3 Flash API with CBT-tuned prompt
4. Response streamed back via Firebase Realtime Database
5. Conversation history stored encrypted in MongoDB

**SOS Emergency Flow:**
1. User triggers SOS button
2. SOS Service immediately returns crisis resources
3. System logs event and schedules follow-up
4. Optional: Connect to nearby NMK via Maps API

## Components and Interfaces

### Frontend Components

#### 1. Authentication Module
```typescript
interface AuthModule {
  register(username: string, password: string, demographics: Demographics): Promise<AuthResponse>
  login(username: string, password: string): Promise<AuthResponse>
  logout(): Promise<void>
  isAuthenticated(): boolean
}

interface Demographics {
  age: number
  gender: string
  location: string
  addictionType: 'alcohol' | 'cannabis' | 'opioid'
  language: 'hindi' | 'hinglish' | 'english'
}

interface AuthResponse {
  success: boolean
  userId: string
  token: string
  error?: string
}
```

#### 2. Dashboard Component
```typescript
interface DashboardComponent {
  fetchUserProgress(): Promise<UserProgress>
  displayRelapseRisk(riskScore: RelapseRiskScore): void
  showRecoveryStreak(streak: number): void
  renderDailyFlow(flow: RecoveryFlow): void
}

interface UserProgress {
  recoveryStreak: number
  completedFlows: number
  relapseRiskTrend: number[]
  milestones: Milestone[]
}

interface RelapseRiskScore {
  score: number // 0-100
  explanation: string[]
  factors: { factor: string; weight: number }[]
  timestamp: Date
}
```

#### 3. Chatbot Component
```typescript
interface ChatbotComponent {
  sendMessage(message: string): Promise<void>
  receiveMessage(callback: (message: ChatMessage) => void): void
  detectCrisis(message: string): boolean
  endSession(): Promise<void>
}

interface ChatMessage {
  id: string
  sender: 'user' | 'bot'
  content: string
  timestamp: Date
  language: string
}
```

#### 4. Recovery Flow Component
```typescript
interface RecoveryFlowComponent {
  loadDailyFlow(): Promise<RecoveryFlow>
  completeFlow(flowId: string): Promise<void>
  trackProgress(flowId: string, progress: number): void
}

interface RecoveryFlow {
  id: string
  title: string
  description: string
  exercises: Exercise[]
  estimatedDuration: number // minutes
  addictionType: string
}

interface Exercise {
  id: string
  type: 'breathing' | 'journaling' | 'meditation' | 'cbt'
  instructions: string
  duration: number
}
```

#### 5. SOS Component
```typescript
interface SOSComponent {
  triggerSOS(): Promise<SOSResponse>
  displayCrisisResources(resources: CrisisResource[]): void
  connectToNMK(nmkId: string): Promise<void>
}

interface SOSResponse {
  immediateStrategies: string[]
  crisisResources: CrisisResource[]
  nearbyNMKs: NMKCenter[]
}

interface CrisisResource {
  name: string
  phone: string
  description: string
  availability: string
}
```

#### 6. NMK Lookup Component
```typescript
interface NMKLookupComponent {
  searchNMK(location: Location, radius: number): Promise<NMKCenter[]>
  displayNMKDetails(nmk: NMKCenter): void
  getDirections(nmk: NMKCenter): void
}

interface NMKCenter {
  id: string
  name: string
  address: string
  location: Location
  distance: number // km
  phone: string
  services: string[]
  rating?: number
}

interface Location {
  latitude: number
  longitude: number
}
```

### Backend Services

#### 1. Auth Service
```python
class AuthService:
    def register(self, username: str, password: str, demographics: Demographics) -> AuthResponse:
        """
        Create anonymous user account without PII
        - Hash password using bcrypt
        - Generate unique anonymous user ID
        - Store encrypted demographics in MongoDB
        - Return JWT token
        """
        pass
    
    def login(self, username: str, password: str) -> AuthResponse:
        """
        Authenticate user and create session
        - Verify credentials against MongoDB
        - Generate JWT with 24-hour expiry
        - Return token in httpOnly cookie
        """
        pass
    
    def validate_token(self, token: str) -> bool:
        """Verify JWT signature and expiry"""
        pass
```

#### 2. Recovery Service
```python
class RecoveryService:
    def get_daily_flow(self, user_id: str) -> RecoveryFlow:
        """
        Generate personalized daily recovery flow
        - Fetch user addiction type and recovery stage
        - Select appropriate exercises from flow library
        - Adapt difficulty based on user progress
        """
        pass
    
    def complete_flow(self, user_id: str, flow_id: str) -> None:
        """
        Record flow completion and update streak
        - Update recovery streak counter
        - Store completion timestamp
        - Trigger milestone check
        """
        pass
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Fetch and aggregate user progress data"""
        pass
```

#### 3. ML Service
```python
class MLService:
    def predict_relapse_risk(self, user_id: str) -> RelapseRiskScore:
        """
        Generate relapse risk prediction using LSTM
        - Fetch user activity data (last 30 days)
        - Preprocess features (mood, triggers, check-ins)
        - Run LSTM inference
        - Generate SHAP-based explanation
        - Return score with feature importance
        """
        pass
    
    def retrain_model(self, training_data: List[UserData]) -> ModelMetrics:
        """
        Retrain LSTM model with new data
        - Batch process anonymized user data
        - Split train/validation/test sets
        - Train LSTM with early stopping
        - Validate performance metrics
        - Deploy if accuracy improves
        """
        pass
    
    def explain_prediction(self, user_id: str, prediction: float) -> List[str]:
        """Generate human-readable explanation of risk factors"""
        pass
```

#### 4. Chatbot Service
```python
class ChatbotService:
    def send_message(self, user_id: str, message: str, language: str) -> ChatMessage:
        """
        Process user message and generate CBT-based response
        - Detect language (Hindi/Hinglish/English)
        - Check for crisis keywords
        - Build context from conversation history
        - Call Gemini 3 Flash API with CBT prompt
        - Stream response via Firebase
        - Store encrypted conversation
        """
        pass
    
    def detect_crisis(self, message: str) -> bool:
        """
        Detect crisis language in user message
        - Check for suicidal ideation keywords
        - Detect severe distress indicators
        - Return true if crisis detected
        """
        pass
    
    def build_cbt_prompt(self, message: str, history: List[ChatMessage]) -> str:
        """
        Construct CBT-tuned prompt for Gemini
        - Include CBT techniques (cognitive reframing, behavioral activation)
        - Add conversation context
        - Specify language and cultural sensitivity
        """
        pass
```

#### 5. SOS Service
```python
class SOSService:
    def handle_sos(self, user_id: str) -> SOSResponse:
        """
        Handle emergency SOS request
        - Log SOS event with timestamp
        - Fetch immediate coping strategies
        - Get crisis helpline numbers
        - Find nearby NMK centers
        - Schedule 24-hour follow-up
        """
        pass
    
    def schedule_followup(self, user_id: str, sos_id: str) -> None:
        """Schedule automated check-in 24 hours after SOS"""
        pass
```

#### 6. NMK Service
```python
class NMKService:
    def search_nmk(self, location: Location, radius: int) -> List[NMKCenter]:
        """
        Search for nearby rehabilitation centers
        - Call Google Maps API with location and radius
        - Filter for Nasha Mukti Kendras
        - Cache results for offline access
        - Return sorted by distance
        """
        pass
    
    def get_nmk_details(self, nmk_id: str) -> NMKCenter:
        """Fetch detailed information about specific NMK"""
        pass
    
    def cache_nmk_data(self, location: Location, centers: List[NMKCenter]) -> None:
        """Cache NMK data for low-bandwidth access"""
        pass
```

## Data Models

### User Model
```python
class User:
    id: str  # Anonymous UUID
    username: str  # Unique, not PII
    password_hash: str  # bcrypt hashed
    demographics: Demographics
    created_at: datetime
    last_login: datetime
    language_preference: str
    
    # Recovery tracking
    recovery_start_date: datetime
    addiction_type: str
    recovery_streak: int
    
    # Privacy
    data_encrypted: bool = True
    consent_given: bool
```

### Demographics Model
```python
class Demographics:
    age: int
    gender: str
    location: str  # City/district, not exact address
    addiction_type: str
    severity: str  # self-reported: mild, moderate, severe
```

### Recovery Flow Model
```python
class RecoveryFlow:
    id: str
    title: str
    description: str
    addiction_type: str
    difficulty_level: str
    exercises: List[Exercise]
    estimated_duration: int
    language: str
    
class Exercise:
    id: str
    type: str  # breathing, journaling, meditation, cbt
    instructions: str
    duration: int
    media_url: Optional[str]  # compressed for low bandwidth
```

### User Activity Model
```python
class UserActivity:
    user_id: str
    date: datetime
    
    # Daily tracking
    mood_score: int  # 1-10
    craving_intensity: int  # 1-10
    triggers_encountered: List[str]
    coping_strategies_used: List[str]
    
    # Flow completion
    flows_completed: List[str]
    exercises_completed: List[str]
    
    # Engagement
    chatbot_sessions: int
    messages_sent: int
    sos_triggered: bool
```

### Relapse Risk Prediction Model
```python
class RelapseRiskPrediction:
    user_id: str
    prediction_date: datetime
    risk_score: float  # 0-100
    confidence: float  # 0-1
    
    # Explainability
    top_risk_factors: List[RiskFactor]
    protective_factors: List[str]
    
    # Model metadata
    model_version: str
    features_used: List[str]

class RiskFactor:
    factor_name: str
    importance: float
    description: str
```

### Chat Conversation Model
```python
class ChatConversation:
    id: str
    user_id: str
    started_at: datetime
    ended_at: Optional[datetime]
    language: str
    
    messages: List[ChatMessage]
    crisis_detected: bool
    sos_triggered: bool
    
    # Privacy
    encrypted: bool = True

class ChatMessage:
    id: str
    conversation_id: str
    sender: str  # 'user' or 'bot'
    content: str  # encrypted
    timestamp: datetime
    language: str
```

### SOS Event Model
```python
class SOSEvent:
    id: str
    user_id: str
    triggered_at: datetime
    resolved_at: Optional[datetime]
    
    # Context
    trigger_reason: Optional[str]
    user_location: Optional[Location]
    
    # Response
    strategies_provided: List[str]
    resources_shared: List[str]
    nmk_contacted: Optional[str]
    
    # Follow-up
    followup_scheduled: datetime
    followup_completed: bool
```

### NMK Center Model
```python
class NMKCenter:
    id: str
    name: str
    address: str
    location: Location
    phone: str
    email: Optional[str]
    
    # Services
    services_offered: List[str]
    addiction_types_treated: List[str]
    capacity: Optional[int]
    
    # Metadata
    verified: bool
    rating: Optional[float]
    last_updated: datetime
    
    # Caching
    cached_at: Optional[datetime]
```

### LSTM Model Configuration
```python
class LSTMModelConfig:
    model_version: str
    architecture: dict  # Layer configuration
    
    # Training parameters
    sequence_length: int = 30  # days of history
    features: List[str] = [
        'mood_score',
        'craving_intensity',
        'triggers_count',
        'flows_completed',
        'chatbot_engagement',
        'recovery_streak'
    ]
    
    # Performance metrics
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    
    trained_at: datetime
    deployed_at: Optional[datetime]
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Anonymous Registration Creates Unique Sessions

*For any* valid username and password combination, when a user completes registration, the system should create a unique anonymous session with a unique user identifier that differs from all other user identifiers.

**Validates: Requirements 1.2, 1.5**

### Property 2: Demographic Data Encryption

*For any* user demographic information (age, gender, location, addiction type), when stored in MongoDB, the data should be encrypted using AES-256 encryption.

**Validates: Requirements 1.3**

### Property 3: Relapse Risk Prediction Generation

*For any* user with activity data who logs in, the LSTM model should generate a relapse risk score between 0 and 100.

**Validates: Requirements 2.1**

### Property 4: Prediction Explainability

*For any* relapse risk prediction generated by the LSTM model, the system should provide an explanation containing at least one risk factor with its importance weight.

**Validates: Requirements 2.2**

### Property 5: Language-Consistent Predictions

*For any* user with a language preference (Hindi, Hinglish, or English), when displaying relapse risk predictions, the system should present the information in the user's preferred language.

**Validates: Requirements 2.5**

### Property 6: Chatbot Language Consistency

*For any* message sent to the chatbot in a specific language (Hindi, Hinglish, or English), the chatbot response should be in the same language as the user's message.

**Validates: Requirements 3.2**

### Property 7: Crisis Detection and Escalation

*For any* message containing crisis keywords (suicidal ideation, severe distress indicators), the system should detect the crisis and trigger SOS request handling.

**Validates: Requirements 3.3**

### Property 8: Conversation Encryption

*For any* completed chat session, when stored in MongoDB, the conversation messages should be encrypted.

**Validates: Requirements 3.5**

### Property 9: Personalized Recovery Flow Generation

*For any* user with a specified addiction type and recovery stage, when accessing the daily flow section, the system should return a recovery flow that matches the user's addiction type.

**Validates: Requirements 4.1**

### Property 10: Recovery Streak Increment

*For any* user who completes a recovery flow, the system should increment the user's recovery streak by 1 and store the completion timestamp.

**Validates: Requirements 4.2**

### Property 11: SOS Response Completeness

*For any* SOS request triggered by a user, the system should provide a response containing both immediate coping strategies and options to contact nearby NMK centers or helplines.

**Validates: Requirements 5.2, 5.3**

### Property 12: SOS Event Logging

*For any* SOS request triggered, the system should create a log entry in the database with a timestamp and user identifier.

**Validates: Requirements 5.4**

### Property 13: SOS Follow-up Scheduling

*For any* resolved SOS request, the system should schedule a follow-up check-in with a timestamp within 24 hours of resolution.

**Validates: Requirements 5.5**

### Property 14: NMK Distance Filtering

*For any* location-based NMK search with a specified radius, all returned NMK centers should be within the specified distance from the search location.

**Validates: Requirements 6.1**

### Property 15: NMK Data Completeness

*For any* NMK center returned in search results, the result should contain name, address, distance, contact information, and services offered.

**Validates: Requirements 6.2**

### Property 16: NMK Data Caching

*For any* NMK search performed, the system should cache the results with a timestamp for offline access.

**Validates: Requirements 6.4**

### Property 17: User Data Encryption at Rest

*For any* user data (profile, activity, conversations) stored in MongoDB, the data should be encrypted using AES-256 encryption.

**Validates: Requirements 7.1**

### Property 18: Conversation PII Anonymization

*For any* user conversation stored in the database, personally identifiable information (phone numbers, addresses, real names) should be anonymized or redacted.

**Validates: Requirements 7.3**

### Property 19: Data Deletion Completeness

*For any* user data deletion request, the system should remove all associated user data (profile, conversations, activity logs, predictions) from the database.

**Validates: Requirements 7.5**

### Property 20: Media Compression Effectiveness

*For any* image or media file uploaded or served by the system, the compressed version should be at least 60% smaller than the original file size.

**Validates: Requirements 8.2**

### Property 21: Offline Functionality Preservation

*For any* user accessing the platform while offline, the system should allow viewing of cached conversations and offline recovery exercises without requiring network connectivity.

**Validates: Requirements 8.5**

### Property 22: Dashboard Data Completeness

*For any* user viewing their dashboard, the displayed data should include recovery streak, number of completed flows, and relapse risk trend data.

**Validates: Requirements 9.1**

### Property 23: Progress Data Privacy Protection

*For any* progress data displayed on the dashboard, sensitive information (specific addiction type, personal identifiers) should be masked or protected from screenshot capture or sharing.

**Validates: Requirements 9.5**

### Property 24: Language Preference Persistence

*For any* user who selects a language preference or switches languages, the system should persist this choice across sessions and maintain session state without data loss.

**Validates: Requirements 10.2, 10.5**

### Property 25: Multi-Language Feature Availability

*For any* language selected by the user (Hindi, Hinglish, English), all core features (chatbot, recovery flows, UI elements) should be available and functional in that language.

**Validates: Requirements 10.3**

### Property 26: Training Data Anonymization

*For any* user data used for LSTM model training, the data should be anonymized with all personally identifiable information removed before being included in the training dataset.

**Validates: Requirements 11.5**

### Property 27: Message Queue and Sync

*For any* message sent during interrupted network connectivity, the system should queue the message locally and sync it to the server when connection is restored, preserving message order.

**Validates: Requirements 12.3**

## Error Handling

### Authentication Errors
- **Invalid Credentials**: Return 401 with clear error message in user's language
- **Duplicate Username**: Return 409 with suggestion to choose different username
- **Session Expiry**: Return 401 and redirect to login with session timeout message
- **Token Validation Failure**: Clear session and require re-authentication

### ML Service Errors
- **LSTM Model Unavailable**: Return cached previous prediction with staleness indicator
- **Insufficient Data for Prediction**: Return message explaining need for more activity data
- **Model Inference Timeout**: Retry once, then return default moderate risk score with explanation
- **Feature Extraction Failure**: Log error and use subset of available features

### Chatbot Errors
- **Gemini API Timeout**: Return pre-defined supportive message and retry in background
- **Gemini API Rate Limit**: Queue message and notify user of brief delay
- **Crisis Detection False Positive**: Allow user to dismiss SOS if triggered incorrectly
- **Language Detection Failure**: Default to user's saved language preference

### Recovery Flow Errors
- **Flow Not Found**: Return default flow for user's addiction type
- **Flow Completion Failure**: Retry database write, cache locally if persistent failure
- **Streak Calculation Error**: Recalculate from activity logs

### SOS Service Errors
- **NMK Search Failure**: Return cached NMK data and national helpline numbers
- **Follow-up Scheduling Failure**: Retry scheduling and log for manual intervention
- **Crisis Resource Unavailable**: Return multiple backup resources and helplines

### NMK Service Errors
- **Google Maps API Failure**: Return cached NMK data with staleness warning
- **Location Permission Denied**: Allow manual location entry or city selection
- **No Results Found**: Expand search radius and suggest alternative search terms
- **Cache Corruption**: Re-fetch from API and rebuild cache

### Data Storage Errors
- **MongoDB Connection Failure**: Queue writes locally and sync when connection restored
- **Encryption Failure**: Reject write and log critical error for investigation
- **Data Validation Failure**: Return 400 with specific validation errors
- **Storage Quota Exceeded**: Archive old data and notify administrators

### Network and Performance Errors
- **Slow Connection Detected**: Switch to low-bandwidth mode automatically
- **Request Timeout**: Retry with exponential backoff (max 3 attempts)
- **Firebase Connection Lost**: Queue realtime updates and sync when reconnected
- **Service Worker Failure**: Fall back to network-only mode

### Privacy and Security Errors
- **Encryption Key Unavailable**: Prevent data access and require key recovery
- **PII Detection in Input**: Warn user and offer to anonymize before storage
- **Suspicious Activity Detected**: Require re-authentication
- **Data Breach Attempt**: Lock account and notify security team

## Testing Strategy

### Dual Testing Approach

VirtualMukti will employ both **unit testing** and **property-based testing** to ensure comprehensive coverage:

- **Unit Tests**: Verify specific examples, edge cases, and error conditions
- **Property Tests**: Verify universal properties across all inputs using randomized test data

Both approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing Configuration

**Library Selection:**
- **Backend (Python)**: Use **Hypothesis** for property-based testing
- **Frontend (TypeScript/JavaScript)**: Use **fast-check** for property-based testing

**Test Configuration:**
- Each property test must run a minimum of **100 iterations** to ensure adequate randomization coverage
- Each property test must include a comment tag referencing the design document property
- Tag format: `# Feature: virtualmukti, Property {number}: {property_text}`

**Property Test Implementation:**
- Each correctness property listed above must be implemented as a single property-based test
- Tests should generate random valid inputs (users, messages, flows, etc.)
- Tests should verify the property holds for all generated inputs
- Tests should fail fast with a clear counterexample when property is violated

### Unit Testing Strategy

**Focus Areas for Unit Tests:**
1. **Specific Examples**: Test concrete scenarios (e.g., registering user "test123" with password "secure456")
2. **Edge Cases**: Test boundary conditions (e.g., 7-day milestone, 70+ risk score threshold, empty NMK results)
3. **Error Conditions**: Test failure scenarios (e.g., invalid credentials, API timeouts, network failures)
4. **Integration Points**: Test component interactions (e.g., Auth Service → MongoDB, Chatbot Service → Gemini API)

**Unit Test Balance:**
- Avoid writing too many unit tests for scenarios already covered by property tests
- Focus unit tests on specific examples that demonstrate correct behavior
- Use unit tests for error handling and edge cases that are difficult to express as properties

### Test Coverage Goals

**Backend Services:**
- Auth Service: 90%+ coverage (critical for security)
- ML Service: 85%+ coverage (complex logic)
- Chatbot Service: 85%+ coverage (crisis detection critical)
- Recovery Service: 80%+ coverage
- SOS Service: 90%+ coverage (emergency functionality)
- NMK Service: 75%+ coverage

**Frontend Components:**
- Authentication Module: 85%+ coverage
- Dashboard Component: 80%+ coverage
- Chatbot Component: 85%+ coverage
- SOS Component: 90%+ coverage
- Recovery Flow Component: 80%+ coverage
- NMK Lookup Component: 75%+ coverage

### Integration Testing

**Critical Integration Paths:**
1. End-to-end user registration and login flow
2. Complete chatbot conversation with crisis detection
3. SOS trigger → resource delivery → follow-up scheduling
4. Daily flow completion → streak update → milestone recognition
5. Relapse prediction → explanation generation → user display
6. NMK search → caching → offline access

**Integration Test Approach:**
- Use test doubles for external APIs (Gemini, Google Maps)
- Test with real MongoDB and Firebase instances in test environment
- Verify data flows correctly through all layers
- Test error propagation and recovery

### Performance Testing

**Key Performance Metrics:**
- Chatbot response time: < 3 seconds (p95)
- SOS response time: < 5 seconds (p99)
- Dashboard load time: < 10 seconds on 2G connection
- LSTM prediction time: < 2 seconds
- NMK search time: < 5 seconds

**Load Testing:**
- Simulate 1000 concurrent users
- Test chatbot under high load (100 concurrent conversations)
- Test LSTM prediction batching with 500 users
- Verify Firebase realtime performance with 200 active connections

### Security Testing

**Security Test Areas:**
1. **Authentication**: Test JWT validation, session management, password hashing
2. **Encryption**: Verify AES-256 encryption for data at rest
3. **PII Protection**: Test anonymization and redaction logic
4. **Input Validation**: Test SQL injection, XSS, CSRF protection
5. **API Security**: Test rate limiting, authentication headers, CORS

### Accessibility Testing

**Accessibility Requirements:**
- WCAG 2.1 Level AA compliance
- Screen reader compatibility
- Keyboard navigation support
- High contrast mode for low vision users
- Text size adjustment without breaking layout

### Localization Testing

**Language Testing:**
- Verify Hindi, Hinglish, and English translations
- Test language switching without state loss
- Verify cultural appropriateness of content
- Test right-to-left text handling for Urdu (future)

### Monitoring and Observability

**Production Monitoring:**
- Track relapse prediction accuracy over time
- Monitor chatbot conversation quality (user satisfaction)
- Track SOS response times and resolution rates
- Monitor API error rates and timeouts
- Track user engagement metrics (daily active users, flow completion rates)

**Alerting:**
- Alert on high error rates (> 5% of requests)
- Alert on slow response times (> p95 thresholds)
- Alert on SOS volume spikes (potential crisis event)
- Alert on model performance degradation
- Alert on security anomalies
