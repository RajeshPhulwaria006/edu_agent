import { Link } from "react-router-dom";
export default function Sidebar() {
  return (
    <aside className="sidebar">
      <Link to="/">Dashboard</Link>
      <Link to="/students">Students</Link>
    </aside>
  );
}
