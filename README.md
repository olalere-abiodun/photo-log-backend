# PhotoLog Backend API

FastAPI backend for PhotoLog - Event photo sharing platform with Firebase authentication.

## Features

- Firebase Authentication (Email/Password + Google Sign-In)
- Token verification and user management
- Admin authentication
- RESTful API endpoints
- CORS enabled for frontend integration

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Firebase Admin SDK** - Token verification and user management
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Firebase Configuration

1. You already have `firebase_account_services.json` - make sure it's in the `backend/` directory
2. The file is already in `.gitignore` to keep it secure

### 3. Environment Variables

Create a `.env` file in the `backend/` directory:

```env
FIREBASE_CREDENTIALS_PATH=./firebase_account_services.json
FRONTEND_URL=http://localhost:5173
ADMIN_EMAILS=admin@photolog.com
```

### 4. Run the Server

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the built-in runner
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Authentication Flow

### How It Works

1. **Frontend** authenticates users via Firebase (Email/Password or Google Sign-In)
2. **Frontend** receives Firebase ID token after successful authentication
3. **Frontend** sends token to backend in `Authorization: Bearer <token>` header or request body
4. **Backend** verifies token using Firebase Admin SDK
5. **Backend** returns user information

### Supported Auth Methods

- ✅ Email/Password signup and signin
- ✅ Google Sign-In (OAuth)
- ✅ Email verification
- ✅ Password reset
- ✅ Token refresh

**Note**: The backend doesn't distinguish between email/password and Google sign-in - both methods return Firebase ID tokens that are verified the same way.

## API Endpoints

### Authentication (`/auth/*`)

- `POST /auth/signup` - Register new user (requires Firebase token)
- `POST /auth/signin` - User login (requires Firebase token)
- `POST /auth/signout` - Sign out
- `POST /auth/refresh` - Refresh authentication token
- `POST /auth/verify-email` - Verify email address
- `POST /auth/resend-verification` - Resend verification email
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password
- `GET /auth/me` - Get current user profile (protected)
- `PATCH /auth/me` - Update user profile (protected)
- `PATCH /auth/me/password` - Change password (protected)

### Admin Authentication (`/admin/auth/*`)

- `POST /admin/auth/signin` - Admin login
- `POST /admin/auth/signout` - Admin sign out
- `POST /admin/auth/refresh` - Refresh admin token

### Utilities

- `GET /health` - Health check endpoint
- `GET /` - API information

## Testing the API

### Using the Interactive Docs

1. Start the server
2. Visit http://localhost:8000/docs
3. Try the `/health` endpoint first
4. For auth endpoints, you'll need a Firebase ID token from your frontend

### Using Postman/Thunder Client

1. Get a Firebase ID token from your frontend after signing in
2. For protected routes, use `Authorization: Bearer <token>` header
3. For signup/signin endpoints, send token in request body: `{"token": "<firebase-token>"}`

### Example Request

```bash
# Health check
curl http://localhost:8000/health

# Signin (requires Firebase token from frontend)
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_FIREBASE_ID_TOKEN"}'

# Get current user (protected route)
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_FIREBASE_ID_TOKEN"
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py             # Configuration and settings
│   ├── dependencies.py       # Auth dependencies
│   ├── models/
│   │   ├── auth.py          # Auth request/response models
│   │   └── user.py          # User models
│   ├── routers/
│   │   ├── auth.py          # Auth endpoints
│   │   └── admin_auth.py    # Admin auth endpoints
│   └── services/
│       └── firebase.py      # Firebase Admin SDK service
├── firebase_account_services.json  # Firebase credentials (keep secret!)
├── requirements.txt
├── .env                      # Environment variables (create this)
└── README.md
```

## Security Notes

- ✅ Firebase credentials file is in `.gitignore`
- ✅ Never commit `firebase_account_services.json` to version control
- ✅ Tokens are verified on every protected route
- ✅ CORS is configured to only allow your frontend domain
- ✅ Admin access is restricted to configured admin emails

## Next Steps

1. Add database integration (SQLite or PostgreSQL)
2. Implement user profile storage
3. Add event management endpoints
4. Implement photo upload and storage
5. Add admin dashboard endpoints

## Troubleshooting

### Firebase credentials not found

Make sure `firebase_account_services.json` is in the `backend/` directory and the path in `.env` is correct.

### Token verification fails

- Check that Firebase Authentication is enabled in Firebase Console
- Verify the token hasn't expired (tokens expire after 1 hour)
- Ensure Email/Password and Google Sign-In providers are enabled in Firebase

### CORS errors

Update `FRONTEND_URL` in `.env` to match your frontend URL.

## License

Private project - All rights reserved

