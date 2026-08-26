const BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
async function call(path, body) {
  const response = await fetch(`${BASE}${path}`, body && {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
  if (!response.ok) throw new Error((await response.json()).detail || 'Request failed');
  return response.json();
}
export const schedule = (input) => call('/schedule/', input);
export const saveSchedule = (input) => call('/schedule/save/', input);
export const history = () => call('/schedule/history/');
