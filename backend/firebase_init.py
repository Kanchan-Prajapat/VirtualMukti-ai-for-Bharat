# """Firebase initialization for realtime features"""

# import firebase_admin
# from firebase_admin import credentials, db
# import logging
# from .config import settings

# logger = logging.getLogger(__name__)


# class FirebaseService:
#     """Firebase Realtime Database service"""
    
#     _initialized = False
    
#     @classmethod
#     def initialize(cls):
#         """Initialize Firebase Admin SDK"""
#         if cls._initialized:
#             logger.info("Firebase already initialized")
#             return
        
#         try:
#             # Initialize Firebase with service account credentials
#             cred = credentials.Certificate(settings.firebase_credentials_path)
#             firebase_admin.initialize_app(cred, {
#                 'databaseURL': settings.firebase_database_url
#             })
#             cls._initialized = True
#             logger.info("Firebase initialized successfully")
#         except Exception as e:
#             logger.error(f"Failed to initialize Firebase: {e}")
#             raise
    
#     @classmethod
#     def get_reference(cls, path: str):
#         """
#         Get Firebase database reference
        
#         Args:
#             path: Database path (e.g., 'chats/user123')
            
#         Returns:
#             Firebase database reference
#         """
#         if not cls._initialized:
#             cls.initialize()
#         return db.reference(path)
    
#     @classmethod
#     def push_message(cls, user_id: str, message: dict):
#         """
#         Push message to user's chat in Firebase
        
#         Args:
#             user_id: User identifier
#             message: Message dictionary with content, sender, timestamp
#         """
#         ref = cls.get_reference(f'chats/{user_id}/messages')
#         ref.push(message)
    
#     @classmethod
#     def get_messages(cls, user_id: str, limit: int = 50):
#         """
#         Get recent messages for user
        
#         Args:
#             user_id: User identifier
#             limit: Maximum number of messages to retrieve
            
#         Returns:
#             List of messages
#         """
#         ref = cls.get_reference(f'chats/{user_id}/messages')
#         return ref.order_by_child('timestamp').limit_to_last(limit).get()


# # Global Firebase service instance
# firebase_service = FirebaseService()


import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    def initialize(self):
        logger.warning("Firebase is disabled (MVP mode)")

firebase_service = FirebaseService()
