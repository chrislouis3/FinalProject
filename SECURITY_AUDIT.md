# 🔒 Security Audit Report - Rumah Makan Diadoek
**Date**: April 25, 2026  
**Application**: Student Grading System (Flask Web App)  
**Environment**: Development/Localhost

---

## ⚠️ SECURITY FINDINGS SUMMARY

### Critical Issues: 2
### High Issues: 3
### Medium Issues: 4
### Low Issues: 2

---

## 🔴 CRITICAL ISSUES

### 1. Debug Mode Enabled in Production-like Environment
**File**: `run.py` (Line 5)
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

**Risk Level**: 🔴 CRITICAL

**Issues**:
- ✗ `debug=True` memberikan akses ke Werkzeug debugger
- ✗ Debugger dapat diakses dari internet tanpa autentikasi
- ✗ Dapat menjalankan arbitrary Python code melalui interactive console
- ✗ Source code terlihat penuh di error pages
- ✗ Secret keys terekspos di error tracebacks

**Impact**: Penyerang dapat:
- Remote Code Execution (RCE) via debugger console
- Steal sensitive data dari memory
- Manipulate aplikasi tanpa batasan

**Remediation**:
```python
# SAFER APPROACH
if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
```

---

### 2. Accessible on All Network Interfaces (0.0.0.0)
**File**: `run.py` (Line 5)
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

**Risk Level**: 🔴 CRITICAL

**Issues**:
- ✗ `host='0.0.0.0'` membuka aplikasi untuk semua interface
- ✗ Termasuk interface external yang terhubung ke network/internet
- ✗ Dapat diakses oleh semua device di network yang sama
- ✗ Tidak ada rate limiting atau access control

**Impact**: Unauthorized access dari:
- Devices lain di local network
- Potential internet access jika router terbuka
- DDoS attacks dari network

**Remediation**:
```python
# Hanya accessible dari localhost
app.run(debug=False, host='127.0.0.1', port=5000)

# Atau jika perlu network access (dengan caution)
app.run(debug=False, host='0.0.0.0', port=5000)  # + nginx reverse proxy + authentication
```

---

## 🟠 HIGH SEVERITY ISSUES

### 3. Missing CSRF Protection
**Status**: ❌ No CSRF tokens found in templates

**Risk Level**: 🟠 HIGH

**Issues**:
- ✗ Templates tidak menggunakan CSRF tokens
- ✗ POST/PUT/DELETE requests vulnerable terhadap CSRF attacks
- ✗ Tidak ada Flask-WTF atau CSRF middleware detected

**Example Attack**:
```html
<!-- Malicious site bisa bikin request dari user Anda -->
<img src="http://localhost:5000/api/students/1" style="display:none">
<form action="http://localhost:5000/api/students" method="POST">
  <input name="name" value="Hacked">
  <input name="nim" value="123">
  <input name="email" value="hacker@evil.com">
</form>
```

**Remediation**:
```bash
pip install Flask-WTF
```

```python
# app/__init__.py
from flask_wtf.csrf import CSRFProtect

def create_app(config_name='development'):
    app = Flask(__name__)
    csrf = CSRFProtect(app)
    # ...
```

```html
<!-- Dalam forms/AJAX requests -->
<form method="POST" action="/api/students">
    {{ csrf_token() }}
    <input type="text" name="name">
</form>
```

---

### 4. No Input Validation & SQL Injection Risk
**File**: `app/routes.py` (Multiple endpoints)

**Risk Level**: 🟠 HIGH

**Issues**:
- ✗ Input tidak divalidasi untuk format/length
- ✗ Email tidak di-validate sebagai valid email format
- ✗ NIM bisa berisi special characters
- ✗ Name field vulnerable terhadap injection

**Vulnerable Code**:
```python
@api_bp.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    name = data.get('name')  # ❌ No validation!
    nim = data.get('nim')
    email = data.get('email')  # ❌ No email validation!
    
    student = StudentService.create_student(name, nim, email)
```

**Attack Example**:
```json
{
  "name": "<script>alert('XSS')</script>",
  "nim": "'; DROP TABLE students; --",
  "email": "not-an-email"
}
```

