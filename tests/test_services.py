"""
Unit tests untuk StudentService dan GradeService
"""
import pytest
from app.services import StudentService, GradeService
from app.models import Student, Grade
from app import db


class TestStudentService:
    """Test cases untuk StudentService"""
    
    def test_create_student_valid(self, app_context):
        """Test membuat student dengan data valid"""
        student = StudentService.create_student('Test User', '2024100', 'test@example.com')
        
        assert student.id is not None
        assert student.name == 'Test User'
        assert student.nim == '2024100'
        assert student.email == 'test@example.com'
    
    def test_create_student_duplicate_name(self, app_context):
        """Test membuat student dengan nama duplicate"""
        StudentService.create_student('Duplicate Name', '2024101', 'first@example.com')
        
        with pytest.raises(ValueError, match='Nama atau NIM sudah terdaftar'):
            StudentService.create_student('Duplicate Name', '2024102', 'second@example.com')
    
    def test_create_student_duplicate_nim(self, app_context):
        """Test membuat student dengan NIM duplicate"""
        StudentService.create_student('User One', '2024103', 'user1@example.com')
        
        with pytest.raises(ValueError, match='Nama atau NIM sudah terdaftar'):
            StudentService.create_student('User Two', '2024103', 'user2@example.com')
    
    def test_create_student_empty_name(self, app_context):
        """Test membuat student dengan nama kosong"""
        with pytest.raises(ValueError, match='Nama siswa tidak boleh kosong'):
            StudentService.create_student('', '2024104', 'test@example.com')
    
    def test_create_student_empty_nim(self, app_context):
        """Test membuat student dengan NIM kosong"""
        with pytest.raises(ValueError, match='NIM tidak boleh kosong'):
            StudentService.create_student('Test User', '', 'test@example.com')
    
    def test_create_student_empty_email(self, app_context):
        """Test membuat student dengan email kosong"""
        with pytest.raises(ValueError, match='Email tidak boleh kosong'):
            StudentService.create_student('Test User', '2024105', '')
    
    def test_create_student_invalid_email(self, app_context):
        """Test membuat student dengan format email invalid"""
        with pytest.raises(ValueError, match='Format email tidak valid'):
            StudentService.create_student('Test User', '2024106', 'invalidemail')
    
    def test_get_student_by_id_valid(self, app_context):
        """Test ambil student berdasarkan ID yang valid"""
        created = StudentService.create_student('User Three', '2024107', 'user3@example.com')
        student = StudentService.get_student_by_id(created.id)
        
        assert student is not None
        assert student.name == 'User Three'
    
    def test_get_student_by_id_invalid_id(self, app_context):
        """Test ambil student dengan ID invalid"""
        with pytest.raises(ValueError, match='ID siswa harus berupa angka positif'):
            StudentService.get_student_by_id(-1)
    
    def test_get_student_by_id_not_found(self, app_context):
        """Test ambil student yang tidak ada"""
        student = StudentService.get_student_by_id(99999)
        assert student is None
    
    def test_get_all_students_empty(self, app_context):
        """Test ambil semua student ketika kosong"""
        students = StudentService.get_all_students()
        assert len(students) == 0
    
    def test_get_all_students_multiple(self, app_context):
        """Test ambil semua student dengan multiple data"""
        StudentService.create_student('User A', '2024200', 'userA@example.com')
        StudentService.create_student('User B', '2024201', 'userB@example.com')
        StudentService.create_student('User C', '2024202', 'userC@example.com')
        
        students = StudentService.get_all_students()
        
        assert len(students) == 3
    
    def test_update_student_name(self, app_context):
        """Test update nama student"""
        student = StudentService.create_student('Old Name', '2024203', 'test@example.com')
        
        updated = StudentService.update_student(student.id, name='New Name')
        
        assert updated.name == 'New Name'
        assert updated.nim == '2024203'
    
    def test_update_student_email(self, app_context):
        """Test update email student"""
        student = StudentService.create_student('Test User', '2024204', 'old@example.com')
        
        updated = StudentService.update_student(student.id, email='new@example.com')
        
        assert updated.email == 'new@example.com'
    
    def test_delete_student_valid(self, app_context):
        """Test hapus student yang valid"""
        student = StudentService.create_student('To Delete', '2024205', 'delete@example.com')
        
        result = StudentService.delete_student(student.id)
        
        assert result is True
        assert StudentService.get_student_by_id(student.id) is None


