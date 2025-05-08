const BASE_URL = "http://127.0.0.1:5000";

// General
export async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  return await res.json();
}

export async function apiPost(path, data) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

export async function apiPut(path, data) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

export async function apiDelete(path) {
  const res = await fetch(`${BASE_URL}${path}`, { method: "DELETE" });
  return await res.json();
}

// Restaurant
export async function getRestaurantePorId(id) {
    const res = await fetch(`http://127.0.0.1:5000/restaurantes/${id}`);
    return await res.json();
}
  
