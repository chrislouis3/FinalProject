"""
Integration tests untuk API endpoints
"""
import pytest
import json
from app.services import StudentService, GradeService


class TestStudentAPI:
    """Integration tests untuk Student API"""
    
    def test_get_students_empty(self, client):
        """Test GET /api/students ketika kosong"""
        response = client.get('/api/students')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 0
    
    def test_create_student_api(self, client):
        """Test POST /api/students untuk membuat student"""
        payload = {
            'name': 'API Student',
            'nim': '2024500',
            'email': 'api@example.com'
        }
        response = client.post('/api/students',
                              data=json.dumps(payload),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'API Student'
        assert data['nim'] == '2024500'
    
    def test_create_student_missing_field(self, client):
        """Test POST /api/students dengan field missing"""
        payload = {
            'name': 'Incomplete Student',
            'nim': '2024501'
        }
        response = client.post('/api/students',
                              data=json.dumps(payload),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_get_single_student(self, client, app_context):
        """Test GET /api/students/<id>"""
        student = StudentService.create_student('Single Student', '2024502', 'single@example.com')
        
        response = client.get(f'/api/students/{student.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Single Student'
    
    def test_get_student_not_found(self, client):
        """Test GET /api/students/<id> dengan student tidak ditemukan"""
        response = client.get('/api/students/99999')
        
        assert response.status_code == 404
    
    def test_update_student_api(self, client, app_context):
        """Test PUT /api/students/<id>"""
        student = StudentService.create_student('Update Student', '2024503', 'update@example.com')
        
        payload = {
            'name': 'Updated Student',
            'email': 'updated@example.com'
        }
        response = client.put(f'/api/students/{student.id}',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Student'
        assert data['email'] == 'updated@example.com'
    
    def test_delete_student_api(self, client, app_context):
        """Test DELETE /api/students/<id>"""
        student = StudentService.create_student('Delete Student', '2024504', 'delete@example.com')
        
        response = client.delete(f'/api/students/{student.id}')
        
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get(f'/api/students/{student.id}')
        assert response.status_code == 404


class TestGradeAPI:
    """Integration tests untuk Grade API"""
    
    @pytest.fixture
    def api_student(self, app_context):
        """Create student untuk API testing"""
        return StudentService.create_student('Grade API Student', '2024600', 'gradeapi@example.com')
    
    def test_add_grade_api(self, client, api_student, app_context):
        """Test POST /api/students/<id>/grades"""
        payload = {
            'subject': 'Mathematics',
            'score': 85.0
        }
        response = client.post(f'/api/students/{api_student.id}/grades',
                              data=json.dumps(payload),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['subject'] == 'Mathematics'
        assert data['score'] == 85.0
    
    def test_get_student_grades_api(self, client, api_student, app_context):
        """Test GET /api/students/<id>/grades"""
        GradeService.add_grade(api_student.id, 'Physics', 90.0)
        GradeService.add_grade(api_student.id, 'Chemistry', 88.0)
        
        response = client.get(f'/api/students/{api_student.id}/grades')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
    
    def test_add_grade_invalid_score(self, client, api_student):
        """Test POST /api/students/<id>/grades dengan score invalid"""
        payload = {
            'subject': 'Biology',
            'score': 105.0
        }
        response = client.post(f'/api/students/{api_student.id}/grades',
                              data=json.dumps(payload),
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_update_grade_api(self, client, api_student, app_context):
        """Test PUT /api/grades/<id>"""
        grade = GradeService.add_grade(api_student.id, 'History', 80.0)
        
        payload = {
            'subject': 'World History',
            'score': 92.0
        }
        response = client.put(f'/api/grades/{grade.id}',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['subject'] == 'World History'
        assert data['score'] == 92.0
    
    def test_delete_grade_api(self, client, api_student, app_context):
        """Test DELETE /api/grades/<id>"""
        grade = GradeService.add_grade(api_student.id, 'Art', 87.0)
        
        response = client.delete(f'/api/grades/{grade.id}')
        
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get(f'/api/students/{api_student.id}/grades')
        data = json.loads(response.data)
        assert len(data) == 0


class TestStatisticsAPI:
    """Integration tests untuk Statistics API"""
    
    def test_get_statistics_empty(self, client):
        """Test GET /api/statistics ketika kosong"""
        response = client.get('/api/statistics')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_students'] == 0
        assert data['average_class_grade'] == 0
    
    def test_get_statistics_with_data(self, client, app_context):
        """Test GET /api/statistics dengan data"""
        student1 = StudentService.create_student('Stats Test 1', '2024700', 'stats1@example.com')
        student2 = StudentService.create_student('Stats Test 2', '2024701', 'stats2@example.com')
        
        GradeService.add_grade(student1.id, 'Math', 80.0)
        GradeService.add_grade(student1.id, 'Science', 90.0)
        GradeService.add_grade(student2.id, 'Math', 70.0)
        
        response = client.get('/api/statistics')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_students'] == 2
        assert data['highest_grade'] == 90.0
