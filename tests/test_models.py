"""
Unit tests untuk Student dan Grade models
"""
import pytest
from app.models import Student, Grade
from app import db


class TestStudentModel:
    """Test cases untuk Student model"""
    
    def test_create_student(self, app_context):
        """Test membuat student baru"""
        student = Student(name='Alice Smith', nim='2024001', email='alice@example.com')
        db.session.add(student)
        db.session.commit()
        
        assert student.id is not None
        assert student.name == 'Alice Smith'
        assert student.nim == '2024001'
    
    def test_student_to_dict(self, app_context):
        """Test konversi student ke dictionary"""
        student = Student(name='Bob Johnson', nim='2024002', email='bob@example.com')
        db.session.add(student)
        db.session.commit()
        
        student_dict = student.to_dict()
        
        assert student_dict['name'] == 'Bob Johnson'
        assert student_dict['nim'] == '2024002'
        assert student_dict['email'] == 'bob@example.com'
        assert 'id' in student_dict
        assert 'created_at' in student_dict
        assert 'average_grade' in student_dict
    
    def test_student_average_grade_no_grades(self, app_context):
        """Test average grade ketika tidak ada nilai"""
        student = Student(name='Charlie Brown', nim='2024003', email='charlie@example.com')
        db.session.add(student)
        db.session.commit()
        
        assert student.get_average_grade() == 0
    
    def test_student_average_grade_with_grades(self, app_context):
        """Test average grade dengan beberapa nilai"""
        student = Student(name='Diana Prince', nim='2024004', email='diana@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade1 = Grade(student_id=student.id, subject='Math', score=80.0)
        grade2 = Grade(student_id=student.id, subject='Science', score=90.0)
        grade3 = Grade(student_id=student.id, subject='English', score=85.0)
        
        db.session.add_all([grade1, grade2, grade3])
        db.session.commit()
        
        expected_avg = (80.0 + 90.0 + 85.0) / 3
        assert student.get_average_grade() == round(expected_avg, 2)
    
    def test_get_grade_letter_a(self, app_context):
        """Test grade letter A (85+)"""
        student = Student(name='Eve White', nim='2024005', email='eve@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Math', score=90.0)
        db.session.add(grade)
        db.session.commit()
        
        assert student.get_grade_letter() == 'A'
    
    def test_get_grade_letter_b(self, app_context):
        """Test grade letter B (75-84)"""
        student = Student(name='Frank Miller', nim='2024006', email='frank@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Math', score=78.0)
        db.session.add(grade)
        db.session.commit()
        
        assert student.get_grade_letter() == 'B'
    
    def test_get_grade_letter_c(self, app_context):
        """Test grade letter C (65-74)"""
        student = Student(name='Grace Lee', nim='2024007', email='grace@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Math', score=70.0)
        db.session.add(grade)
        db.session.commit()
        
        assert student.get_grade_letter() == 'C'
    
    def test_get_grade_letter_d(self, app_context):
        """Test grade letter D (55-64)"""
        student = Student(name='Henry Davis', nim='2024008', email='henry@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Math', score=60.0)
        db.session.add(grade)
        db.session.commit()
        
        assert student.get_grade_letter() == 'D'
    
    def test_get_grade_letter_e(self, app_context):
        """Test grade letter E (<55)"""
        student = Student(name='Ivy Taylor', nim='2024009', email='ivy@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Math', score=50.0)
        db.session.add(grade)
        db.session.commit()
        
        assert student.get_grade_letter() == 'E'


class TestGradeModel:
    """Test cases untuk Grade model"""
    
    def test_create_grade(self, app_context):
        """Test membuat grade baru"""
        student = Student(name='Jack Wilson', nim='2024010', email='jack@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Physics', score=88.5)
        db.session.add(grade)
        db.session.commit()
        
        assert grade.id is not None
        assert grade.subject == 'Physics'
        assert grade.score == 88.5
    
    def test_grade_to_dict(self, app_context):
        """Test konversi grade ke dictionary"""
        student = Student(name='Kathy Adams', nim='2024011', email='kathy@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Chemistry', score=92.0)
        db.session.add(grade)
        db.session.commit()
        
        grade_dict = grade.to_dict()
        
        assert grade_dict['subject'] == 'Chemistry'
        assert grade_dict['score'] == 92.0
        assert 'id' in grade_dict
        assert 'student_id' in grade_dict
        assert 'created_at' in grade_dict
    
    def test_grade_is_valid_score_valid(self, app_context):
        """Test validasi score yang valid"""
        student = Student(name='Leo Brown', nim='2024012', email='leo@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='History', score=75.0)
        
        assert grade.is_valid_score() is True
    
    def test_grade_is_valid_score_too_high(self, app_context):
        """Test validasi score lebih dari 100"""
        student = Student(name='Mia Johnson', nim='2024013', email='mia@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Geography', score=105.0)
        
        assert grade.is_valid_score() is False
    
    def test_grade_is_valid_score_negative(self, app_context):
        """Test validasi score negatif"""
        student = Student(name='Noah Smith', nim='2024014', email='noah@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Biology', score=-5.0)
        
        assert grade.is_valid_score() is False
    
    def test_grade_relationship_with_student(self, app_context):
        """Test relasi grade dengan student"""
        student = Student(name='Olivia Davis', nim='2024015', email='olivia@example.com')
        db.session.add(student)
        db.session.flush()
        
        grade = Grade(student_id=student.id, subject='Art', score=87.0)
        db.session.add(grade)
        db.session.commit()
        
        assert grade.student == student
        assert grade in student.grades
