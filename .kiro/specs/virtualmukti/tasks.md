# Implementation Plan: VirtualMukti

## Overview

This implementation plan breaks down the VirtualMukti MVP into discrete, incremental coding tasks. The approach follows a layered architecture:

1. **Foundation**: Set up project structure, database models, and core utilities
2. **Authentication**: Implement anonymous user registration and session management
3. **Recovery Features**: Build daily flows, progress tracking, and streak management
4. **AI/ML Integration**: Implement LSTM relapse prediction and Gemini chatbot
5. **Emergency Support**: Build SOS functionality and NMK lookup
6. **Frontend**: Create React components and integrate with backend
7. **Testing & Polish**: Implement property-based tests and optimize for low bandwidth

Each task builds incrementally, with testing integrated throughout to validate functionality early.

## Tasks

- [x] 1. Set up project structure and core infrastructure
  - Create backend directory structure: `/backend/api/ml/chatbot/`
  - Create frontend directory structure: `/frontend/components/pages/styles/`
  - Set up Python virtual environment and install dependencies (FastAPI, TensorFlow, Keras, pymongo, firebase-admin, python-jose, bcrypt, hypothesis)
  - Set up React project with TypeScript and install dependencies (react, react-router-dom, firebase, axios, fast-check)
  - Create `.env` files for environment variables (MongoDB URI, Firebase config, Gemini API key, Google Maps API key)
  - Set up MongoDB connection utility with encryption configuration
  - Set up Firebase initialization for realtime features
  - _Requirements: 7.1, 7.2, 12.1_

- [ ] 2. Implement data models and database layer
  - [x] 2.1 Create MongoDB data models for User, Demographics, UserActivity, RecoveryFlow, ChatConversation, SOSEvent, NMKCenter, RelapseRiskPrediction
    - Define Pydantic models for data validation
    - Implement AES-256 encryption utilities for sensitive fields
    - Create database indexes for performance (user_id, date, location)
    - _Requirements: 1.3, 7.1_
  
  - [ ]* 2.2 Write property test for data encryption
    - **Property 2: Demographic Data Encryption**
    - **Property 17: User Data Encryption at Rest**
    - **Validates: Requirements 1.3, 7.1**
  
  - [x] 2.3 Implement database CRUD operations for all models
    - Create repository pattern classes for each model
    - Implement create, read, update, delete operations
    - Add error handling for connection failures and validation errors
    - _Requirements: 7.1, 7.5_
  
  - [ ]* 2.4 Write property test for data deletion completeness
    - **Property 19: Data Deletion Completeness**
    - **Validates: Requirements 7.5**

- [ ] 3. Implement authentication service
  - [x] 3.1 Create Auth Service with anonymous registration
    - Implement `register()` function: validate username uniqueness, hash password with bcrypt, generate anonymous UUID
    - Implement `login()` function: verify credentials, generate JWT token with 24-hour expiry
    - Implement `validate_token()` function: verify JWT signature and expiration
    - Store JWT in httpOnly cookies for security
    - _Requirements: 1.1, 1.2, 1.4, 1.5_
  
  - [ ]* 3.2 Write property test for anonymous registration
    - **Property 1: Anonymous Registration Creates Unique Sessions**
    - **Validates: Requirements 1.2, 1.5**
  
  - [x] 3.3 Create FastAPI authentication endpoints
    - POST `/api/auth/register` - anonymous registration
    - POST `/api/auth/login` - user login
    - POST `/api/auth/logout` - session termination
    - GET `/api/auth/validate` - token validation
    - Add request validation and error handling
    - _Requirements: 1.1, 1.2_
  
  - [ ]* 3.4 Write unit tests for authentication edge cases
    - Test duplicate username handling
    - Test invalid credentials
    - Test token expiry
    - Test session management
    - _Requirements: 1.1, 1.2_

