import { useEffect, useState } from "react";
import { getAssets, createAsset, logUsage, getRiskReport } from "./api";

function App() {
  const [assets, setAssets] = useState([]);
  const [loadingAssets, setLoadingAssets] = useState(false);
  const [error, setError] = useState("");

  // Create asset form state
  const [newName, setNewName] = useState("");
  const [newType, setNewType] = useState("rope");
  const [newMaxUses, setNewMaxUses] = useState(100);

  // Usage form state
  const [usageAssetId, setUsageAssetId] = useState("");
  const [usesAdded, setUsesAdded] = useState(1);

  // Risk report state
  const [riskAssetId, setRiskAssetId] = useState("");
  const [riskReport, setRiskReport] = useState(null);

  async function refreshAssets() {
    setError("");
    setLoadingAssets(true);
    try {
      const data = await getAssets();
      setAssets(data);
    } catch (e) {
      setError(e.message || "Failed to load assets");
    } finally {
      setLoadingAssets(false);
    }
  }

  useEffect(() => {
    refreshAssets();
  }, []);

  async function handleCreateAsset(e) {
    e.preventDefault();
    setError("");
    try {
      await createAsset({
        name: newName,
        type: newType,
        max_allowed_uses: Number(newMaxUses),
      });
      setNewName("");
      await refreshAssets();
    } catch (e) {
      setError(e.message || "Create asset failed");
    }
  }

  async function handleLogUsage(e) {
    e.preventDefault();
    setError("");
    try {
      await logUsage({
        asset_id: Number(usageAssetId),
        uses_added: Number(usesAdded),
      });
      setUsesAdded(1);
      await refreshAssets();
    } catch (e) {
      setError(e.message || "Log usage failed");
    }
  }

  async function handleGetRisk(e) {
    e.preventDefault();
    setError("");
    setRiskReport(null);
    try {
      const data = await getRiskReport(Number(riskAssetId));
      setRiskReport(data);
    } catch (e) {
      setError(
        (e.message || "Risk report failed") +
          " (If you haven't built /risk-report yet, this is expected.)"
      );
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 16 }}>
      <h1>SummitSafe</h1>
      <p>Climbing gear lifecycle prototype (React + FastAPI)</p>

      {error && (
        <div style={{ padding: 12, background: "#ffe5e5", marginBottom: 16 }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Assets List */}
      <section style={{ marginBottom: 32 }}>
        <h2>Assets</h2>
        <button onClick={refreshAssets} disabled={loadingAssets}>
          {loadingAssets ? "Refreshing..." : "Refresh"}
        </button>

        <div style={{ marginTop: 12 }}>
          {assets.length === 0 ? (
            <p>No assets yet.</p>
          ) : (
            <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Max Uses</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((a) => (
                  <tr key={a.id}>
                    <td>{a.id}</td>
                    <td>{a.name}</td>
                    <td>{a.type}</td>
                    <td>{a.status}</td>
                    <td>{a.max_allowed_uses}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>

      {/* Create Asset */}
      <section style={{ marginBottom: 32 }}>
        <h2>Create Asset</h2>
        <form onSubmit={handleCreateAsset}>
          <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
            <input
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="Name (e.g., Mammut 9.8mm Rope)"
              style={{ flex: 2 }}
              required
            />
            <select value={newType} onChange={(e) => setNewType(e.target.value)} style={{ flex: 1 }}>
              <option value="rope">rope</option>
              <option value="harness">harness</option>
              <option value="carabiner">carabiner</option>
              <option value="belay_device">belay_device</option>
            </select>
            <input
              type="number"
              value={newMaxUses}
              onChange={(e) => setNewMaxUses(e.target.value)}
              min="1"
              style={{ width: 140 }}
              required
            />
          </div>
          <button type="submit">Create</button>
        </form>
      </section>

      {/* Log Usage */}
      <section style={{ marginBottom: 32 }}>
        <h2>Log Usage</h2>
        <form onSubmit={handleLogUsage}>
          <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
            <input
              type="number"
              value={usageAssetId}
              onChange={(e) => setUsageAssetId(e.target.value)}
              placeholder="Asset ID"
              min="1"
              style={{ width: 140 }}
              required
            />
            <input
              type="number"
              value={usesAdded}
              onChange={(e) => setUsesAdded(e.target.value)}
              placeholder="Uses added"
              min="1"
              style={{ width: 140 }}
              required
            />
            <button type="submit">Submit</button>
          </div>
        </form>
      </section>

      {/* Risk Report */}
      <section style={{ marginBottom: 32 }}>
        <h2>Risk Report</h2>
        <form onSubmit={handleGetRisk}>
          <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
            <input
              type="number"
              value={riskAssetId}
              onChange={(e) => setRiskAssetId(e.target.value)}
              placeholder="Asset ID"
              min="1"
              style={{ width: 140 }}
              required
            />
            <button type="submit">Get Risk</button>
          </div>
        </form>

        {riskReport && (
          <pre style={{ background: "#f6f6f6", padding: 12, overflowX: "auto" }}>
            {JSON.stringify(riskReport, null, 2)}
          </pre>
        )}
        {!riskReport && (
          <p style={{ color: "#666" }}>
            (If you haven’t built <code>/risk-report</code> yet, this will error — that’s normal.)
          </p>
        )}
      </section>
    </div>
  );
}

export default App;