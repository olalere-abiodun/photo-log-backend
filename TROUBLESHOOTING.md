# Troubleshooting Guide

## Common Errors and Solutions

### Error: `ModuleNotFoundError: No module named 'app'`

**Problem**: You're running the server from the wrong directory.

**Solution**: Make sure you're in the `backend` directory before running the server.

```bash
# Navigate to backend directory first
cd backend

# Then run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or use the startup script**:
- Windows: Double-click `start_server.bat`
- PowerShell: Run `.\start_server.ps1`

### Error: `uvicorn: command not found`

**Problem**: uvicorn is not installed or not in PATH.

**Solution**: 
1. Make sure virtual environment is activated
2. Install dependencies: `pip install -r requirements.txt`
3. Use `python -m uvicorn` instead of just `uvicorn`

### Error: `Firebase credentials file not found`

**Problem**: Firebase credentials file is missing or path is incorrect.

**Solution**:
1. Make sure `firebase_account_services.json` is in the `backend/` directory
2. Check `.env` file has correct path: `FIREBASE_CREDENTIALS_PATH=./firebase_account_services.json`

### Error: `email_validator` module not found

**Problem**: Missing dependency.

**Solution**: Install it:
```bash
pip install email-validator
```

### Error: Port 8000 already in use

**Problem**: Another process is using port 8000.

**Solution**: 
1. Find and stop the process using port 8000
2. Or use a different port: `--port 8001`

### Error: CORS errors in browser

**Problem**: Frontend URL not configured correctly.

**Solution**: 
1. Check `.env` file has: `FRONTEND_URL=http://localhost:5173`
2. Make sure CORS middleware is configured in `app/main.py`

### Error: `Email not sending`

**Problem**: Emails are not being sent or received.

**Solution**:
1.  **Verify `.env` Configuration**: Ensure the following variables are correctly set in your `.env` file:
    *   `EMAIL_ENABLED=true`
    *   `EMAIL_FROM`
    *   `SMTP_SERVER`
    *   `SMTP_PORT`
    *   `SMTP_USERNAME`
    *   `SMTP_PASSWORD` (For Gmail, this should be an App Password, not your regular account password.)
2.  **Check Gmail App Password (if using Gmail)**: If you are using Gmail, make sure you have generated and are using an App Password. Refer to [EMAIL_SETUP.md](./EMAIL_SETUP.md) for detailed instructions.
3.  **Run a Test Script**: You can run a simple Python script to test your email configuration independently.
    *   Create a file named `test_email.py` in your project root with the following content:
        ```python
        import asyncio
        from app.services.email import email_service
        from app.config import settings

        RECIPIENT_EMAIL = "your_test_email@example.com" # REPLACE WITH YOUR EMAIL

        async def send_test_email():
            print(f"Attempting to send a test email to {RECIPIENT_EMAIL}...")
            if not settings.email_enabled:
                print("Email sending is disabled in the configuration.")
                return
            if not all([settings.smtp_server, settings.smtp_port, settings.smtp_username, settings.smtp_password, settings.email_from]):
                print("SMTP settings are not fully configured in your .env file.")
                print("Please ensure SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, and EMAIL_FROM are set.")
                return
            try:
                success = email_service.send_welcome_email(
                    user_email=RECIPIENT_EMAIL,
                    user_name="Test User"
                )
                if success:
                    print("✅ Test email sent successfully!")
                    print(f"Please check the inbox of {RECIPIENT_EMAIL} (and the spam folder) to confirm receipt.")
                else:
                    print("❌ Failed to send test email. Check logs for details.")
            except Exception as e:
                print(f"An error occurred: {e}")

        if __name__ == "__main__":
            asyncio.run(send_test_email())
        ```
    *   **Replace `"your_test_email@example.com"`** with an actual email address you can check.
    *   Run the script from your terminal: `python test_email.py`
    *   Check the output for success or error messages, and check the recipient's inbox (and spam folder).
    *   Delete `test_email.py` after testing.

### Error: `Image uploads are failing`

**Problem**: The Cloudinary URL is not configured correctly.

**Solution**:
1. Make sure you have a `.env` file in the `backend/` directory.
2. Check that the `.env` file contains a valid `CLOUDINARY_URL`. It should look like this:
   ```
   CLOUDINARY_URL="cloudinary://<api_key>:<api_secret>@<cloud_name>"
   ```
3. Ensure the API key, secret, and cloud name are correct.

### Error: `Upload limit exceeded`

**Problem**: An authenticated user (host/admin) has exceeded their 1GB total upload limit.

**Solution**:
1. The 1GB limit applies to all files uploaded by an authenticated user, including event cover images, user avatars, and all photos uploaded to events they host (even public uploads).
2. To free up space, the user needs to delete some of their existing uploads.
3. Consider increasing the limit in `app/routers/events.py` and `app/routers/profiles.py` if a higher limit is desired.

### Error: `admin_emails` parsing error

**Problem**: Pydantic can't parse the admin_emails list from .env.


**Solution**: This is already fixed! The config now uses a comma-separated string:
```
ADMIN_EMAILS=admin@photolog.com,admin2@photolog.com
```

## How to Run the Server Correctly

### Method 1: Using Command Line

1. **Open terminal/PowerShell**
2. **Navigate to backend directory**:
   ```bash
   cd "C:\Users\Owner\Documents\New folder\frontend\backend"
   ```
3. **Activate virtual environment** (if using one):
   ```bash
   venv\Scripts\activate
   ```
4. **Run the server**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Method 2: Using Startup Script

**Windows Batch File**:
- Double-click `start_server.bat` in the `backend` folder

**PowerShell Script**:
- Right-click `start_server.ps1` → Run with PowerShell

### Method 3: Using Python Directly

```bash
cd backend
python -m app.main
```

## Verifying the Server is Running

1. **Check the terminal output** - You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

2. **Test the health endpoint**:
   - Open browser: http://localhost:8000/health
   - Or use curl: `curl http://localhost:8000/health`

3. **Check API docs**:
   - Open browser: http://localhost:8000/docs

## Still Having Issues?

1. **Check Python version**: `python --version` (should be 3.8+)
2. **Check all dependencies are installed**: `pip list`
3. **Check Firebase credentials file exists**: `dir firebase_account_services.json`
4. **Check .env file exists**: `dir .env`
5. **Look at the full error message** - it usually tells you what's wrong

## Quick Checklist

Before running the server, make sure:

- [ ] You're in the `backend` directory
- [ ] Virtual environment is activated (if using one)
- [ ] All dependencies are installed: `pip install -r requirements.txt`
- [ ] `firebase_account_services.json` exists in `backend/` directory
- [ ] `.env` file exists (optional, defaults will be used if not)
- [ ] Port 8000 is not already in use

