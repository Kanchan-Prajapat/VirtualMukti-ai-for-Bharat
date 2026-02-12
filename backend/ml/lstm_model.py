"""LSTM model for relapse risk prediction"""

import numpy as np
# from tensorflow import keras
# from tensorflow.keras import layers
import logging

logger = logging.getLogger(__name__)


class LSTMRelapseModel:
    """LSTM model for predicting relapse risk"""
    
    SEQUENCE_LENGTH = 30  # 30 days of history
    FEATURES = [
        'mood_score',
        'craving_intensity',
        'triggers_count',
        'flows_completed',
        'chatbot_engagement',
        'recovery_streak'
    ]
    NUM_FEATURES = len(FEATURES)
    
    def __init__(self):
        self.model = None
        self.is_trained = False
    
    def build_model(self):
        """Build LSTM architecture"""
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=(self.SEQUENCE_LENGTH, self.NUM_FEATURES)),
            
            # First LSTM layer
            layers.LSTM(64, return_sequences=True, dropout=0.2),
            
            # Second LSTM layer
            layers.LSTM(32, dropout=0.2),
            
            # Dense layers
            layers.Dense(16, activation='relu'),
            layers.Dropout(0.2),
            
            # Output layer (risk score 0-100)
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        logger.info("LSTM model built successfully")
        return model
    
    def train_with_synthetic_data(self, num_samples=1000):
        """Train model with synthetic data for MVP"""
        logger.info(f"Generating {num_samples} synthetic training samples...")
        
        # Generate synthetic training data
        X_train = []
        y_train = []
        
        for _ in range(num_samples):
            # Generate 30-day sequence
            sequence = []
            
            # Random baseline values
            base_mood = np.random.uniform(4, 8)
            base_craving = np.random.uniform(2, 7)
            base_streak = np.random.randint(0, 90)
            
            for day in range(self.SEQUENCE_LENGTH):
                # Add some temporal variation
                mood = np.clip(base_mood + np.random.normal(0, 1), 1, 10)
                craving = np.clip(base_craving + np.random.normal(0, 1), 1, 10)
                triggers = np.random.poisson(2)
                flows = np.random.binomial(1, 0.7)
                chatbot = np.random.poisson(1)
                streak = min(base_streak + day, 365)
                
                sequence.append([
                    mood,
                    craving,
                    triggers,
                    flows,
                    chatbot,
                    streak
                ])
            
            X_train.append(sequence)
            
            # Calculate risk score based on features
            avg_mood = np.mean([s[0] for s in sequence])
            avg_craving = np.mean([s[1] for s in sequence])
            avg_triggers = np.mean([s[2] for s in sequence])
            avg_flows = np.mean([s[3] for s in sequence])
            
            # Simple risk calculation
            risk = (
                (10 - avg_mood) * 10 +  # Low mood increases risk
                avg_craving * 8 +  # High craving increases risk
                avg_triggers * 5 +  # More triggers increase risk
                (1 - avg_flows) * 15  # Fewer flows increase risk
            )
            risk = np.clip(risk / 100, 0, 1)  # Normalize to 0-1
            
            y_train.append(risk)
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        logger.info(f"Training data shape: X={X_train.shape}, y={y_train.shape}")
        
        # Build model if not exists
        if self.model is None:
            self.build_model()
        
        # Train model
        logger.info("Training LSTM model...")
        history = self.model.fit(
            X_train,
            y_train,
            epochs=20,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        self.is_trained = True
        logger.info(f"Model trained. Final loss: {history.history['loss'][-1]:.4f}")
        
        return history
    
    def predict(self, sequence: np.ndarray) -> float:
        """
        Predict relapse risk from 30-day sequence
        
        Args:
            sequence: Array of shape (30, 6) with features
            
        Returns:
            Risk score 0-100
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train_with_synthetic_data() first.")
        
        # Ensure correct shape
        if sequence.shape != (self.SEQUENCE_LENGTH, self.NUM_FEATURES):
            raise ValueError(f"Expected shape ({self.SEQUENCE_LENGTH}, {self.NUM_FEATURES}), got {sequence.shape}")
        
        # Add batch dimension
        sequence_batch = np.expand_dims(sequence, axis=0)
        
        # Predict
        prediction = self.model.predict(sequence_batch, verbose=0)[0][0]
        
        # Convert to 0-100 scale
        risk_score = float(prediction * 100)
        
        return risk_score
    
    def get_feature_importance(self, sequence: np.ndarray) -> list:
        """
        Simple feature importance based on recent values
        
        Args:
            sequence: Array of shape (30, 6)
            
        Returns:
            List of (feature_name, importance, value) tuples
        """
        # Get recent 7-day averages
        recent_data = sequence[-7:]
        
        feature_values = []
        for i, feature_name in enumerate(self.FEATURES):
            avg_value = np.mean(recent_data[:, i])
            feature_values.append((feature_name, avg_value))
        
        # Calculate importance based on contribution to risk
        importances = []
        
        # Mood (lower is worse)
        mood_val = feature_values[0][1]
        mood_importance = (10 - mood_val) / 10
        importances.append(('mood_score', mood_importance, mood_val))
        
        # Craving (higher is worse)
        craving_val = feature_values[1][1]
        craving_importance = craving_val / 10
        importances.append(('craving_intensity', craving_importance, craving_val))
        
        # Triggers (higher is worse)
        triggers_val = feature_values[2][1]
        triggers_importance = min(triggers_val / 5, 1.0)
        importances.append(('triggers_count', triggers_importance, triggers_val))
        
        # Flows (lower is worse)
        flows_val = feature_values[3][1]
        flows_importance = (1 - flows_val)
        importances.append(('flows_completed', flows_importance, flows_val))
        
        # Chatbot (lower is worse)
        chatbot_val = feature_values[4][1]
        chatbot_importance = max(0, (2 - chatbot_val) / 2)
        importances.append(('chatbot_engagement', chatbot_importance, chatbot_val))
        
        # Streak (lower is worse)
        streak_val = feature_values[5][1]
        streak_importance = max(0, (30 - streak_val) / 30)
        importances.append(('recovery_streak', streak_importance, streak_val))
        
        # Sort by importance
        importances.sort(key=lambda x: x[1], reverse=True)
        
        return importances


# Global model instance
lstm_model = LSTMRelapseModel()
