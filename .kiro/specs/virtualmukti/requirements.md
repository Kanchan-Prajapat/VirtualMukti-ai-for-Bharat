# Requirements Document: VirtualMukti

## Introduction

VirtualMukti is an AI-powered addiction recovery platform designed to support individuals in India (ages 18-45) struggling with alcohol, cannabis, and opioid addiction. The platform prioritizes user privacy, accessibility for rural and Tier 2/3 city users, and evidence-based recovery support through AI-driven interventions. The MVP focuses on anonymous onboarding, relapse risk prediction, CBT-based chatbot support, daily recovery tracking, emergency SOS features, and rehabilitation center lookup.

## Glossary

- **System**: The VirtualMukti platform (web application, backend services, and AI models)
- **User**: An individual seeking addiction recovery support (18-45 years old)
- **Recovery_Flow**: A structured daily activity or exercise designed to support recovery
- **Relapse_Risk_Score**: A numerical prediction (0-100) indicating likelihood of relapse
- **CBT_Chatbot**: Cognitive Behavioral Therapy chatbot powered by Gemini 3 Flash
- **NMK**: Nasha Mukti Kendra (rehabilitation center)
- **SOS_Request**: An emergency support request triggered by a user in crisis
- **LSTM_Model**: Long Short-Term Memory neural network for relapse prediction
- **Anonymous_Session**: User session without phone number or Aadhaar verification
- **Recovery_Streak**: Consecutive days of sobriety tracked by the system
- **Trigger_Event**: A situation or condition that increases relapse risk

## Requirements

### Requirement 1: Anonymous User Onboarding

**User Story:** As a user seeking recovery support, I want to create an account anonymously without providing phone number or Aadhaar, so that I can access help without fear of stigma or privacy concerns.

#### Acceptance Criteria

1. WHEN a new user accesses the registration page, THE System SHALL display an anonymous registration form without phone number or Aadhaar fields
2. WHEN a user submits registration with only username and password, THE System SHALL create an Anonymous_Session and grant access to the platform
3. WHEN a user provides basic demographic information (age, gender, location, addiction type), THE System SHALL store this data encrypted in MongoDB
4. THE System SHALL NOT require phone number verification or Aadhaar verification for account creation
5. WHEN a user completes registration, THE System SHALL generate a unique anonymous identifier for the user

### Requirement 2: Relapse Risk Prediction

**User Story:** As a user in recovery, I want to receive daily relapse risk predictions, so that I can understand my vulnerability and take preventive actions.

#### Acceptance Criteria

1. WHEN a user logs in daily, THE LSTM_Model SHALL analyze user activity data and generate a Relapse_Risk_Score
2. WHEN the LSTM_Model generates a prediction, THE System SHALL provide an explainable output showing key factors contributing to the risk score
3. WHEN a Relapse_Risk_Score exceeds 70, THE System SHALL trigger proactive interventions (notifications, chatbot check-ins)
4. THE System SHALL update the LSTM_Model with new user data to improve prediction accuracy over time
5. WHEN displaying risk predictions, THE System SHALL present the information in Hindi or Hinglish based on user preference

### Requirement 3: CBT Chatbot Support

**User Story:** As a user experiencing cravings or emotional distress, I want to chat with an AI counselor in Hindi/Hinglish, so that I can receive immediate support in my preferred language.

#### Acceptance Criteria

1. WHEN a user initiates a chat session, THE CBT_Chatbot SHALL respond within 3 seconds using Gemini 3 Flash
2. WHEN a user sends a message in Hindi or Hinglish, THE CBT_Chatbot SHALL respond appropriately in the same language
3. WHEN the CBT_Chatbot detects crisis language (suicidal ideation, severe distress), THE System SHALL escalate to SOS_Request handling
4. THE CBT_Chatbot SHALL apply evidence-based CBT techniques in conversations (cognitive reframing, behavioral activation, coping strategies)
5. WHEN a chat session ends, THE System SHALL store the conversation encrypted in MongoDB for continuity of care

### Requirement 4: Daily Recovery Flows

**User Story:** As a user committed to recovery, I want to complete daily recovery exercises and track my progress, so that I can build healthy habits and maintain sobriety.

#### Acceptance Criteria

1. WHEN a user accesses the daily flow section, THE System SHALL present a personalized Recovery_Flow based on addiction type and recovery stage
2. WHEN a user completes a Recovery_Flow, THE System SHALL update the user's Recovery_Streak and store completion data
3. WHEN a user maintains a Recovery_Streak for 7 consecutive days, THE System SHALL provide positive reinforcement and milestone recognition
4. THE System SHALL offer Recovery_Flows in Hindi and Hinglish with low-bandwidth optimized content
5. WHEN a user misses a daily flow, THE System SHALL send a gentle reminder notification without judgment

### Requirement 5: SOS Emergency Support

**User Story:** As a user in crisis or experiencing intense cravings, I want to access immediate emergency support, so that I can get help when I need it most.

#### Acceptance Criteria

