import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getStudent, getPerformance, getAnalysis } from "../services/api";
import PerformanceCard from "../components/PerformanceCard";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function StudentProfile() {
  const { id } = useParams();
  const [student, setStudent] = useState(null);
  const [records, setRecords] = useState([]);
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    Promise.all([
      getStudent(id), getPerformance(id), getAnalysis(id)
    ]).then(([a,b,c]) => {
      setStudent(a.data);
      setRecords(b.data);
      setAnalysis(c.data);
    });
  }, [id]);

  if (!student) return <h2>Loading...</h2>;
  
  return (
    <div>
      <h1>{student.name}</h1>
      <p>{student.roll_no} | {student.course} | Semester {student.semester}</p>

      {analysis && !analysis.message && (
        <>
          <div className="dashboard-grid">
            <PerformanceCard title="Overall Score"
              value={`${analysis.overall_score}%`} />
      
            <PerformanceCard title="Attendance"
              value={`${analysis.attendance}%`} />
      
            <PerformanceCard title="Risk Level"
              value={analysis.risk} />
      
            <PerformanceCard title="High Risk Probability"
              value={`${analysis.high_risk_probability}%`} />
          </div>
      
          <div className="chart-container">
            <h2>Performance Analysis</h2>

            <ResponsiveContainer width="100%" height={350}>
            
              <BarChart data={[
                {name:"Attendance",value:analysis.attendance},
                {name:"Internal",value:analysis.internal_marks},
                {name:"Assignment",value:analysis.assignment_marks},
                {name:"Practical",value:analysis.practical_marks},
                {name:"Quiz",value:analysis.quiz_marks}
              ]}>

                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="recommendation-box">
            <h2>AI Recommendations</h2>
            <ul>
              {analysis.recommendations.map((x,i) =>
                <li key={i}>{x}</li>
              )}
            </ul>
          </div>
        </>
      )}
      <h2>Subject Performance</h2>
      <div className="student-list">

        {records.map(r => (
          <div className="student-row" key={r.id}>
            <strong>{r.subject}</strong>
            <span>Attendance: {r.attendance}%</span>
            <span>Internal: {r.internal_marks}</span>
            <span>Practical: {r.practical_marks}</span>
          </div>
        ))}
      </div>
      
      <Link className="ai-button" to={`/ai/${student.id}`}>
        Ask AI Academic Advisor
      </Link>
    </div>
  );
}
