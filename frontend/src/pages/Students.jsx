import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getStudents, createStudent, deleteStudent } from "../services/api";

export default function Students() {
  const [students, setStudents] = useState([]);
  
  const [form, setForm] = useState({
    name: "", roll_no: "", course: "", semester: "",
    section: "", email: "", previous_cgpa: ""
  });

  const load = async () => {
    const r = await getStudents();
    setStudents(r.data);
  };

  useEffect(() => { load(); }, []);
  const change = e => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async e => {
    e.preventDefault();

    try {
      await createStudent({
        ...form,
        semester: Number(form.semester),
        previous_cgpa: Number(form.previous_cgpa)
      });

      setForm({
        name: "", roll_no: "", course: "", semester: "",
        section: "", email: "", previous_cgpa: ""
      });

      load();
    } catch (e) {
      alert(e.response?.data?.detail || "Error");
    }
  };

  const remove = async id => {
    if (confirm("Delete this student?")) {
      await deleteStudent(id);
      load();
    }
  };

  return (
    <div>
      <h1>Students</h1>
      <form className="student-form" onSubmit={submit}>

        <input name="name" placeholder="Student Name"
          value={form.name} onChange={change} required />
      
        <input name="roll_no" placeholder="Roll Number"
          value={form.roll_no} onChange={change} required />
      
        <input name="course" placeholder="Course"
          value={form.course} onChange={change} />
      
        <input name="semester" placeholder="Semester" type="number" min="1" max="8"
          value={form.semester} onChange={change} />
      
        <input name="section" placeholder="Section"
          value={form.section} onChange={change} />
      
        <input name="email" type="email" placeholder="Email"
          value={form.email} onChange={change} />
      
        <input name="previous_cgpa" placeholder="Previous CGPA" type="number" step="0.01"
          value={form.previous_cgpa} onChange={change} />
      
        <button>Add Student</button>
      </form>
      
      <div className="student-list">
      
        {students.map(s => (
          <div className="student-row" key={s.id}>
            <div>
              <strong>{s.name}</strong>
              <p>{s.roll_no}</p>
            </div>
            
            <div>{s.course} / Sem {s.semester}</div>
            <Link className="button" to={`/student/${s.id}`}>Profile</Link>
            <button className="delete-button" onClick={() => remove(s.id)} >Delete</button>

          </div>
        ))}

      </div>
    </div>
  );
}
