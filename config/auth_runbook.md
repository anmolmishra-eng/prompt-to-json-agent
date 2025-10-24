# Authentication & Secret Management Runbook

## Secret Management

### Azure Key Vault Setup

1. **Create Key Vault**:
   ```bash
   az keyvault create \
     --name your-keyvault-name \
     --resource-group your-resource-group \
     --location eastus
   ```

2. **Store Secrets**:
   ```bash
   az keyvault secret set --vault-name your-keyvault-name \
     --name API-KEY --value "your-api-key"

   az keyvault secret set --vault-name your-keyvault-name \
     --name JWT-SECRET-KEY --value "your-jwt-secret"

   az keyvault secret set --vault-name your-keyvault-name \
     --name SUPABASE-URL --value "your-supabase-url"

   az keyvault secret set --vault-name your-keyvault-name \
     --name SUPABASE-KEY --value "your-supabase-key"

   az keyvault secret set --vault-name your-keyvault-name \
     --name YOTTA-API-KEY --value "your-yotta-api-key"
   ```

3. **Configure Access Policy**:
   ```bash
   az keyvault set-policy \
     --name your-keyvault-name \
     --object-id <your-app-identity-object-id> \
     --secret-permissions get list
   ```

4. **Set Environment Variable**:
   ```bash
   export AZURE_KEY_VAULT_URL=https://your-keyvault-name.vault.azure.net/
   ```

### AWS Secrets Manager Setup (Alternative)

1. **Create Secrets**:
   ```bash
   aws secretsmanager create-secret --name API_KEY --secret-string "your-api-key"
   aws secretsmanager create-secret --name JWT_SECRET_KEY --secret-string "your-jwt-secret"
   aws secretsmanager create-secret --name SUPABASE_URL --secret-string "your-supabase-url"
   aws secretsmanager create-secret --name SUPABASE_KEY --secret-string "your-supabase-key"
   ```

2. **Set Environment Variable**:
   ```bash
   export AWS_REGION=us-east-1
   ```

## Local Development

For local development, use environment variables:

```bash
export API_KEY=dev-key
export JWT_SECRET_KEY=dev-secret
export SUPABASE_URL=your-local-supabase-url
export SUPABASE_KEY=your-local-supabase-key
```

## Production Deployment

1. Enable managed identity for your app service
2. Grant Key Vault access to the managed identity
3. Set `AZURE_KEY_VAULT_URL` environment variable
4. Application will automatically authenticate using managed identity

## Troubleshooting

- **Secret not found**: Verify secret name matches exactly (case-sensitive)
- **Access denied**: Check access policy includes `get` and `list` permissions
- **Authentication failed**: Ensure managed identity is enabled and configured
