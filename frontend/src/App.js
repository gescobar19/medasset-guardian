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

  const totalEquipment = assets.length;

  const operationalCount =
    assets.filter(a => a.status === "ACTIVE").length;

  const retiredCount =
    assets.filter(a => a.status === "RETIRED").length;

  const inspectionCount =
    assets.filter(
      a => a.status === "NEEDS_INSPECTION"
    ).length;

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
      <h1>MedAsset Guardian</h1>
      <p>
        Medical Equipment Lifecycle &
        Risk Management Platform
      </p>

      {error && (
        <div style={{ padding: 12, background: "#ffe5e5", marginBottom: 16 }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      <section style={{ marginBottom: 32 }}>
      <h2>Dashboard</h2>

      <div
        style={{
          display: "flex",
          gap: 16,
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 16,
            minWidth: 180,
          }}
        >
          <h3>{totalEquipment}</h3>
          <p>Total Equipment</p>
        </div>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 16,
            minWidth: 180,
          }}
        >
          <h3>{operationalCount}</h3>
          <p>Operational</p>
        </div>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 16,
            minWidth: 180,
          }}
        >
          <h3>{inspectionCount}</h3>
          <p>Needs Inspection</p>
        </div>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 16,
            minWidth: 180,
          }}
        >
          <h3>{retiredCount}</h3>
          <p>Out of Service</p>
        </div>
      </div>
    </section>

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
        <h2>Register Equipment</h2>
        <form onSubmit={handleCreateAsset}>
          <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
            <input
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="Name (e.g., Ventilator #14)"
              style={{ flex: 2 }}
              required
            />
            <select value={newType} onChange={(e) => setNewType(e.target.value)} style={{ flex: 1 }}>
              <option value="ventilator">Ventilator</option>
              <option value="infusion_pump">Infusion Pump</option>
              <option value="defibrillator">Defibrillator</option>
              <option value="mri_scanner">MRI Scanner</option>
              <option value="xray_machine">X-Ray Machine</option>
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
        <div
          style={{
            background: "#f6f6f6",
            padding: 16,
            borderRadius: 8,
            marginTop: 12,
            border: "1px solid #ddd",
          }}
        >
          <h3>Equipment Risk Assessment</h3>

          <p>
            <strong>Name:</strong> {riskReport.name}
          </p>

          <p>
            <strong>Type:</strong> {riskReport.type}
          </p>

          <p>
            <strong>Health Score:</strong> {riskReport.health_score}/100
          </p>

          <p>
          <strong>Risk Level:</strong>{" "}
          <span
            style={{
              color:
                riskReport.risk_level === "LOW"
                  ? "green"
                  : riskReport.risk_level === "MEDIUM"
                  ? "orange"
                  : "red",
              fontWeight: "bold",
            }}
          >
            {riskReport.risk_level}
          </span>
        </p>

        <p>
          <strong>Status:</strong> {riskReport.recommended_status}
        </p>

        <p>
          <strong>Total Uses:</strong> {riskReport.total_uses}
        </p>

        <p>
          <strong>Maximum Uses:</strong> {riskReport.max_allowed_uses}
        </p>

        <p>
          <strong>Remaining Service Life:</strong>{" "}
          {riskReport.remaining_uses} cycles
        </p>
        
        <p>
          <strong>Recommendation:</strong>{" "}
          {riskReport.recommendation}
        </p>

        <p>
          <strong>Reason:</strong> {riskReport.reason}
        </p>
      </div>
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