const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function getCities() {
  const res = await fetch(`${API_BASE_URL}/cities`);
  if (!res.ok) throw new Error("Failed to fetch cities");
  return res.json();
}

export async function getSites(city: string) {
  const res = await fetch(`${API_BASE_URL}/sites?city=${city}`);
  if (!res.ok) throw new Error("Failed to fetch sites");
  return res.json();
}

export async function getSiteDetail(id: string) {
  const res = await fetch(`${API_BASE_URL}/site/${id}`);
  if (!res.ok) throw new Error("Failed to fetch site detail");
  return res.json();
}
