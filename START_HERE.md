# 🚀 START HERE - Quick Setup Guide

**Untuk memulai dengan cepat, ikuti langkah-langkah di bawah!**

---

## Option 1: Automated Setup (Recommended for Windows)
Paling mudah dan cepat!

```bash
# Double-click file ini:
# quickstart.bat

# Atau jalankan di command prompt:
quickstart.bat
```

Selesai! Aplikasi akan langsung berjalan di http://localhost:5000

---

## Option 2: Automated Setup (Linux/Mac)

```bash
# Make script executable
chmod +x quickstart.sh

# Run it
./quickstart.sh
```

Selesai! Aplikasi akan langsung berjalan di http://localhost:5000

---

## Option 3: Manual Setup

### Step 1: Create Virtual Environment
```cmd
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
python run.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

---

## ✅ What You'll See

### Home Page (http://localhost:5000/)
- Welcome message
- Feature overview
- Link to dashboard

### Dashboard (http://localhost:5000/dashboard)
- Add new student form
- List of all students
- Add grades for each student
- Class statistics
- Student's average grade

---

## 🧪 Run Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=app --cov-report=html

# View coverage report
# Open: htmlcov/index.html
```

---

## 📊 What's in This Project?

✅ **Web Application** - Modern dashboard at localhost:5000  
✅ **REST API** - 9 endpoints for data management  
✅ **Database** - SQLite with proper schema  
✅ **Tests** - 54 test cases with 85% coverage  
✅ **CI/CD** - GitHub Actions automation  
✅ **Documentation** - Complete setup guide  

---

## 📝 Important Files

| File | Purpose |
|------|---------|
| `run.py` | Start application here |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `PROJECT_REPORT.md` | Formal project report |
| `SETUP_GUIDE.md` | Detailed setup |
| `tests/` | Test files (54 tests) |

---

## 🆘 Common Issues

### "Python not found"
- Install Python 3.9+ from python.org
- Add to PATH during installation

### "Port 5000 already in use"
- Change port in `run.py` line 7
- Or close other programs using port 5000

### "Module not found"
```bash
# Activate virtual environment first!
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Then: pip install -r requirements.txt
```

---

## 🎯 Next Steps

1. ✅ Run `quickstart.bat` or `quickstart.sh`
2. ✅ Open http://localhost:5000 in browser
3. ✅ Click "Open Dashboard"
4. ✅ Try adding a student and grades
5. ✅ Run tests: `pytest`
6. ✅ View coverage: `pytest --cov=app --cov-report=html`

---

## 📖 Full Documentation

- Detailed setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Project info: [README.md](README.md)
- Report: [PROJECT_REPORT.md](PROJECT_REPORT.md)
- Requirements: [REQUIREMENTS_CHECKLIST.md](REQUIREMENTS_CHECKLIST.md)

---

## ✨ Features to Try

1. **Add Students** - Use the form on dashboard
2. **Add Grades** - Input scores for each subject
3. **View Stats** - See class average, highest, lowest
4. **View Average** - Each student's average grade
5. **Auto Calculate** - System calculates automatically
6. **Grade Conversion** - See A-E grades automatically

---

**Ready? Let's go!** 🎉

Run `quickstart.bat` (Windows) or `./quickstart.sh` (Linux/Mac) now!

---

For more details, see [SETUP_GUIDE.md](SETUP_GUIDE.md) or [README.md](README.md)
