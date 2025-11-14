# Google Sign-In Integration Guide

## How Google Sign-In Works with This Backend

### Overview

The backend **does not need special handling** for Google sign-in. Firebase handles both email/password and Google OAuth authentication, and both methods return the same Firebase ID token format.

### Authentication Flow

1. **Frontend (React)**: User clicks "Sign in with Google"
2. **Firebase Client SDK**: Handles Google OAuth flow
3. **Firebase**: Returns Firebase ID token (same format as email/password)
4. **Frontend**: Sends token to backend
5. **Backend**: Verifies token (same verification for all auth methods)

### Backend Endpoints

All authentication endpoints work the same way for both email/password and Google sign-in:

- `POST /auth/signup` - Works for both email/password and Google sign-up
- `POST /auth/signin` - Works for both email/password and Google sign-in
- `GET /auth/me` - Returns user info regardless of auth method
- All other endpoints work identically

### Token Format

Both authentication methods return Firebase ID tokens with the same structure:

```json
{
  "uid": "firebase-user-id",
  "email": "user@example.com",
  "email_verified": true,
  "name": "User Name",
  "firebase_claims": { ... }
}
```

### Frontend Setup (For Reference)

To enable Google sign-in in your React frontend:

1. **Enable Google Provider in Firebase Console**:
   - Go to Firebase Console → Authentication → Sign-in method
   - Enable "Google" provider
   - Add your OAuth client IDs

2. **Install Firebase SDK in Frontend**:
   ```bash
   npm install firebase
   ```

3. **Initialize Firebase in Frontend**:
   ```javascript
   import { initializeApp } from 'firebase/app';
   import { getAuth, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
   
   const auth = getAuth();
   const provider = new GoogleAuthProvider();
   
   // Sign in with Google
   signInWithPopup(auth, provider)
     .then((result) => {
       const token = await result.user.getIdToken();
       // Send token to backend
     });
   ```

4. **Send Token to Backend**:
   ```javascript
   // After getting token from Firebase
   const response = await fetch('http://localhost:8000/auth/signin', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ token: firebaseToken })
   });
   ```

### Backend Verification

The backend verifies tokens the same way regardless of auth method:

```python
# In app/services/firebase.py
def verify_firebase_token(token: str) -> Dict[str, Any]:
    decoded_token = auth.verify_id_token(token)
    # Works for both email/password and Google tokens
    return {
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "email_verified": decoded_token.get("email_verified", False),
        "name": decoded_token.get("name"),
    }
```

### Key Points

✅ **No backend changes needed** - Google sign-in works out of the box  
✅ **Same token format** - Both auth methods return Firebase ID tokens  
✅ **Same verification** - Backend verifies all tokens the same way  
✅ **Same endpoints** - Use the same `/auth/signin` and `/auth/signup` endpoints  
✅ **User info included** - Google sign-in provides name and email automatically  

### Testing

1. Test email/password sign-in:
   ```bash
   curl -X POST http://localhost:8000/auth/signin \
     -H "Content-Type: application/json" \
     -d '{"token": "EMAIL_PASSWORD_TOKEN"}'
   ```

2. Test Google sign-in:
   ```bash
   curl -X POST http://localhost:8000/auth/signin \
     -H "Content-Type: application/json" \
     -d '{"token": "GOOGLE_TOKEN"}'
   ```

Both should work identically!

### Notes

- Google sign-in users will have `email_verified: true` automatically
- Google sign-in provides `name` field automatically
- No password reset needed for Google users (they use Google's password)
- Admin access works the same way - check email against `ADMIN_EMAILS` in config

