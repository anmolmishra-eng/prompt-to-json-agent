# Authentication Runbook

## 🔐 Secret Management (CRITICAL)

### ⚠️ PRODUCTION REQUIREMENT
**DO NOT use .env files in production!**

Use platform secret managers:

#### AWS Secrets Manager
```bash
export AWS_REGION=us-east-1
# Secrets: API_KEY, JWT_SECRET, DATABASE_URL
```

#### Azure Key Vault
```bash
export AZURE_KEY_VAULT_URL=https://your-vault.vault.azure.net/
# Secrets: API-KEY, JWT-SECRET, DATABASE-URL
```

#### GCP Secret Manager
```bash
export GCP_PROJECT_ID=your-project-id
# Secrets: API_KEY, JWT_SECRET, DATABASE_URL
```

### Development Only (Local)
```bash
# ⚠️ WARNING: Development fallback only!
JWT_SECRET=your-dev-jwt-secret
API_KEY=your-dev-api-key
DEMO_USERNAME=admin
DEMO_PASSWORD=your-dev-password
```

**See**: [config/SECRETS_SECURITY.md](SECRETS_SECURITY.md) for full setup

## JWT Token Management

### Login Flow
1. POST `/api/v1/auth/login` with username/password
2. Receive JWT token (24h expiry)
3. Include in Authorization header: `Bearer <token>`

### API Key Requirements
- All endpoints require `X-API-Key: bhiv-secret-key-2024`
- Public endpoints: `/health`, `/metrics`
- Auth endpoint: `/api/v1/auth/login` (API key only)

### Token Verification
```python
from src.auth.jwt_middleware import verify_token
# Use as dependency: current_user: str = Depends(verify_token)
```

### Security Headers
```bash
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

### Troubleshooting
- 401 Unauthorized: Check API key and JWT token
- Token expired: Re-login to get new token
- Invalid credentials: Verify DEMO_USERNAME/DEMO_PASSWORD