"""
Secret Manager - Azure Key Vault Implementation
Replace .env files with secure secret management
"""
import os
from typing import Optional
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class SecretManager:
    """Secure secret management using Azure Key Vault"""
    
    def __init__(self):
        self.vault_url = os.getenv(
            "AZURE_KEY_VAULT_URL",
            "https://your-keyvault-name.vault.azure.net/"
        )
        
        try:
            # Use DefaultAzureCredential for automatic auth
            # (works with managed identity in production)
            credential = DefaultAzureCredential()
            self.client = SecretClient(
                vault_url=self.vault_url,
                credential=credential
            )
            logger.info("Secret Manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Secret Manager: {e}")
            raise
    
    @lru_cache(maxsize=50)
    def get_secret(self, secret_name: str, default: Optional[str] = None) -> str:
        """
        Retrieve secret from Key Vault with caching
        
        Args:
            secret_name: Name of the secret in Key Vault
            default: Default value if secret not found
            
        Returns:
            Secret value as string
        """
        try:
            secret = self.client.get_secret(secret_name)
            logger.info(f"Successfully retrieved secret: {secret_name}")
            return secret.value
        except Exception as e:
            logger.warning(f"Failed to get secret {secret_name}: {e}")
            if default is not None:
                logger.info(f"Using default value for {secret_name}")
                return default
            raise
    
    def set_secret(self, secret_name: str, secret_value: str) -> None:
        """
        Store a secret in Key Vault
        
        Args:
            secret_name: Name of the secret
            secret_value: Value to store
        """
        try:
            self.client.set_secret(secret_name, secret_value)
            logger.info(f"Successfully stored secret: {secret_name}")
            # Clear cache for this secret
            self.get_secret.cache_clear()
        except Exception as e:
            logger.error(f"Failed to set secret {secret_name}: {e}")
            raise

# Global instance
secret_manager = SecretManager()

# Convenience function
def get_secret(name: str, default: Optional[str] = None) -> str:
    """Get secret from Key Vault"""
    return secret_manager.get_secret(name, default)


# ========== AWS SECRETS MANAGER VERSION ==========
"""
import boto3
from botocore.exceptions import ClientError
import json

class AWSSecretManager:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    
    @lru_cache(maxsize=50)
    def get_secret(self, secret_name: str, default: Optional[str] = None) -> str:
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            
            # Handle both string and JSON secrets
            if 'SecretString' in response:
                secret = response['SecretString']
                try:
                    return json.loads(secret)
                except json.JSONDecodeError:
                    return secret
            else:
                return base64.b64decode(response['SecretBinary'])
                
        except ClientError as e:
            logger.warning(f"Failed to get secret {secret_name}: {e}")
            if default is not None:
                return default
            raise
"""
