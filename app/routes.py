from flask import Blueprint, render_template, request, jsonify
from app.services import StudentService, GradeService

# Blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)


# ============ WEB ROUTES ============
@main_bp.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')


@main_bp.route('/dashboard')
def dashboard():
    """Dashboard dengan daftar siswa dan statistik"""
    return render_template('dashboard.html')


# ============ API ROUTES - STUDENT ============
@api_bp.route('/students', methods=['GET'])
def get_students():
    """GET: Ambil semua data siswa"""
    try:
        students = StudentService.get_all_students()
        return jsonify([s.to_dict() for s in students]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/students', methods=['POST'])
def create_student():
    """POST: Tambah siswa baru"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        name = data.get('name')
        nim = data.get('nim')
        email = data.get('email')
        
        student = StudentService.create_student(name, nim, email)
        return jsonify(student.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """GET: Ambil data siswa berdasarkan ID"""
    try:
        student = StudentService.get_student_by_id(student_id)
        if not student:
            return jsonify({'error': 'Siswa tidak ditemukan'}), 404
        return jsonify(student.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """PUT: Update data siswa"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        student = StudentService.update_student(
            student_id,
            name=data.get('name'),
            email=data.get('email')
        )
        return jsonify(student.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """DELETE: Hapus siswa"""
    try:
        StudentService.delete_student(student_id)
        return jsonify({'message': 'Siswa berhasil dihapus'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ API ROUTES - GRADES ============
@api_bp.route('/students/<int:student_id>/grades', methods=['POST'])
def add_grade(student_id):
    """POST: Tambah nilai siswa"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        subject = data.get('subject')
        score = data.get('score')
        
        grade = GradeService.add_grade(student_id, subject, score)
        return jsonify(grade.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/students/<int:student_id>/grades', methods=['GET'])
def get_grades(student_id):
    """GET: Ambil semua nilai siswa"""
    try:
        grades = GradeService.get_student_grades(student_id)
        return jsonify([g.to_dict() for g in grades]), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/grades/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    """PUT: Update nilai siswa"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body tidak boleh kosong'}), 400
        
        grade = GradeService.update_grade(
            grade_id,
            subject=data.get('subject'),
            score=data.get('score')
        )
        return jsonify(grade.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/grades/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    """DELETE: Hapus nilai siswa"""
    try:
        GradeService.delete_grade(grade_id)
        return jsonify({'message': 'Nilai berhasil dihapus'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ API ROUTES - STATISTICS ============
@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """GET: Ambil statistik kelas"""
    try:
        stats = GradeService.get_class_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
