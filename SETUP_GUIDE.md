# 🚀 PANDUAN SETUP & DEPLOYMENT

## Daftar Isi
1. [Setup Lokal](#setup-lokal)
2. [Menjalankan Aplikasi](#menjalankan-aplikasi)
3. [Menjalankan Tests](#menjalankan-tests)
4. [Deploy ke GitHub](#deploy-ke-github)
5. [Troubleshooting](#troubleshooting)

---

## Setup Lokal

### Prerequisite
- ✅ Python 3.9 atau lebih tinggi
- ✅ Git
- ✅ pip (sudah include dengan Python)

### Windows

#### 1. Clone Repository (jika dari GitHub)
```cmd
git clone https://github.com/your-username/student-grading-system.git
cd student-grading-system
```

#### 2. Create Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

Atau gunakan setup script:
```cmd
setup.bat
```

#### 4. Verifikasi Instalasi
```cmd
python -c "import flask; import pytest; print('Setup OK!')"
```

---

### Linux/Mac

#### 1. Clone Repository (jika dari GitHub)
```bash
git clone https://github.com/your-username/student-grading-system.git
cd student-grading-system
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Atau gunakan setup script:
```bash
chmod +x setup.sh
./setup.sh
```

#### 4. Verifikasi Instalasi
```bash
python -c "import flask; import pytest; print('Setup OK!')"
```

---

## Menjalankan Aplikasi

### Akses di Localhost

#### Windows
```cmd
# Aktifkan virtual environment
venv\Scripts\activate

# Jalankan aplikasi
python run.py
```

#### Linux/Mac
```bash
# Aktifkan virtual environment
source venv/bin/activate

# Jalankan aplikasi
python run.py
```

### Akses Web Interface
Buka browser dan akses:
- **Home Page**: http://localhost:5000/
- **Dashboard**: http://localhost:5000/dashboard

### Struktur URL
| Path | Deskripsi |
|------|-----------|
| `/` | Home page dengan info aplikasi |
| `/dashboard` | Dashboard utama - kelola siswa & nilai |
| `/api/students` | REST API endpoint |
| `/api/statistics` | REST API statistik |

### Example API Calls

**Tambah Siswa:**
```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "nim": "2024001", "email": "john@example.com"}'
```

**Ambil Semua Siswa:**
```bash
curl http://localhost:5000/api/students
```

**Tambah Nilai:**
```bash
curl -X POST http://localhost:5000/api/students/1/grades \
  -H "Content-Type: application/json" \
  -d '{"subject": "Mathematics", "score": 85}'
```

---

## Menjalankan Tests

### Run All Tests
```bash
# Aktifkan virtual environment terlebih dahulu
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pytest
```

### Run Tests dengan Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_models.py
pytest tests/test_services.py
pytest tests/test_api.py
```

### Run Tests dengan Coverage Report

#### Generate Coverage Report (Terminal)
```bash
pytest --cov=app --cov-report=term-missing
```

#### Generate HTML Coverage Report
```bash
pytest --cov=app --cov-report=html
```

Buka: `htmlcov/index.html` di browser

#### Generate XML Coverage Report (untuk CI/CD)
```bash
pytest --cov=app --cov-report=xml
```

### Test Statistics
```bash
# Run tests dan tampilkan performa
pytest -v --tb=short

# Output contoh:
# test_models.py::TestStudentModel::test_create_student PASSED
# test_services.py::TestStudentService::test_create_student_valid PASSED
# test_api.py::TestStudentAPI::test_get_students_empty PASSED
# =================== 47 passed in 2.34s ===================
```

---

## Deploy ke GitHub

### 1. Create GitHub Repository

#### A. Create Repository di GitHub
- Login ke [github.com](https://github.com)
- Klik `+` → New repository
- Repository name: `student-grading-system`
- Description: `Final Project - Software Testing Course`
- Choose: **Public** (untuk lebih transparan)
- Initialize: **Don't initialize**
- Click: **Create repository**

#### B. Get Repository URL
Setelah membuat repo, copy HTTPS URL:
```
https://github.com/your-username/student-grading-system.git
```

### 2. Push Code ke GitHub

#### First Time Setup

```bash
# Navigasi ke project folder
cd "c:\Users\CHRISTIAN\OneDrive\Desktop\Final Project\d"

# Initialize git (jika belum)
git init

# Add all files
git add .

# Configure git (first time)
git config user.email "your@email.com"
git config user.name "Your Name"

# Commit
git commit -m "Initial commit: Setup Student Grading System with tests and CI/CD"

# Add remote repository
git remote add origin https://github.com/your-username/student-grading-system.git

# Push ke GitHub (main branch)
git branch -M main
git push -u origin main
```

### 3. Verify GitHub Actions

#### Cek Workflow
1. Buka repository di GitHub
2. Klik tab **Actions**
3. Lihat workflow runs
4. Tunggu hingga build selesai

#### Expected Status
- ✅ **Green checkmark** = All tests passed
- ❌ **Red X** = Tests failed (perlu diperbaiki)

### 4. Add Status Badges

Edit `README.md` di repository GitHub:

```markdown
# Student Grading System

![Build Status](https://github.com/your-username/student-grading-system/workflows/CI%2FCD%20Pipeline/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)

...rest of README...
```

### 5. Continuous Deployment

Setiap kali push code:
1. GitHub Actions workflow triggered
2. Tests berjalan otomatis
3. Coverage report generated
4. Status di-update otomatis

---

## Workflow Git

### Standard Commits
```bash
# Feature development
git checkout -b feature/add-export-feature
# ... make changes ...
git add .
git commit -m "feat: Add PDF export functionality"
git push origin feature/add-export-feature

# Create pull request di GitHub
# After review → merge to main
```

### Commit Message Convention
- `feat:` - New feature
- `fix:` - Bug fix
- `test:` - Adding/modifying tests
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Example:
```bash
git commit -m "test: Add 5 new integration tests for API"
git commit -m "docs: Update README with setup guide"
git commit -m "feat: Implement student ranking feature"
```

---

## Project Structure Overview

```
student-grading-system/
│
├── 📁 app/                          # Application source code
│   ├── __init__.py                  # Flask app factory
│   ├── models.py                    # Database models
│   ├── services.py                  # Business logic
│   ├── routes.py                    # API endpoints
│   ├── 📁 templates/
│   │   ├── index.html               # Home page
│   │   └── dashboard.html           # Dashboard UI
│   └── 📁 static/
│       ├── style.css                # Styling
│       └── script.js                # Client-side logic
│
├── 📁 tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_models.py               # Model tests (15 cases)
│   ├── test_services.py             # Service tests (26 cases)
│   └── test_api.py                  # API tests (13 cases)
│
├── 📁 instance/                     # Runtime data
│   └── grades.db                    # SQLite database (auto-created)
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── ci.yml                   # GitHub Actions pipeline
│
├── 📁 htmlcov/                      # Coverage reports (generated)
│
├── 📄 run.py                        # Application entry point
├── 📄 requirements.txt              # Python dependencies
├── 📄 pytest.ini                    # Pytest configuration
├── 📄 README.md                     # Full documentation
├── 📄 PROJECT_REPORT.md             # Project report (2-3 pages)
├── 📄 SETUP_GUIDE.md                # This file
├── 📄 .gitignore                    # Git ignore rules
├── 📄 .gitattributes                # Git attributes
├── 📄 setup.bat                     # Windows setup script
└── 📄 setup.sh                      # Linux/Mac setup script
```

---

## Important Folders

| Folder | Purpose |
|--------|---------|
| `app/` | All application source code |
| `tests/` | All test files |
| `instance/` | Database & runtime data |
| `htmlcov/` | Code coverage reports |
| `.github/` | GitHub Actions workflows |

---

## Troubleshooting

### Issue: Module not found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
```
Address already in use
```
**Solution:**
```bash
# Change port in run.py
# Or kill process using port 5000

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Issue: Database errors
```
sqlite3.OperationalError: attempt to write a readonly database
```
**Solution:**
```bash
# Delete old database
rm instance/grades.db

# Restart application
python run.py
```

### Issue: Tests not found
```
ERROR collecting tests
```
**Solution:**
```bash
cd path/to/project
pip install pytest
pytest --collect-only  # Debug
```

### Issue: Git authentication error
```
fatal: Authentication failed
```
**Solution:**
```bash
# Use GitHub token instead of password
# Or configure SSH key
git remote set-url origin git@github.com:username/repo.git
```

---

## Quick Checklists

### Before Submit
- [ ] Run `pytest` - all tests pass
- [ ] Check coverage - 85%+
- [ ] Run application - works at localhost:5000
- [ ] View dashboard - UI responsive
- [ ] Test API endpoints - working
- [ ] Documentation - complete
- [ ] Git commits - meaningful messages
- [ ] GitHub Actions - workflow running

### GitHub Repository
- [ ] Repository created and public
- [ ] Code pushed to main branch
- [ ] GitHub Actions workflow visible
- [ ] Status badges in README
- [ ] Project report included
- [ ] README with setup instructions
- [ ] Coverage badge showing 85%+

### Documentation
- [ ] README.md - complete
- [ ] PROJECT_REPORT.md - 2-3 pages
- [ ] SETUP_GUIDE.md - this file
- [ ] Code comments - clear
- [ ] API documentation - in README

---

## Support Resources

### Documentation Files
- [README.md](README.md) - Full project documentation
- [PROJECT_REPORT.md](PROJECT_REPORT.md) - Formal project report
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - This setup guide

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Docs](https://docs.github.com/actions)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

---

## Next Steps

1. ✅ Run setup: `python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt`
2. ✅ Start app: `python run.py`
3. ✅ Open browser: http://localhost:5000
4. ✅ Run tests: `pytest`
5. ✅ Generate coverage: `pytest --cov=app --cov-report=html`
6. ✅ Push to GitHub: `git push origin main`
7. ✅ View GitHub Actions: Check repository Actions tab

---

**Good luck dengan Final Project Anda! 🎉**

Last Updated: April 23, 2024
