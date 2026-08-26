import React, { useState } from "react";
export default function Results({result}) {
  if (!result) return null;
  const a = result.aggregate;
  const metrics = [['Avg. waiting', a.average_waiting_time, 'ticks'], ['Avg. turnaround', a.average_turnaround_time, 'ticks'], ['CPU utilization', `${a.cpu_utilization}%`, 'efficiency'], ['Throughput', a.throughput, 'jobs / tick']];
  return <><div className="row g-3 mb-3">{metrics.map(([label,value,unit]) => <div className="col-sm-6 col-lg-3" key={label}><div className="card summary-card"><div className="card-body"><small>{label}</small><div className="fs-4 fw-bold">{value}</div><span>{unit}</span></div></div></div>)}</div><div className="card panel"><div className="card-body"><div className="panel-heading"><div><span className="section-kicker">Result set</span><h2 className="h5">Per-process metrics</h2></div><span className="live-label">Complete</span></div><div className="table-responsive"><table className="table"><thead><tr><th>PID</th><th>Arrival</th><th>Burst</th><th>Completion</th><th>Turnaround</th><th>Waiting</th></tr></thead><tbody>{result.metrics.map(m=><tr key={m.pid}><td><span className="pid-chip">{m.pid}</span></td><td>{m.arrival_time}</td><td>{m.burst_time}</td><td>{m.completion_time}</td><td>{m.turnaround_time}</td><td>{m.waiting_time}</td></tr>)}</tbody></table></div></div></div></>;
}
