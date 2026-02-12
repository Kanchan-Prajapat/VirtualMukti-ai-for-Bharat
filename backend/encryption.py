"""AES-256 encryption utilities for sensitive data"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os
from .config import settings


class EncryptionService:
    """AES-256 encryption/decryption service"""
    
    def __init__(self):
        # Convert hex key to bytes (expecting 32-byte key for AES-256)
        self.key = settings.aes_encryption_key.encode()[:32]
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using AES-256-CBC
        
        Args:
            plaintext: String to encrypt
            
        Returns:
            Base64-encoded encrypted string with IV prepended
        """
        # Generate random IV
        iv = os.urandom(16)
        
        # Pad plaintext to block size
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Prepend IV to ciphertext and encode as base64
        encrypted_data = iv + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt AES-256-CBC encrypted text
        
        Args:
            encrypted_text: Base64-encoded encrypted string with IV prepended
            
        Returns:
            Decrypted plaintext string
        """
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_text)
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')


# Global encryption service instance
encryption_service = EncryptionService()
