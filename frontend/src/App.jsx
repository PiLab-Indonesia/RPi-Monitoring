import React, { useCallback, useEffect, useState } from "react";
import { fetchDevices } from "./api.js";

export default function App() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updated, setUpdated] = useState(null);

  const refresh = useCallback(async ({ signal } = {}) => {
    setLoading(true);
    setError("");
    try {
      const rows = await fetchDevices({ signal });
      if (!signal?.aborted) {
        setDevices(rows);
        setUpdated(new Date());
      }
    } catch (cause) {
      if (!signal?.aborted) setError(cause instanceof Error ? cause.message : "Unable to fetch devices");
    } finally {
      if (!signal?.aborted) setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    refresh({ signal: controller.signal });
    return () => controller.abort();
  }, [refresh]);

  const online = devices.filter((row) => row.alive).length;
  return <main className="layout">
    <header className="topbar">
      <div><p className="eyebrow">RPi NETWORK MONITORING</p><h1>Device dashboard</h1>
        <p className="muted">Latest known connectivity of your Raspberry Pis</p></div>
      <button className="refresh" disabled={loading} onClick={() => refresh()} type="button">
        {loading ? "Loading…" : "Refresh"}</button>
    </header>
    <section className="summary" aria-label="Device summary">
      <div className="stat"><span>Total</span><strong>{devices.length}</strong></div>
      <div className="stat"><span>Online</span><strong className="online">{online}</strong></div>
      <div className="stat"><span>Offline</span><strong className="offline">{devices.length - online}</strong></div>
    </section>
    <section className="panel" aria-label="Devices">
      <div className="panel-heading"><h2>All devices</h2>
        <p className="muted">{updated ? `Last updated: ${updated.toLocaleTimeString()}` : "Awaiting first refresh"}</p></div>
      {error && <p className="error" role="alert">{error}</p>}
      {loading && devices.length === 0 ? <p className="message" role="status">Loading devices…</p>
        : devices.length === 0 ? <p className="message">{error ? "Data unavailable." : "No devices discovered yet."}</p>
        : <div className="table-wrap"><table><thead><tr><th>Device</th><th>IP address</th><th>Status</th></tr></thead>
          <tbody>{devices.map((row) => <tr key={row.id ?? row.ip}>
            <td><strong>{row.name}</strong></td><td className="mono">{row.ip}</td>
            <td><span className={row.alive ? "pill up" : "pill down"}>
              {row.alive ? "Online" : "Offline"}</span></td>
          </tr>)}</tbody></table></div>}
    </section>
  </main>;
}
