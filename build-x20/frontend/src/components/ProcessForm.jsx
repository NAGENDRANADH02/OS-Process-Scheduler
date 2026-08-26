import React from "react";
const names = {fcfs:'FCFS', sjf_non_preemptive:'SJF (Non-preemptive)', sjf_preemptive:'SJF (Preemptive)', round_robin:'Round Robin', priority_non_preemptive:'Priority (Non-preemptive)', priority_preemptive:'Priority (Preemptive)'};
export default function ProcessForm({input, setInput, onRun, onCompare, onSave, loading}) {
  const priority = input.algorithm.startsWith('priority');
  const changeProcess = (index, field, value) => setInput(x => ({...x, processes:x.processes.map((p,i) => i === index ? {...p,[field]:value} : p)}));
  const add = () => setInput(x => ({...x, processes:[...x.processes,{pid:`P${x.processes.length+1}`,arrival_time:0,burst_time:1,priority:1}]}));
  const remove = (i) => setInput(x => ({...x, processes:x.processes.filter((_, index) => index !== i).map((p,index) => ({...p,pid:`P${index+1}`}))}));
  return <div className="card shadow-sm"><div className="card-body">
    <h2 className="h5">Workload</h2><div className="row g-3 mb-3"><div className="col-md-7"><label className="form-label">Algorithm</label><select className="form-select" value={input.algorithm} onChange={e=>setInput(x=>({...x,algorithm:e.target.value}))}>{Object.entries(names).map(([v,n])=><option key={v} value={v}>{n}</option>)}</select></div>
    {input.algorithm === 'round_robin' && <div className="col-md-5"><label className="form-label">Time quantum</label><input className="form-control" type="number" min="1" value={input.time_quantum} onChange={e=>setInput(x=>({...x,time_quantum:+e.target.value}))}/></div>}</div>
    <div className="table-responsive"><table className="table table-sm align-middle"><thead><tr><th>PID</th><th>Arrival</th><th>Burst</th>{priority && <th>Priority*</th>}<th/></tr></thead><tbody>{input.processes.map((p,i)=><tr key={p.pid}><td>{p.pid}</td>{['arrival_time','burst_time'].map(field=><td key={field}><input aria-label={`${p.pid} ${field}`} className="form-control" type="number" min={field==='burst_time'?1:0} value={p[field]} onChange={e=>changeProcess(i,field,+e.target.value)}/></td>)}{priority && <td><input aria-label={`${p.pid} priority`} className="form-control" type="number" value={p.priority} onChange={e=>changeProcess(i,'priority',+e.target.value)}/></td>}<td><button className="btn btn-outline-danger btn-sm" disabled={input.processes.length===1} onClick={()=>remove(i)}>×</button></td></tr>)}</tbody></table></div>
    <button className="btn btn-outline-primary btn-sm me-2" onClick={add}>+ Add process</button><button className="btn btn-primary me-2" disabled={loading} onClick={onRun}>Run simulation</button><button className="btn btn-dark me-2" disabled={loading} onClick={onCompare}>Compare algorithms</button><button className="btn btn-success" disabled={loading} onClick={onSave}>Save run</button>
    <p className="small text-muted mt-3 mb-0">* Lower numeric priority runs first.</p>
  </div></div>;
}
