# Security Fixes for app/routes.py
# ==================================
# This file shows how to add input validation and secure error handling

from flask import Blueprint, render_template, request, jsonify
from app.services import StudentService, GradeService
from email_validator import validate_email, EmailNotValidError
import re
import logging

logger = logging.getLogger(__name__)

# Blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ============ VALIDATION HELPERS ============

def validate_name(name):
    """Validate student name"""
    if not name or not isinstance(name, str):
        return False, "Name is required"
    
    name = name.strip()
    if len(name) < 3 or len(name) > 120:
        return False, "Name must be between 3 and 120 characters"
    
    # Only allow letters, spaces, hyphens, and dots
    if not re.match(r'^[a-zA-Z\s\-\.\']+$', name):
        return False, "Name contains invalid characters"
    
    return True, name

def validate_nim(nim):
    """Validate student NIM"""
    if not nim or not isinstance(nim, str):
        return False, "NIM is required"
    
    nim = nim.strip()
    if len(nim) < 2 or len(nim) > 20:
        return False, "NIM must be between 2 and 20 characters"
    
    # Only allow alphanumeric characters
    if not nim.isalnum():
        return False, "NIM must be alphanumeric only"
    
    return True, nim

def validate_email_format(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False, "Email is required"
    
    email = email.strip().lower()
    
    try:
        # Validate email format
        validate_email(email)
        return True, email
    except EmailNotValidError as e:
        return False, "Invalid email format"

# ============ WEB ROUTES ============

@main_bp.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard dengan daftar siswa dan statistik"""
    return render_template('dashboard.html')

# ============ API ROUTES - STUDENT (WITH VALIDATION) ============

@api_bp.route('/students', methods=['GET'])
def get_students():
    """GET: Ambil semua data siswa"""
    try:
        students = StudentService.get_all_students()
        return jsonify([s.to_dict() for s in students]), 200
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch students'}), 500

@api_bp.route('/students', methods=['POST'])
def create_student():
    """POST: Tambah siswa baru dengan validasi input"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Validate name
        is_valid, name_or_error = validate_name(data.get('name'))
        if not is_valid:
            logger.warning(f"Invalid name input: {name_or_error}")
            return jsonify({'error': name_or_error}), 400
        name = name_or_error
        
        # Validate NIM
        is_valid, nim_or_error = validate_nim(data.get('nim'))
        if not is_valid:
            logger.warning(f"Invalid NIM input: {nim_or_error}")
            return jsonify({'error': nim_or_error}), 400
        nim = nim_or_error
        
        # Validate email
        is_valid, email_or_error = validate_email_format(data.get('email'))
        if not is_valid:
            logger.warning(f"Invalid email input: {email_or_error}")
            return jsonify({'error': email_or_error}), 400
        email = email_or_error
        
        # Create student with validated data
        student = StudentService.create_student(name, nim, email)
        logger.info(f"Student created: ID={student.id}, NIM={nim}")
        return jsonify(student.to_dict()), 201
        
    except ValueError as e:
        # This is expected for business logic errors
        logger.warning(f"Validation error creating student: {str(e)}")
        return jsonify({'error': 'Invalid student data'}), 400
    except Exception as e:
        # Unexpected errors - log but don't expose details
        logger.error(f"Unexpected error creating student: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred'}), 500

@api_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """GET: Ambil data siswa berdasarkan ID"""
    try:
        # Validate student_id is positive integer
        if student_id <= 0:
            return jsonify({'error': 'Invalid student ID'}), 400
        
        student = StudentService.get_student_by_id(student_id)
        if not student:
            logger.warning(f"Student not found: ID={student_id}")
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify(student.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching student {student_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred'}), 500

@api_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """PUT: Update data siswa dengan validasi"""
    try:
        if student_id <= 0:
            return jsonify({'error': 'Invalid student ID'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        update_fields = {}
        
        # Validate and update name if provided
        if 'name' in data:
            is_valid, name_or_error = validate_name(data.get('name'))
            if not is_valid:
                return jsonify({'error': f'Invalid name: {name_or_error}'}), 400
            update_fields['name'] = name_or_error
        
        # Validate and update email if provided
        if 'email' in data:
            is_valid, email_or_error = validate_email_format(data.get('email'))
            if not is_valid:
                return jsonify({'error': f'Invalid email: {email_or_error}'}), 400
            update_fields['email'] = email_or_error
        
        student = StudentService.update_student(student_id, **update_fields)
        logger.info(f"Student updated: ID={student_id}")
        return jsonify(student.to_dict()), 200
        
    except ValueError as e:
        logger.warning(f"Validation error updating student: {str(e)}")
        return jsonify({'error': 'Invalid update data'}), 400
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred'}), 500

@api_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """DELETE: Hapus siswa"""
    try:
        if student_id <= 0:
            return jsonify({'error': 'Invalid student ID'}), 400
        
        StudentService.delete_student(student_id)
        logger.info(f"Student deleted: ID={student_id}")
        return jsonify({'message': 'Student deleted successfully'}), 200
        
    except ValueError as e:
        logger.warning(f"Error deleting student {student_id}: {str(e)}")
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        logger.error(f"Unexpected error deleting student {student_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred'}), 500

# ============ NOTES ============
# 1. All input is validated before use
# 2. Error messages are generic - no internal details exposed
# 3. All errors are logged for debugging
# 4. Database operations use SQLAlchemy (prevents SQL injection)
# 5. CSRF protection is enabled via Flask-WTF