1. WHEN a user triggers an SOS_Request, THE System SHALL immediately connect the user to crisis resources within 5 seconds
2. WHEN an SOS_Request is triggered, THE System SHALL provide immediate coping strategies and grounding exercises
3. WHEN an SOS_Request is active, THE System SHALL offer options to contact nearby NMK centers or helplines
4. THE System SHALL log all SOS_Request events for follow-up care and pattern analysis
5. WHEN an SOS_Request is resolved, THE System SHALL schedule a follow-up check-in within 24 hours

### Requirement 6: Nasha Mukti Kendra Lookup

**User Story:** As a user considering professional treatment, I want to find nearby rehabilitation centers, so that I can access in-person care when needed.

#### Acceptance Criteria

1. WHEN a user searches for NMK centers, THE System SHALL query Google Maps API and return results within 50km radius
2. WHEN displaying NMK results, THE System SHALL show center name, address, distance, contact information, and services offered
3. WHEN a user selects an NMK center, THE System SHALL provide directions using Google Maps integration
4. THE System SHALL cache NMK data to support low-bandwidth access in rural areas
5. WHEN NMK data is unavailable, THE System SHALL display cached results with a staleness indicator

### Requirement 7: Privacy and Data Security

**User Story:** As a user concerned about privacy, I want my data to be protected and anonymous, so that I can use the platform without fear of exposure or discrimination.

#### Acceptance Criteria

1. THE System SHALL encrypt all user data at rest in MongoDB using AES-256 encryption
2. THE System SHALL encrypt all data in transit using TLS 1.3
3. WHEN storing user conversations, THE System SHALL anonymize personally identifiable information
4. THE System SHALL NOT share user data with third parties without explicit consent
5. WHEN a user requests data deletion, THE System SHALL permanently remove all associated data within 48 hours

### Requirement 8: Low Bandwidth Optimization

**User Story:** As a user in a rural area with limited internet connectivity, I want the platform to work on slow connections, so that I can access support regardless of network quality.

#### Acceptance Criteria

1. WHEN a user accesses the platform on a connection slower than 2G, THE System SHALL load core features within 10 seconds
2. THE System SHALL compress images and media to reduce bandwidth consumption by at least 60%
3. WHEN network connectivity is poor, THE System SHALL prioritize loading essential features (chatbot, SOS) over non-critical content
4. THE System SHALL implement progressive loading for content-heavy pages
5. WHEN offline, THE System SHALL cache critical resources and allow limited functionality (viewing past conversations, offline exercises)

### Requirement 9: User Progress Tracking

**User Story:** As a user in recovery, I want to track my progress over time, so that I can see my improvement and stay motivated.

#### Acceptance Criteria

1. WHEN a user views their dashboard, THE System SHALL display Recovery_Streak, completed flows, and relapse risk trends
2. WHEN a user achieves a milestone (7, 30, 90 days sober), THE System SHALL provide celebratory feedback and encouragement
3. THE System SHALL visualize progress data using charts and graphs optimized for low-bandwidth viewing
4. WHEN a user experiences a setback, THE System SHALL reframe it as a learning opportunity and adjust recovery plans
5. WHEN displaying progress data, THE System SHALL protect user privacy by not exposing sensitive information in screenshots or shared views

### Requirement 10: Multi-Language Support

**User Story:** As a user more comfortable with Hindi or Hinglish, I want to use the platform in my preferred language, so that I can fully understand and engage with the content.

#### Acceptance Criteria

1. WHEN a user first accesses the platform, THE System SHALL detect browser language and offer Hindi, Hinglish, or English
2. WHEN a user selects a language preference, THE System SHALL persist this choice across sessions
3. THE System SHALL provide all core features (chatbot, recovery flows, UI elements) in the selected language
4. WHEN translating content, THE System SHALL maintain cultural sensitivity and use appropriate terminology for Indian context
5. WHEN a user switches languages mid-session, THE System SHALL update the interface without losing session state

### Requirement 11: AI Model Training and Updates

**User Story:** As a system administrator, I want the LSTM model to improve over time with new data, so that predictions become more accurate and personalized.

#### Acceptance Criteria

1. WHEN new user data is collected, THE System SHALL batch process it for LSTM_Model retraining weekly
2. WHEN retraining the LSTM_Model, THE System SHALL validate model performance against a holdout dataset
3. WHEN a new model version achieves better accuracy, THE System SHALL deploy it to production after validation
4. THE System SHALL maintain model versioning and rollback capability in case of performance degradation
5. WHEN training models, THE System SHALL ensure data anonymization and privacy compliance

### Requirement 12: Firebase Realtime Features

**User Story:** As a user engaging with the chatbot, I want to receive responses in real-time, so that the conversation feels natural and supportive.

#### Acceptance Criteria

1. WHEN a user sends a message to the CBT_Chatbot, THE System SHALL use Firebase to deliver the response in real-time
2. WHEN multiple users are active, THE System SHALL maintain separate realtime connections without performance degradation
3. WHEN network connectivity is interrupted, THE System SHALL queue messages and sync when connection is restored
4. THE System SHALL use Firebase for push notifications about daily reminders and check-ins
5. WHEN a user is inactive for 5 minutes during a chat, THE System SHALL send a gentle prompt to continue the conversation
