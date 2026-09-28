export default function PerformanceCard({ title, value }) {
  return (
    <div className="performance-card">
      <h3>{title}</h3>
      <div className="card-value">{value}</div>
    </div>
  );
}
