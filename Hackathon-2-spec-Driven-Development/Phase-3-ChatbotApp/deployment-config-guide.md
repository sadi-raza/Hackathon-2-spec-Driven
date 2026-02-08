# Production Configuration Guide

## Backend Environment Variables
Set these environment variables in your deployed backend (VPS, Heroku, etc.):

```
DATABASE_URL=your_postgresql_database_url
JWT_SECRET=your_secure_jwt_secret
CORS_ORIGINS=https://chatbot-todoapp.vercel.app,http://localhost:3000
DEBUG=false
COHERE_API_KEY=your_cohere_api_key
```

## Frontend Environment Variables
Set these environment variables in your Vercel deployment:

```
NEXT_PUBLIC_API_URL=https://your-deployed-backend-url/api
NEXT_PUBLIC_CHATBOT_ENABLED=true
```

## Common Deployment Issues and Fixes:

### 1. Sign-in not working after deployment
- **Issue**: CORS error preventing frontend from communicating with backend
- **Solution**: Ensure CORS_ORIGINS includes your frontend URL (https://chatbot-todoapp.vercel.app)

### 2. API requests failing
- **Issue**: Frontend pointing to localhost instead of deployed backend
- **Solution**: Update NEXT_PUBLIC_API_URL to your live backend URL

### 3. Authentication failures
- **Issue**: Different domains causing issues with token handling
- **Solution**: Ensure both frontend and backend are properly configured for cross-origin requests

## Local Development vs Production:
- For local development: CORS_ORIGINS=http://localhost:3000, NEXT_PUBLIC_API_URL=http://localhost:8000/api
- For production: CORS_ORIGINS=https://chatbot-todoapp.vercel.app, NEXT_PUBLIC_API_URL=https://your-backend-url/api