- [ ] 4. Checkpoint - Ensure authentication tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement recovery flow service
  - [ ] 5.1 Create recovery flow library with Hindi/Hinglish content
    - Define recovery flows for alcohol, cannabis, and opioid addiction
    - Create exercises: breathing, journaling, meditation, CBT techniques
    - Implement content in Hindi, Hinglish, and English
    - Optimize media files for low bandwidth (compress images to 60%+ reduction)
    - _Requirements: 4.1, 4.4, 8.2_
  
  - [ ]* 5.2 Write property test for media compression
    - **Property 20: Media Compression Effectiveness**
    - **Validates: Requirements 8.2**
  
  - [ ] 5.3 Implement Recovery Service
    - Implement `get_daily_flow()`: fetch user addiction type, select personalized flow
    - Implement `complete_flow()`: update recovery streak, store completion timestamp
    - Implement `get_user_progress()`: aggregate streak, completed flows, milestones
    - Add logic for milestone detection (7, 30, 90 days)
    - _Requirements: 4.1, 4.2, 4.3, 9.1, 9.2_
  
  - [ ]* 5.4 Write property tests for recovery flow service
    - **Property 9: Personalized Recovery Flow Generation**
    - **Property 10: Recovery Streak Increment**
    - **Property 22: Dashboard Data Completeness**
    - **Validates: Requirements 4.1, 4.2, 9.1**
  
  - [ ] 5.5 Create FastAPI recovery endpoints
    - GET `/api/recovery/daily-flow` - get personalized daily flow
    - POST `/api/recovery/complete-flow` - mark flow as completed
    - GET `/api/recovery/progress` - get user progress data
    - Add authentication middleware
    - _Requirements: 4.1, 4.2, 9.1_

- [ ] 6. Implement LSTM relapse prediction model
  - [x] 6.1 Create LSTM model architecture with TensorFlow/Keras
    - Define LSTM architecture: input layer (6 features), 2 LSTM layers (64, 32 units), dropout layers, dense output
    - Define features: mood_score, craving_intensity, triggers_count, flows_completed, chatbot_engagement, recovery_streak
    - Set sequence length to 30 days of history
    - Implement model training pipeline with train/validation/test split
    - _Requirements: 2.1, 11.1, 11.2_
  
  - [x] 6.2 Implement ML Service for relapse prediction
    - Implement `predict_relapse_risk()`: fetch user activity data (30 days), preprocess features, run LSTM inference, return score 0-100
    - Implement `explain_prediction()`: use SHAP or feature importance to generate explanation
    - Implement `retrain_model()`: batch process anonymized data, train model, validate performance
    - Add model versioning and rollback capability
    - _Requirements: 2.1, 2.2, 2.4, 11.3, 11.4_
  
  - [ ]* 6.3 Write property tests for ML service
    - **Property 3: Relapse Risk Prediction Generation**
    - **Property 4: Prediction Explainability**
    - **Property 26: Training Data Anonymization**
    - **Validates: Requirements 2.1, 2.2, 11.5**
  
  - [x] 6.4 Create FastAPI ML endpoints
    - GET `/api/ml/relapse-risk` - get daily relapse risk prediction
    - POST `/api/ml/retrain` - trigger model retraining (admin only)
    - GET `/api/ml/model-info` - get current model version and metrics
    - _Requirements: 2.1, 2.2_
  
  - [ ]* 6.5 Write unit tests for LSTM edge cases
    - Test insufficient data handling
    - Test model unavailable fallback
    - Test feature extraction errors
    - _Requirements: 2.1_

- [ ] 7. Implement chatbot service with Gemini integration
  - [x] 7.1 Create Chatbot Service with CBT-tuned prompts
    - Implement `send_message()`: detect language, build context from history, call Gemini 3 Flash API
    - Implement `build_cbt_prompt()`: construct prompt with CBT techniques (cognitive reframing, behavioral activation, coping strategies)
    - Implement `detect_crisis()`: check for suicidal ideation keywords, severe distress indicators
    - Add Hindi/Hinglish language support in prompts
    - Store conversations encrypted in MongoDB
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  
  - [ ]* 7.2 Write property tests for chatbot service
    - **Property 6: Chatbot Language Consistency**
    - **Property 7: Crisis Detection and Escalation**
    - **Property 8: Conversation Encryption**
    - **Property 18: Conversation PII Anonymization**
    - **Validates: Requirements 3.2, 3.3, 3.5, 7.3**
  
  - [ ] 7.3 Implement Firebase realtime message delivery
    - Set up Firebase Realtime Database for chat messages
    - Implement message streaming from Gemini to Firebase
    - Add message queuing for offline scenarios
    - Implement sync logic when connection restored
    - _Requirements: 12.1, 12.3_
  
  - [ ]* 7.4 Write property test for message queue and sync
    - **Property 27: Message Queue and Sync**
    - **Validates: Requirements 12.3**
  
  - [x] 7.5 Create FastAPI chatbot endpoints
    - POST `/api/chatbot/message` - send message and get response
    - GET `/api/chatbot/history` - get conversation history
    - POST `/api/chatbot/end-session` - end chat session
    - WebSocket `/api/chatbot/stream` - realtime message streaming
    - _Requirements: 3.1, 3.2, 12.1_

