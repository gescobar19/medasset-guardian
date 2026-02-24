const API_BASE = "http://127.0.0.1:8000";

export async function getAssets() {
  const res = await fetch(`${API_BASE}/assets`);
  if (!res.ok) throw new Error("Failed to fetch assets");
  return res.json();
}

export async function createAsset(payload) {
  const res = await fetch(`${API_BASE}/assets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create asset");
  return res.json();
}

export async function logUsage(payload) {
  const res = await fetch(`${API_BASE}/usage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || "Failed to log usage");
  }
  return res.json();
}

// You'll implement this once you build /risk-report/{asset_id}
export async function getRiskReport(assetId) {
  const res = await fetch(`${API_BASE}/risk-report/${assetId}`);
  if (!res.ok) throw new Error("Failed to fetch risk report");
  return res.json();
}