**Remediation**:
```bash
pip install email-validator
```

```python
from email_validator import validate_email, EmailNotValidError
import re

@api_bp.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        
        # Validate name
        name = data.get('name', '').strip()
        if not name or len(name) > 120:
            return jsonify({'error': 'Invalid name'}), 400
        if not re.match(r'^[a-zA-Z\s\-\.]+$', name):
            return jsonify({'error': 'Name contains invalid characters'}), 400
        
        # Validate NIM
        nim = data.get('nim', '').strip()
        if not nim or len(nim) > 20:
            return jsonify({'error': 'Invalid NIM'}), 400
        if not nim.isalnum():
            return jsonify({'error': 'NIM must be alphanumeric'}), 400
        
        # Validate email
        email = data.get('email', '').strip()
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400
        
        student = StudentService.create_student(name, nim, email)
        return jsonify(student.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
```

---

### 5. Detailed Error Messages Leak Information
**File**: `app/routes.py` (All endpoints)

**Risk Level**: 🟠 HIGH

**Issues**:
- ✗ Exception messages returned in responses: `return jsonify({'error': str(e)})`
- ✗ Stack traces mungkin terekspos di debug mode
- ✗ Database paths, internal structure terlihat

**Leaky Error Example**:
```json
{
  "error": "INSERT failed: column 'unique_constraint' violation"
}
```

Penyerang bisa infer:
- Database structure dan column names
- Library versions digunakan
- Internal application logic

**Remediation**:
```python
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        student = StudentService.create_student(name, nim, email)
        return jsonify(student.to_dict()), 201
    except ValueError as e:
        # Log internally, return generic message
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({'error': 'Invalid input data'}), 400
    except Exception as e:
        # Never expose internal errors
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred'}), 500
```

---

## 🟡 MEDIUM SEVERITY ISSUES

### 6. No Rate Limiting
**Risk Level**: 🟡 MEDIUM

**Issues**:
- ✗ No rate limiting on API endpoints
- ✗ Vulnerable terhadap brute force attacks
- ✗ Vulnerable terhadap DDoS/resource exhaustion

**Remediation**:
```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@api_bp.route('/students', methods=['GET'])
@limiter.limit("30 per minute")
def get_students():
    # ...
```

---

### 7. No Security Headers
**Risk Level**: 🟡 MEDIUM

**Issues**:
- ✗ Missing Content-Security-Policy header
- ✗ Missing X-Frame-Options (Clickjacking)
- ✗ Missing X-Content-Type-Options
- ✗ Missing Strict-Transport-Security (HSTS)

**Remediation**:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

### 8. No SQLAlchemy Parameterization Validation
**Status**: ⚠️ Currently SQLAlchemy handles this, but needs verification

**Risk**: 🟡 MEDIUM

**Issues**:
- ✓ SQLAlchemy menggunakan parameterized queries (GOOD)
- ⚠️ Namun string concatenation di tempat lain bisa risky
- ⚠️ Dynamic query construction perlu diaudit

---

### 9. Database File Permissions
**File**: `instance/grades.db`

**Risk Level**: 🟡 MEDIUM

**Issues**:
- ⚠️ SQLite database file ada di working directory
- ⚠️ File permissions mungkin accessible oleh other users
- ⚠️ Tidak ada encryption on database

**Remediation**:
```python
# Set restrictive permissions setelah create
import os
import stat

db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'grades.db')
if os.path.exists(db_path):
    os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)  # 0600 - only owner can read/write
```

---

## 🟢 LOW SEVERITY ISSUES

### 10. Missing Security.txt
**Risk Level**: 🟢 LOW

**Issue**: Tidak ada `/.well-known/security.txt` untuk vulnerability disclosure policy

**Remediation**:
```python
@app.route('/.well-known/security.txt')
def security_txt():
    return """Contact: security@yourdomain.com
Expires: 2024-12-31T23:59:59.000Z
Preferred-Languages: en
"""
```

---

### 11. No Dependency Vulnerability Check
**Risk Level**: 🟢 LOW

