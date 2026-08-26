import React, { useEffect, useState } from "react";

import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
export default function Comparison({data}) {if(!data) return null; return <div className="card shadow-sm"><div className="card-body"><h2 className="h5">Average waiting time comparison</h2><div style={{height:300}}><ResponsiveContainer><BarChart data={data}><CartesianGrid strokeDasharray="3 3"/><XAxis dataKey="algorithm"/><YAxis/><Tooltip/><Bar dataKey="waiting" fill="#0d6efd" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div></div></div>}
