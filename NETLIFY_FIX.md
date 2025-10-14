# Netlify Deployment Fix

## Issue
The frontend was calling `/auth/signup` but the backend API expects `/api/v1/auth/signup`.

## Root Cause
The `VITE_API_URL` environment variable in Netlify was set to `https://closealead.onrender.com` without the `/api/v1` path prefix.

## Solution

### 1. Update Netlify Environment Variable
Go to your Netlify dashboard:
1. Navigate to **Site settings** → **Environment variables**
2. Update `VITE_API_URL` from:
   ```
   https://closealead.onrender.com
   ```
   to:
   ```
   https://closealead.onrender.com/api/v1
   ```

### 2. Redeploy
After updating the environment variable, trigger a new deployment:
- Go to **Deploys** → **Trigger deploy** → **Deploy site**

## What Changed

### netlify.toml
Updated the proxy redirect to properly forward API requests:
```toml
[[redirects]]
  from = "/api/*"
  to = "https://closealead.onrender.com/api/:splat"
  status = 200
  force = true
```

### .env.example
Updated the example to show the correct format:
```
VITE_API_URL=http://localhost:8000/api/v1
```

## Verification
After redeploying, the signup request should go to:
- **Correct**: `https://closealead.onrender.com/api/v1/auth/signup` ✅

Instead of:
- **Incorrect**: `https://closealead.onrender.com/auth/signup` ❌
