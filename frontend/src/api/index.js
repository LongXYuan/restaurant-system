// 动态获取当前的域名/IP，确保手机访问时也能请求到正确的后端
const hostname = window.location.hostname;
const API_BASE = `http://${hostname}:8000/api`;

export const fetchTables = async () => {
  const res = await fetch(`${API_BASE}/tables`);
  if (!res.ok) throw new Error('获取桌台失败');
  return await res.json();
};