class TestGradeService:
    """Test cases untuk GradeService"""
    
    @pytest.fixture
    def student_for_grade(self, app_context):
        """Create a student untuk test grade"""
        return StudentService.create_student('Grade Student', '2024300', 'grade@example.com')
    
    def test_add_grade_valid(self, student_for_grade, app_context):
        """Test tambah grade dengan data valid"""
        grade = GradeService.add_grade(student_for_grade.id, 'Mathematics', 85.0)
        
        assert grade.id is not None
        assert grade.subject == 'Mathematics'
        assert grade.score == 85.0
    
    def test_add_grade_score_validation_too_high(self, student_for_grade, app_context):
        """Test tambah grade dengan score > 100"""
        with pytest.raises(ValueError, match='Nilai harus antara 0-100'):
            GradeService.add_grade(student_for_grade.id, 'Physics', 105.0)
    
    def test_add_grade_score_validation_negative(self, student_for_grade, app_context):
        """Test tambah grade dengan score negatif"""
        with pytest.raises(ValueError, match='Nilai harus antara 0-100'):
            GradeService.add_grade(student_for_grade.id, 'Chemistry', -5.0)
    
    def test_add_grade_invalid_score_type(self, student_for_grade, app_context):
        """Test tambah grade dengan score tipe invalid"""
        with pytest.raises(ValueError, match='Nilai harus berupa angka'):
            GradeService.add_grade(student_for_grade.id, 'Biology', 'invalid')
    
    def test_add_grade_empty_subject(self, student_for_grade, app_context):
        """Test tambah grade dengan subject kosong"""
        with pytest.raises(ValueError, match='Nama mata pelajaran tidak boleh kosong'):
            GradeService.add_grade(student_for_grade.id, '', 80.0)
    
    def test_add_grade_student_not_found(self, app_context):
        """Test tambah grade untuk student yang tidak ada"""
        with pytest.raises(ValueError, match='Siswa tidak ditemukan'):
            GradeService.add_grade(99999, 'History', 90.0)
    
    def test_get_student_grades_empty(self, student_for_grade, app_context):
        """Test ambil grades student ketika kosong"""
        grades = GradeService.get_student_grades(student_for_grade.id)
        
        assert len(grades) == 0
    
    def test_get_student_grades_multiple(self, student_for_grade, app_context):
        """Test ambil multiple grades student"""
        GradeService.add_grade(student_for_grade.id, 'Math', 80.0)
        GradeService.add_grade(student_for_grade.id, 'Science', 90.0)
        GradeService.add_grade(student_for_grade.id, 'English', 85.0)
        
        grades = GradeService.get_student_grades(student_for_grade.id)
        
        assert len(grades) == 3
    
    def test_get_grade_by_id_valid(self, student_for_grade, app_context):
        """Test ambil grade berdasarkan ID"""
        created = GradeService.add_grade(student_for_grade.id, 'Art', 88.0)
        grade = GradeService.get_grade_by_id(created.id)
        
        assert grade is not None
        assert grade.subject == 'Art'
    
    def test_get_grade_by_id_invalid_id(self, app_context):
        """Test ambil grade dengan ID invalid"""
        with pytest.raises(ValueError, match='ID nilai harus berupa angka positif'):
            GradeService.get_grade_by_id(-1)
    
    def test_update_grade(self, student_for_grade, app_context):
        """Test update grade"""
        grade = GradeService.add_grade(student_for_grade.id, 'Original', 75.0)
        
        updated = GradeService.update_grade(grade.id, subject='Updated', score=95.0)
        
        assert updated.subject == 'Updated'
        assert updated.score == 95.0
    
    def test_delete_grade(self, student_for_grade, app_context):
        """Test hapus grade"""
        grade = GradeService.add_grade(student_for_grade.id, 'To Delete', 70.0)
        
        result = GradeService.delete_grade(grade.id)
        
        assert result is True
        assert GradeService.get_grade_by_id(grade.id) is None
    
    def test_class_statistics_empty(self, app_context):
        """Test statistik kelas ketika kosong"""
        stats = GradeService.get_class_statistics()
        
        assert stats['total_students'] == 0
        assert stats['average_class_grade'] == 0
    
    def test_class_statistics_with_data(self, app_context):
        """Test statistik kelas dengan data"""
        student1 = StudentService.create_student('Stat User 1', '2024400', 'stat1@example.com')
        student2 = StudentService.create_student('Stat User 2', '2024401', 'stat2@example.com')
        
        GradeService.add_grade(student1.id, 'Math', 80.0)
        GradeService.add_grade(student1.id, 'Science', 90.0)
        GradeService.add_grade(student2.id, 'Math', 70.0)
        
        stats = GradeService.get_class_statistics()
        
        assert stats['total_students'] == 2
        assert stats['highest_grade'] == 90.0
        assert stats['lowest_grade'] == 70.0
        assert stats['average_class_grade'] > 0
