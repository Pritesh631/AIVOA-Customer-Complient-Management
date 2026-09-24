const API = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';
export async function getComplaints(){return fetch(`${API}/complaints`).then(r=>r.json())}
export async function analyze(data){const r=await fetch(`${API}/analyze`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});if(!r.ok)throw new Error(await r.text());return r.json()}
export async function saveComplaint(data){const r=await fetch(`${API}/complaints`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});if(!r.ok)throw new Error(await r.text());return r.json()}
export async function analyzeFile(file){const fd=new FormData();fd.append('file',file);const r=await fetch(`${API}/analyze-file`,{method:'POST',body:fd});if(!r.ok)throw new Error(await r.text());return r.json()}
