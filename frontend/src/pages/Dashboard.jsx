import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getStudents } from "../services/api";

export default function Dashboard() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    getStudents().then(res => setStudents(res.data));
  }, []);

  const courses = [...new Set(students.map(s => s.course))];
  return (
    <div>
      <h1>Student Performance Dashboard</h1>
      <div className="dashboard-grid">
        <div className="stat-card">
          <h3>Total Students</h3>
          <strong>{students.length}</strong>
        </div>

        <div className="stat-card">
          <h3>Courses</h3>
          <strong>{courses.length}</strong>
        </div>

        <div className="stat-card">
          <h3>AI Monitoring</h3>
          <strong>Active</strong>
        </div>
      </div>

      <h2>Students</h2>
      <div className="student-list">
        {students.map(student => (
          <div className="student-row" key={student.id}>
            <div>
              <strong>{student.name}</strong>
              <p>{student.roll_no}</p>
            </div>

            <div>{student.course} - Semester {student.semester}</div>
            <Link className="button" to={`/student/${student.id}`}>
              View
            </Link>
          </div>
        ))}
      
      </div>

    </div>
  );
}