- [ ] 8. Checkpoint - Ensure AI/ML tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement SOS emergency support service
  - [ ] 9.1 Create SOS Service
    - Implement `handle_sos()`: log event, fetch coping strategies, get crisis helplines, find nearby NMKs
    - Implement `schedule_followup()`: create follow-up task for 24 hours after SOS resolution
    - Create crisis resource database with Indian helplines (NIMHANS, Vandrevala Foundation, etc.)
    - Add immediate grounding exercises and coping strategies
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ]* 9.2 Write property tests for SOS service
    - **Property 11: SOS Response Completeness**
    - **Property 12: SOS Event Logging**
    - **Property 13: SOS Follow-up Scheduling**
    - **Validates: Requirements 5.2, 5.3, 5.4, 5.5**
  
  - [ ] 9.3 Create FastAPI SOS endpoints
    - POST `/api/sos/trigger` - trigger SOS request
    - POST `/api/sos/resolve` - mark SOS as resolved
    - GET `/api/sos/resources` - get crisis resources
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ]* 9.4 Write unit tests for SOS edge cases
    - Test SOS with no nearby NMKs
    - Test follow-up scheduling failures
    - Test concurrent SOS requests
    - _Requirements: 5.1, 5.5_

- [ ] 10. Implement NMK lookup service with Google Maps integration
  - [ ] 10.1 Create NMK Service
    - Implement `search_nmk()`: call Google Maps API with location and 50km radius, filter for rehabilitation centers
    - Implement `get_nmk_details()`: fetch detailed information about specific NMK
    - Implement `cache_nmk_data()`: store NMK results in MongoDB with timestamp for offline access
    - Add distance calculation and sorting logic
    - _Requirements: 6.1, 6.2, 6.4, 6.5_
  
  - [ ]* 10.2 Write property tests for NMK service
    - **Property 14: NMK Distance Filtering**
    - **Property 15: NMK Data Completeness**
    - **Property 16: NMK Data Caching**
    - **Validates: Requirements 6.1, 6.2, 6.4**
  
  - [ ] 10.3 Create FastAPI NMK endpoints
    - GET `/api/nmk/search` - search for nearby NMK centers
    - GET `/api/nmk/{id}` - get NMK details
    - GET `/api/nmk/cached` - get cached NMK data for offline
    - _Requirements: 6.1, 6.2, 6.4_
  
  - [ ]* 10.4 Write unit tests for NMK edge cases
    - Test Maps API failure with cache fallback
    - Test no results found scenario
    - Test location permission denied
    - _Requirements: 6.1, 6.5_

- [ ] 11. Implement multi-language support
  - [ ] 11.1 Create language detection and translation utilities
    - Implement language detection from browser headers
    - Create translation files for Hindi, Hinglish, and English
    - Implement language switching logic with state persistence
    - Add cultural sensitivity checks for Indian context
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 11.2 Write property tests for language support
    - **Property 5: Language-Consistent Predictions**
    - **Property 24: Language Preference Persistence**
    - **Property 25: Multi-Language Feature Availability**
    - **Validates: Requirements 2.5, 10.2, 10.3, 10.5**
  
  - [ ] 11.3 Integrate language support across all services
    - Update Auth Service to store language preference
    - Update Recovery Service to serve flows in user's language
    - Update ML Service to display predictions in user's language
    - Update Chatbot Service to respond in user's language
    - _Requirements: 2.5, 3.2, 4.4, 10.3_

