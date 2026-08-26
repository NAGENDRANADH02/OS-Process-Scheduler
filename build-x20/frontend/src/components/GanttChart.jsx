import React, { useEffect, useState } from "react";
import { motion } from 'framer-motion';
const palette = ['#0d6efd','#6f42c1','#198754','#fd7e14','#d63384','#0dcaf0'];
export default function GanttChart({segments}) {
  if (!segments?.length) return null;
  const end = segments.at(-1).end;
  const color = (pid) => pid === 'IDLE' ? '#6c757d' : palette[(Number(pid.replace(/\D/g,'')) - 1) % palette.length];
  return <div className="card panel gantt-panel"><div className="card-body"><div className="panel-heading"><div><span className="section-kicker">Execution trace</span><h2 className="h5">CPU Gantt chart</h2></div><span className="timeline-total">{end} ticks</span></div><div className="gantt">{segments.map((s,i)=><motion.div key={`${s.pid}-${s.start}`} className="gantt-block" title={`${s.pid}: ${s.start} → ${s.end}`} style={{backgroundColor:color(s.pid), width:`${((s.end-s.start)/end)*100}%`}} initial={{scaleX:0,opacity:0}} animate={{scaleX:1,opacity:1}} transition={{duration:.35,delay:i*.18}}><span>{s.pid}</span><small>{s.start}–{s.end}</small></motion.div>)}</div><div className="timeline-labels"><span>t = 0</span><span>t = {end}</span></div></div></div>;
}
