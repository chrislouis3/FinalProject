from app import db
from datetime import datetime

class Student(db.Model):
    """Model untuk data siswa"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    nim = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nim': self.nim,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'average_grade': self.get_average_grade()
        }
    
    def get_average_grade(self):
        """Hitung rata-rata nilai siswa"""
        if not self.grades:
            return 0
        total = sum(grade.score for grade in self.grades)
        return round(total / len(self.grades), 2)
    
    def get_grade_letter(self):
        """Konversi rata-rata nilai ke huruf"""
        avg = self.get_average_grade()
        if avg >= 85:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 65:
            return 'C'
        elif avg >= 55:
            return 'D'
        else:
            return 'E'


class Grade(db.Model):
    """Model untuk data nilai siswa"""
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'score': self.score,
            'created_at': self.created_at.isoformat()
        }
    
    def is_valid_score(self):
        """Validasi nilai harus antara 0-100"""
        return 0 <= self.score <= 100
