@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! To run the application, use:
echo python run.py

echo.
echo To run tests, use:
echo pytest

echo.
echo To view coverage report, use:
echo pytest --cov=app --cov-report=html
echo Then open htmlcov/index.html
