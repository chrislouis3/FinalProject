// API Helper Functions
const API_URL = '/api';

async function apiCall(method, endpoint, data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(`${API_URL}${endpoint}`, options);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'API Error');
    }
    
    return await response.json();
}

// Load Statistics
async function loadStatistics() {
    try {
        const stats = await apiCall('GET', '/statistics');
        document.getElementById('totalStudents').textContent = stats.total_students;
        document.getElementById('averageGrade').textContent = stats.average_class_grade;
        document.getElementById('highestGrade').textContent = stats.highest_grade;
        document.getElementById('lowestGrade').textContent = stats.lowest_grade;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load Students
async function loadStudents() {
    try {
        const students = await apiCall('GET', '/students');
        const studentsList = document.getElementById('studentsList');
        
        if (students.length === 0) {
            studentsList.innerHTML = '<p style="text-align: center; color: #999;">Belum ada data siswa</p>';
            return;
        }
        
        studentsList.innerHTML = students.map(student => `
            <div class="student-card">
                <div class="student-header">
                    <div class="student-info">
                        <h4>${student.name}</h4>
                        <p>NIM: ${student.nim}</p>
                        <p>Email: ${student.email}</p>
                        <p><strong>Rata-rata:</strong> ${student.average_grade} / 100</p>
                    </div>
                    <div class="student-actions">
                        <button class="btn btn-danger" onclick="deleteStudent(${student.id})">Hapus</button>
                    </div>
                </div>
                
                <div class="student-grade-section">
                    <h5 style="margin-bottom: 0.8rem;">Nilai Mata Pelajaran:</h5>
                    <div id="grades-${student.id}" class="grades-list"></div>
                    
                    <div class="add-grade-form">
                        <input type="text" id="subject-${student.id}" placeholder="Mata Pelajaran" required>
                        <input type="number" id="score-${student.id}" placeholder="Nilai (0-100)" min="0" max="100" required>
                        <button onclick="addGrade(${student.id})">Tambah Nilai</button>
                    </div>
                </div>
            </div>
        `).join('');
        
        // Load grades for each student
        for (const student of students) {
            await loadStudentGrades(student.id);
        }
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

// Load Grades for a Student
async function loadStudentGrades(studentId) {
    try {
        const grades = await apiCall('GET', `/students/${studentId}/grades`);
        const gradesList = document.getElementById(`grades-${studentId}`);
        
        if (grades.length === 0) {
            gradesList.innerHTML = '<p style="color: #999; font-size: 0.9rem;">Belum ada nilai</p>';
            return;
        }
        
        gradesList.innerHTML = grades.map(grade => `
            <div class="grade-item">
                <div class="grade-info">
                    <p><strong>${grade.subject}</strong></p>
                    <p style="font-size: 0.8rem; color: #999;">${new Date(grade.created_at).toLocaleDateString()}</p>
                </div>
                <div class="grade-score">${grade.score}</div>
                <button class="btn btn-danger" onclick="deleteGrade(${grade.id})" style="padding: 0.3rem 0.6rem; font-size: 0.8rem;">Hapus</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading grades:', error);
    }
}

// Add Student
document.getElementById('addStudentForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const name = document.getElementById('studentName').value;
        const nim = document.getElementById('studentNim').value;
        const email = document.getElementById('studentEmail').value;
        
        await apiCall('POST', '/students', { name, nim, email });
        
        const messageDiv = document.getElementById('formMessage');
        messageDiv.className = 'message success';
        messageDiv.textContent = '✓ Siswa berhasil ditambahkan!';
        
        document.getElementById('addStudentForm').reset();
        loadStudents();
        loadStatistics();
        
        setTimeout(() => {
            messageDiv.textContent = '';
            messageDiv.className = 'message';
        }, 3000);
    } catch (error) {
        const messageDiv = document.getElementById('formMessage');
        messageDiv.className = 'message error';
        messageDiv.textContent = '✗ Error: ' + error.message;
    }
});

// Delete Student
async function deleteStudent(studentId) {
    if (!confirm('Yakin ingin menghapus siswa ini?')) return;
    
    try {
        await apiCall('DELETE', `/students/${studentId}`);
        loadStudents();
        loadStatistics();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Add Grade
async function addGrade(studentId) {
    try {
        const subject = document.getElementById(`subject-${studentId}`).value;
        const score = parseFloat(document.getElementById(`score-${studentId}`).value);
        
        if (!subject.trim()) {
            alert('Nama mata pelajaran tidak boleh kosong');
            return;
        }
        
        if (isNaN(score) || score < 0 || score > 100) {
            alert('Nilai harus antara 0-100');
            return;
        }
        
        await apiCall('POST', `/students/${studentId}/grades`, { subject, score });
        
        document.getElementById(`subject-${studentId}`).value = '';
        document.getElementById(`score-${studentId}`).value = '';
        
        await loadStudentGrades(studentId);
        loadStatistics();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Delete Grade
async function deleteGrade(gradeId) {
    if (!confirm('Yakin ingin menghapus nilai ini?')) return;
    
    try {
        await apiCall('DELETE', `/grades/${gradeId}`);
        loadStudents();
        loadStatistics();
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('studentsList')) {
        loadStatistics();
        loadStudents();
        
        // Refresh data every 30 seconds
        setInterval(loadStatistics, 30000);
    }
});
