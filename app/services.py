from app import db
from app.models import Student, Grade
from sqlalchemy.exc import IntegrityError

class StudentService:
    """Service untuk mengelola data siswa"""
    
    @staticmethod
    def create_student(name, nim, email):
        """
        Tambah siswa baru
        
        Args:
            name: Nama siswa
            nim: Nomor identitas mahasiswa
            email: Email siswa
            
        Returns:
            Student object atau None jika gagal
            
        Raises:
            ValueError: Jika data tidak valid
        """
        # Validasi input
        if not name or not name.strip():
            raise ValueError("Nama siswa tidak boleh kosong")
        if not nim or not nim.strip():
            raise ValueError("NIM tidak boleh kosong")
        if not email or not email.strip():
            raise ValueError("Email tidak boleh kosong")
        
        # Validasi format email
        if '@' not in email or '.' not in email:
            raise ValueError("Format email tidak valid")
        
        try:
            student = Student(name=name.strip(), nim=nim.strip(), email=email.strip())
            db.session.add(student)
            db.session.commit()
            return student
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Nama atau NIM sudah terdaftar")
    
    @staticmethod
    def get_student_by_id(student_id):
        """Ambil data siswa berdasarkan ID"""
        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("ID siswa harus berupa angka positif")
        return Student.query.get(student_id)
    
    @staticmethod
    def get_all_students():
        """Ambil semua data siswa"""
        return Student.query.all()
    
    @staticmethod
    def update_student(student_id, name=None, email=None):
        """Update data siswa"""
        student = StudentService.get_student_by_id(student_id)
        if not student:
            raise ValueError("Siswa tidak ditemukan")
        
        if name:
            student.name = name.strip()
        if email:
            if '@' not in email or '.' not in email:
                raise ValueError("Format email tidak valid")
            student.email = email.strip()
        
        try:
            db.session.commit()
            return student
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Nama atau email sudah terdaftar")
    
    @staticmethod
    def delete_student(student_id):
        """Hapus siswa"""
        student = StudentService.get_student_by_id(student_id)
        if not student:
            raise ValueError("Siswa tidak ditemukan")
        
        db.session.delete(student)
        db.session.commit()
        return True


class GradeService:
    """Service untuk mengelola nilai siswa"""
    
    @staticmethod
    def add_grade(student_id, subject, score):
        """
        Tambah nilai siswa
        
        Args:
            student_id: ID siswa
            subject: Nama mata pelajaran
            score: Nilai (0-100)
            
        Returns:
            Grade object
            
        Raises:
            ValueError: Jika data tidak valid
        """
        # Validasi input
        if not subject or not subject.strip():
            raise ValueError("Nama mata pelajaran tidak boleh kosong")
        
        # Validasi score
        try:
            score_float = float(score)
        except (TypeError, ValueError):
            raise ValueError("Nilai harus berupa angka")
        
        if not (0 <= score_float <= 100):
            raise ValueError("Nilai harus antara 0-100")
        
        # Cek student exists
        student = StudentService.get_student_by_id(student_id)
        if not student:
            raise ValueError("Siswa tidak ditemukan")
        
        grade = Grade(student_id=student_id, subject=subject.strip(), score=score_float)
        db.session.add(grade)
        db.session.commit()
        return grade
    
    @staticmethod
    def get_student_grades(student_id):
        """Ambil semua nilai siswa"""
        student = StudentService.get_student_by_id(student_id)
        if not student:
            raise ValueError("Siswa tidak ditemukan")
        return student.grades
    
    @staticmethod
    def get_grade_by_id(grade_id):
        """Ambil data nilai berdasarkan ID"""
        if not isinstance(grade_id, int) or grade_id <= 0:
            raise ValueError("ID nilai harus berupa angka positif")
        return Grade.query.get(grade_id)
    
    @staticmethod
    def update_grade(grade_id, subject=None, score=None):
        """Update nilai siswa"""
        grade = GradeService.get_grade_by_id(grade_id)
        if not grade:
            raise ValueError("Nilai tidak ditemukan")
        
        if subject:
            grade.subject = subject.strip()
        
        if score is not None:
            try:
                score_float = float(score)
            except (TypeError, ValueError):
                raise ValueError("Nilai harus berupa angka")
            
            if not (0 <= score_float <= 100):
                raise ValueError("Nilai harus antara 0-100")
            
            grade.score = score_float
        
        db.session.commit()
        return grade
    
    @staticmethod
    def delete_grade(grade_id):
        """Hapus nilai siswa"""
        grade = GradeService.get_grade_by_id(grade_id)
        if not grade:
            raise ValueError("Nilai tidak ditemukan")
        
        db.session.delete(grade)
        db.session.commit()
        return True
    
    @staticmethod
    def get_class_statistics():
        """Hitung statistik kelas"""
        students = Student.query.all()
        
        if not students:
            return {
                'total_students': 0,
                'average_class_grade': 0,
                'highest_grade': 0,
                'lowest_grade': 0
            }
        
        all_grades = []
        for student in students:
            if student.grades:
                all_grades.extend([g.score for g in student.grades])
        
        if not all_grades:
            return {
                'total_students': len(students),
                'average_class_grade': 0,
                'highest_grade': 0,
                'lowest_grade': 0
            }
        
        return {
            'total_students': len(students),
            'average_class_grade': round(sum(all_grades) / len(all_grades), 2),
            'highest_grade': max(all_grades),
            'lowest_grade': min(all_grades)
        }