- [ ] 12. Implement frontend React components
  - [ ] 12.1 Create authentication components
    - Build `RegisterForm` component: username, password, demographics inputs
    - Build `LoginForm` component: username, password inputs
    - Implement form validation and error display
    - Add language selector on registration page
    - _Requirements: 1.1, 1.2, 10.1_
  
  - [ ] 12.2 Create dashboard component
    - Build `Dashboard` component: display recovery streak, completed flows, relapse risk
    - Build `ProgressChart` component: visualize relapse risk trends
    - Build `MilestoneCard` component: show achievements and milestones
    - Implement data fetching from backend APIs
    - Add privacy protection for sensitive data display
    - _Requirements: 9.1, 9.2, 9.5_
  
  - [ ]* 12.3 Write property test for dashboard data completeness
    - **Property 22: Dashboard Data Completeness**
    - **Property 23: Progress Data Privacy Protection**
    - **Validates: Requirements 9.1, 9.5**
  
  - [ ] 12.4 Create recovery flow component
    - Build `RecoveryFlow` component: display daily flow with exercises
    - Build `ExerciseCard` component: show individual exercise instructions
    - Implement flow completion tracking with progress bar
    - Add celebration animation for streak milestones
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [ ] 12.5 Create chatbot component
    - Build `Chatbot` component: message input, conversation display
    - Build `MessageBubble` component: user and bot message styling
    - Implement Firebase realtime message listener
    - Add typing indicator and message timestamps
    - Implement crisis detection UI with SOS trigger
    - _Requirements: 3.1, 3.2, 3.3, 12.1_
  
  - [ ] 12.6 Create SOS component
    - Build `SOSButton` component: prominent emergency button
    - Build `SOSModal` component: display coping strategies and resources
    - Build `CrisisResourceCard` component: show helpline information
    - Implement NMK center display with directions link
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ] 12.7 Create NMK lookup component
    - Build `NMKSearch` component: location input and search button
    - Build `NMKList` component: display search results
    - Build `NMKCard` component: show center details with distance
    - Implement Google Maps integration for directions
    - Add offline indicator for cached results
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [ ] 13. Implement offline functionality and PWA features
  - [ ] 13.1 Set up service worker for offline caching
    - Create service worker to cache static assets
    - Implement cache-first strategy for recovery flows and NMK data
    - Implement network-first strategy for chatbot and predictions
    - Add offline page with limited functionality message
    - _Requirements: 8.5_
  
  - [ ]* 13.2 Write property test for offline functionality
    - **Property 21: Offline Functionality Preservation**
    - **Validates: Requirements 8.5**
  
  - [ ] 13.3 Configure PWA manifest and icons
    - Create `manifest.json` with app metadata
    - Generate app icons for various sizes
    - Add install prompt for mobile users
    - Configure theme colors and display mode
    - _Requirements: 8.1, 8.5_
  
  - [ ] 13.4 Implement progressive loading and low-bandwidth optimization
    - Add lazy loading for images and components
    - Implement skeleton screens for loading states
    - Add bandwidth detection and automatic quality adjustment
    - Compress all assets and enable gzip compression
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 14. Checkpoint - Ensure frontend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Implement integration and end-to-end flows
  - [ ] 15.1 Wire authentication flow end-to-end
    - Connect RegisterForm to Auth Service API
    - Connect LoginForm to Auth Service API
    - Implement JWT token storage and refresh
    - Add protected route middleware
    - _Requirements: 1.1, 1.2_
  
  - [ ] 15.2 Wire recovery flow end-to-end
    - Connect Dashboard to Recovery Service API
    - Connect RecoveryFlow component to flow completion API
    - Implement streak update and milestone display
    - Add progress data visualization
    - _Requirements: 4.1, 4.2, 9.1_
  
  - [ ] 15.3 Wire chatbot flow end-to-end
    - Connect Chatbot component to Chatbot Service API
    - Implement Firebase realtime message streaming
    - Add crisis detection and SOS escalation
    - Store conversation history
    - _Requirements: 3.1, 3.2, 3.3, 12.1_
  
  - [ ] 15.4 Wire relapse prediction flow end-to-end
    - Connect Dashboard to ML Service API
    - Display risk score with explanation
    - Implement high-risk intervention triggers
    - Add language-specific prediction display
    - _Requirements: 2.1, 2.2, 2.3, 2.5_
  
  - [ ] 15.5 Wire SOS flow end-to-end
    - Connect SOSButton to SOS Service API
    - Display crisis resources and coping strategies
    - Integrate NMK search for nearby centers
    - Implement follow-up scheduling
    - _Requirements: 5.1, 5.2, 5.3, 5.5_
  
  - [ ] 15.6 Wire NMK lookup flow end-to-end
    - Connect NMKSearch to NMK Service API
    - Display search results with distance sorting
    - Implement Google Maps directions integration
    - Add caching for offline access
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [ ]* 15.7 Write integration tests for critical paths
    - Test complete user registration and login flow
    - Test chatbot conversation with crisis detection
    - Test SOS trigger to resource delivery
    - Test daily flow completion to streak update
    - Test relapse prediction to user display
    - _Requirements: 1.1, 3.3, 5.1, 4.2, 2.1_