**Issues**:
- ⚠️ Dependencies bisa memiliki known vulnerabilities
- ⚠️ Flask 2.3.3 is relatively old (current: 3.x)

**Remediation**:
```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies ke latest
pip install --upgrade Flask Flask-SQLAlchemy
```

---

## 📋 CHECKLIST - Quick Fixes (Priority Order)

### Immediate (Do Now):
- [ ] Change `debug=True` → `debug=False` di run.py
- [ ] Change `host='0.0.0.0'` → `host='127.0.0.1'` di run.py
- [ ] Add input validation untuk semua API endpoints
- [ ] Add generic error messages (jangan expose details)
- [ ] Add CSRF protection dengan Flask-WTF

### Short-term (This Week):
- [ ] Implement rate limiting dengan Flask-Limiter
- [ ] Add security headers (CSP, X-Frame-Options, dll)
- [ ] Fix database file permissions
- [ ] Update Flask dan dependencies
- [ ] Add logging untuk security events

### Long-term (Production Ready):
- [ ] Implement proper authentication/authorization
- [ ] Add HTTPS/SSL configuration
- [ ] Setup WAF (Web Application Firewall)
- [ ] Regular security audits
- [ ] Implement secrets management (.env)
- [ ] Setup monitoring dan alerting

---

## 🔧 PROPOSED SECURE CONFIGURATION

**run.py (IMPROVED)**:
```python
from app import create_app
import os

if __name__ == '__main__':
    app = create_app()
    
    # Security configuration
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # Default: localhost only
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Development safe defaults
    print(f"🚀 Starting app:")
    print(f"   Debug: {debug}")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    
    app.run(debug=debug, host=host, port=port)
```

**.env (EXAMPLE)**:
```
FLASK_ENV=development
FLASK_DEBUG=False
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

---

## ✅ VERIFICATION STEPS

Untuk verify security di localhost:

1. **Test 1**: Cek apakah accessible dari device lain
   ```bash
   # From another device on network
   curl http://<your-pc-ip>:5000/
   # Should fail jika hanya listen di 127.0.0.1
   ```

2. **Test 2**: Check error messages tidak leak info
   ```bash
   curl -X POST http://localhost:5000/api/students \
     -H "Content-Type: application/json" \
     -d '{"name":"test","nim":"123","email":"invalid"}'
   # Response harus generic, bukan detail error
   ```

3. **Test 3**: Security headers check
   ```bash
   curl -i http://localhost:5000/
   # Check response headers untuk security headers
   ```

4. **Test 4**: Database permissions
   ```bash
   # Linux/Mac
   ls -la instance/grades.db
   # Should be: -rw------- (600 permissions)
   ```

---

## 📊 RISK ASSESSMENT

| Issue | Severity | Impact | Effort | Priority |
|-------|----------|--------|--------|----------|
| Debug Mode | CRITICAL | RCE | Very Easy | P0 |
| Host 0.0.0.0 | CRITICAL | Unauthorized Access | Very Easy | P0 |
| No CSRF | HIGH | Account Takeover | Medium | P1 |
| No Input Validation | HIGH | Injection Attacks | Medium | P1 |
| Verbose Errors | HIGH | Information Disclosure | Easy | P1 |
| No Rate Limiting | MEDIUM | Brute Force/DDoS | Medium | P2 |
| Missing Security Headers | MEDIUM | Multiple Vectors | Easy | P2 |
| Dependency Updates | LOW | Known Vulns | Easy | P3 |

---

## 🎯 CONCLUSION

**Current Status**: ⚠️ **UNSAFE FOR PRODUCTION**

Localhost saat ini:
- ✗ Vulnerable terhadap remote code execution
- ✗ Accessible dari network/internet
- ✗ Tidak ada protection terhadap common attacks
- ✗ Error messages leak sensitive information

**Recommendation**: 
1. **Fix critical issues immediately** (debug mode, 0.0.0.0)
2. **Add validation dan security headers** 
3. **Implement proper error handling**
4. **Test dengan security scanning tools**

Setelah fixes, akan jauh lebih aman untuk development & testing purposes.

---

**Report Generated**: April 25, 2026  
**Next Review**: After implementing fixes
