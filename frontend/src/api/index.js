// 动态获取当前的域名/IP，确保手机访问时也能请求到正确的后端
const hostname = window.location.hostname;
const API_BASE = `http://${hostname}:8000/api`;

export const fetchTables = async () => {
  const res = await fetch(`${API_BASE}/tables`);
  if (!res.ok) throw new Error('获取桌台失败');
  return await res.json();
};

export const fetchMenu = async () => {
  const res = await fetch(`${API_BASE}/menu`);
  if (!res.ok) throw new Error('获取菜单失败');
  return await res.json();
};

export const submitOrderApi = async (orderData) => {
  const res = await fetch(`${API_BASE}/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(orderData)
  });
  if (!res.ok) throw new Error('提交订单失败');
  return await res.json();
};