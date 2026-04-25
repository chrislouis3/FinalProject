# SECURITY TESTING GUIDE
# =======================

## 🧪 Quick Security Verification Tests

### Test 1: Check if Application is Localhost-Only
```bash
# On your PC
curl -v http://localhost:5000/

# Result should work:
# * Connection #0 to localhost left intact
# Response: 200 OK
```

```bash
# From another device on network (SHOULD FAIL with current config)
curl -v http://<YOUR-PC-IP>:5000/

# If using host='127.0.0.1': Should timeout/fail
# If using host='0.0.0.0': Will succeed (SECURITY ISSUE!)
```

### Test 2: Verify Debug Mode is OFF
```bash
# Send intentional error
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"invalid": "json'

# SECURE response (debug=False):
# {"error": "An error occurred"}
# Status: 500

# INSECURE response (debug=True):
# Full traceback with source code visible
# Werkzeug debugger accessible
```

### Test 3: Check Error Messages Don't Leak Info
```bash
# Test invalid input
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "nim": "123456",
    "email": "john@example.com"
  }'

# SECURE response:
# {"error": "Invalid input data"}

# INSECURE response:
# {"error": "UNIQUE constraint failed: students.name"}
# ^ This reveals database structure!
```

### Test 4: Verify Security Headers
```bash
curl -i http://localhost:5000/ | grep -i "X-"

# SECURE: Should see
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# X-XSS-Protection: 1; mode=block
# Content-Security-Policy: ...
# Referrer-Policy: ...

# INSECURE: No/few headers
```

### Test 5: Check SQL Injection Protection
```bash
# Try SQL injection
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'; DROP TABLE students; --",
    "nim": "123456",
    "email": "test@test.com"
  }'

# SECURE (SQLAlchemy parameterized):
# Returns error, no tables dropped
# Database is safe

# INSECURE (raw SQL):
# Could execute arbitrary SQL
# Database could be damaged
```

### Test 6: CSRF Protection (if implemented)
```bash
# Try POST without CSRF token
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"test","nim":"123","email":"test@test.com"}'

# With CSRF protection:
# Should return 400 or reject request

# Without CSRF protection:
# Will accept the request (VULNERABLE)
```

### Test 7: Check Database Permissions (Linux/Mac)
```bash
ls -la instance/grades.db

# SECURE: Should show
# -rw------- (0600 permissions - only owner can read/write)

# INSECURE: Should avoid
# -rw-r--r-- (0644 - others can read your database)
```

---

## 📋 Security Checklist

### Current Status (As of April 25, 2026)
- [ ] Debug mode is OFF
- [ ] Application binds to 127.0.0.1 (localhost only)
- [ ] No raw SQL queries (using SQLAlchemy ORM)
- [ ] Input validation implemented
- [ ] Generic error messages (no details leaked)
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Database file has secure permissions (0600)
- [ ] Dependencies updated to latest versions
- [ ] No hardcoded secrets in code
- [ ] Logging configured for security events
- [ ] HTTPS/SSL ready for production

### Scoring
- Count checks: [ ] / 13 ✓
- Score: (checked / 13) × 100%

---

## 🔧 Before Running Application

### Step 1: Create .env file
```bash
cp .env.example .env

# Edit .env and set:
FLASK_ENV=development
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

### Step 2: Install secure dependencies
```bash
pip install -r requirements_secure.txt
```

### Step 3: Run application securely
```bash
# Option A: Use secure run script
python run_secure.py

# Option B: Use current run.py (after fixing it)
python run.py

# Expected output:
# ============================================================
# 🚀 RUMAH MAKAN DIADOEK - STARTING APPLICATION
# ============================================================
# 📌 Environment: development
# 🔍 Debug Mode: False ✅ Secure
# 🌐 Host: 127.0.0.1 ✅ Localhost only
# 🔌 Port: 5000
# ============================================================
```

### Step 4: Verify application running safely
```bash
# In another terminal
curl http://localhost:5000/

# Should return the homepage
```

---

## 🛡️ Recommended Fixes (Priority Order)

### CRITICAL - Do Now (5 minutes)
1. **Change run.py**:
   ```python
   # BEFORE (UNSAFE)
   app.run(debug=True, host='0.0.0.0', port=5000)
   
   # AFTER (SECURE)
   app.run(debug=False, host='127.0.0.1', port=5000)
   ```

### HIGH - This Week (30 minutes)
1. Add input validation to routes.py
2. Add generic error handling
3. Update requirements.txt with secure packages
4. Add security headers to app/__init__.py

### MEDIUM - Before Production (2-3 hours)
1. Implement Flask-WTF for CSRF protection
2. Add Flask-Limiter for rate limiting
3. Add email-validator for input validation
4. Setup logging configuration

### LOW - Nice to Have (ongoing)
1. Update dependencies to latest versions
2. Run security scanner (bandit, safety)
3. Setup HTTPS/SSL for production
4. Implement proper authentication/authorization

---

## 🔍 Security Scanning Tools

### Install security scankers
```bash
pip install bandit safety
```

### Scan for security issues
```bash
# Scan code for security issues
bandit -r app/

# Check dependencies for known vulnerabilities
safety check
```

### Expected output for SECURE app:
```
$ bandit -r app/
...
Total lines of code scanned: 256
Total issues (by severity):
  Confirmed: 0
  Probable: 0
  Possible: 0
Code scanned successfully.
```

---

## 📊 Security Status

**Before Fixes** ⚠️:
- Debug: Enabled
- Host: 0.0.0.0 (all interfaces)
- Input Validation: None
- Error Messages: Detailed (info leak)
- Security Headers: None
- CSRF Protection: None
- Risk Level: CRITICAL

**After Fixes** ✅:
- Debug: Disabled
- Host: 127.0.0.1 (localhost only)
- Input Validation: Enabled
- Error Messages: Generic
- Security Headers: Enabled
- CSRF Protection: Enabled
- Risk Level: LOW (for development)

---

## 🆘 Troubleshooting

### Issue: "Port 5000 already in use"
```bash
# Find and kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

### Issue: "Connection refused" when accessing localhost:5000
```bash
# Make sure application is running
# Check terminal output for errors
# Default should be: http://127.0.0.1:5000/
```

### Issue: Application accessible from other devices
```bash
# Check run.py is using host='127.0.0.1'
# Make sure FLASK_HOST=127.0.0.1 in .env
# Restart application
```

---

## 📚 References

- [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/3.0.x/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

Generated: April 25, 2026
