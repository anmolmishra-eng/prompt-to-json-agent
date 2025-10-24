"""
Production Secret Manager - Multi-Cloud Support
Supports: AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
Fallback: Environment variables (dev only)
"""
import os
import logging
from typing import Optional, Dict
from enum import Enum

logger = logging.getLogger(__name__)

class SecretProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ENV = "env"  # Development fallback only

class SecretManager:
    def __init__(self):
        self.provider = self._detect_provider()
        self._client = None
        self._cache: Dict[str, str] = {}
        
    def _detect_provider(self) -> SecretProvider:
        """Auto-detect cloud provider from environment"""
        if os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"):
            return SecretProvider.AWS
        elif os.getenv("AZURE_KEY_VAULT_URL"):
            return SecretProvider.AZURE
        elif os.getenv("GCP_PROJECT_ID"):
            return SecretProvider.GCP
        else:
            logger.warning("⚠️ No cloud provider detected. Using ENV fallback (NOT for production)")
            return SecretProvider.ENV
    
    def get_secret(self, secret_name: str) -> str:
        """Fetch secret from configured provider"""
        if secret_name in self._cache:
            return self._cache[secret_name]
        
        if self.provider == SecretProvider.AWS:
            value = self._get_aws_secret(secret_name)
        elif self.provider == SecretProvider.AZURE:
            value = self._get_azure_secret(secret_name)
        elif self.provider == SecretProvider.GCP:
            value = self._get_gcp_secret(secret_name)
        else:
            value = self._get_env_secret(secret_name)
        
        if value:
            self._cache[secret_name] = value
        return value
    
    def _get_aws_secret(self, secret_name: str) -> str:
        """Fetch from AWS Secrets Manager"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            if not self._client:
                region = os.getenv("AWS_REGION", "us-east-1")
                self._client = boto3.client("secretsmanager", region_name=region)
            
            response = self._client.get_secret_value(SecretId=secret_name)
            logger.info(f"✅ Retrieved secret '{secret_name}' from AWS Secrets Manager")
            return response["SecretString"]
        except ImportError:
            logger.error("❌ boto3 not installed. Run: pip install boto3")
            return self._get_env_secret(secret_name)
        except ClientError as e:
            logger.error(f"❌ AWS Secrets Manager error: {e}")
            return self._get_env_secret(secret_name)
    
    def _get_azure_secret(self, secret_name: str) -> str:
        """Fetch from Azure Key Vault"""
        try:
            from azure.keyvault.secrets import SecretClient
            from azure.identity import DefaultAzureCredential
            
            if not self._client:
                vault_url = os.getenv("AZURE_KEY_VAULT_URL")
                credential = DefaultAzureCredential()
                self._client = SecretClient(vault_url=vault_url, credential=credential)
            
            secret = self._client.get_secret(secret_name)
            logger.info(f"✅ Retrieved secret '{secret_name}' from Azure Key Vault")
            return secret.value
        except ImportError:
            logger.error("❌ Azure SDK not installed. Run: pip install azure-keyvault-secrets azure-identity")
            return self._get_env_secret(secret_name)
        except Exception as e:
            logger.error(f"❌ Azure Key Vault error: {e}")
            return self._get_env_secret(secret_name)
    
    def _get_gcp_secret(self, secret_name: str) -> str:
        """Fetch from GCP Secret Manager"""
        try:
            from google.cloud import secretmanager
            
            if not self._client:
                self._client = secretmanager.SecretManagerServiceClient()
            
            project_id = os.getenv("GCP_PROJECT_ID")
            name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
            response = self._client.access_secret_version(request={"name": name})
            logger.info(f"✅ Retrieved secret '{secret_name}' from GCP Secret Manager")
            return response.payload.data.decode("UTF-8")
        except ImportError:
            logger.error("❌ GCP SDK not installed. Run: pip install google-cloud-secret-manager")
            return self._get_env_secret(secret_name)
        except Exception as e:
            logger.error(f"❌ GCP Secret Manager error: {e}")
            return self._get_env_secret(secret_name)
    
    def _get_env_secret(self, secret_name: str) -> str:
        """Fallback to environment variables (dev only)"""
        value = os.getenv(secret_name)
        if value:
            logger.warning(f"⚠️ Using ENV fallback for '{secret_name}' - NOT PRODUCTION SAFE")
        else:
            logger.error(f"❌ Secret '{secret_name}' not found in any provider")
        return value or ""

# Global singleton instance
_secret_manager = SecretManager()

def get_secret(secret_name: str) -> str:
    """Public API to fetch secrets"""
    return _secret_manager.get_secret(secret_name)

def get_provider() -> str:
    """Get current provider name"""
    return _secret_manager.provider.value