- [ ] 16. Implement error handling and resilience
  - [ ] 16.1 Add comprehensive error handling to all backend services
    - Implement retry logic with exponential backoff for external APIs
    - Add fallback mechanisms for service failures (cached data, default responses)
    - Implement circuit breaker pattern for Gemini and Maps APIs
    - Add detailed error logging with context
    - _Requirements: All error handling requirements_
  
  - [ ] 16.2 Add error handling to frontend components
    - Implement error boundaries for React components
    - Add user-friendly error messages in user's language
    - Implement automatic retry for failed requests
    - Add offline detection and messaging
    - _Requirements: 8.1, 8.5_
  
  - [ ]* 16.3 Write unit tests for error scenarios
    - Test all error handling paths defined in design
    - Test API timeout handling
    - Test network failure recovery
    - Test data validation errors
    - _Requirements: All error handling requirements_

- [ ] 17. Implement security and privacy features
  - [ ] 17.1 Add comprehensive input validation and sanitization
    - Implement input validation for all API endpoints
    - Add SQL injection and XSS protection
    - Implement rate limiting on all endpoints
    - Add CSRF protection for state-changing operations
    - _Requirements: 7.1, 7.2_
  
  - [ ] 17.2 Implement PII detection and anonymization
    - Create PII detection utility (phone numbers, addresses, names)
    - Add anonymization logic for conversations and user data
    - Implement data masking for sensitive fields
    - Add warning when PII is detected in user input
    - _Requirements: 7.3, 11.5_
  
  - [ ]* 17.3 Write property tests for privacy features
    - **Property 18: Conversation PII Anonymization**
    - **Property 23: Progress Data Privacy Protection**
    - **Validates: Requirements 7.3, 9.5**
  
  - [ ] 17.4 Implement data deletion and user rights
    - Create data deletion endpoint for user requests
    - Implement complete data removal across all collections
    - Add data export functionality for user data portability
    - Implement consent management
    - _Requirements: 7.4, 7.5_

- [ ] 18. Final checkpoint and testing
  - [ ] 18.1 Run all property-based tests with 100+ iterations
    - Verify all 27 correctness properties pass
    - Check for any failing test cases or counterexamples
    - Fix any bugs discovered by property tests
    - _Requirements: All requirements_
  
  - [ ] 18.2 Run all unit tests and integration tests
    - Ensure 80%+ code coverage across all services
    - Verify all edge cases and error scenarios pass
    - Test all integration paths end-to-end
    - _Requirements: All requirements_
  
  - [ ] 18.3 Perform manual testing of critical flows
    - Test complete user journey from registration to recovery tracking
    - Test chatbot conversations in Hindi, Hinglish, and English
    - Test SOS flow with crisis detection
    - Test offline functionality and PWA features
    - Test on slow network connections (2G simulation)
    - _Requirements: All requirements_
  
  - [ ] 18.4 Performance and load testing
    - Test chatbot response times under load
    - Test LSTM prediction performance with batch processing
    - Test Firebase realtime performance with concurrent users
    - Verify low-bandwidth optimization effectiveness
    - _Requirements: 3.1, 5.1, 8.1, 12.1_
  
  - [ ] 18.5 Security and accessibility testing
    - Run security scan for vulnerabilities
    - Test WCAG 2.1 Level AA compliance
    - Test screen reader compatibility
    - Verify encryption and data protection
    - _Requirements: 7.1, 7.2, 7.3_

- [ ] 19. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional property-based and unit tests that can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties with randomized inputs (100+ iterations)
- Unit tests validate specific examples, edge cases, and error conditions
- Integration tests verify end-to-end flows across all system layers
- The implementation follows a bottom-up approach: data layer → services → APIs → frontend → integration
- All code should include inline comments explaining complex logic
- All APIs should include request/response validation
- All services should include comprehensive error handling
- Security and privacy are integrated throughout, not added at the end
