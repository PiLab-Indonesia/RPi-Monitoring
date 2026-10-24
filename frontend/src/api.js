/** Environment variable REACT_APP_API_BASE is embedded by the build script. */
export const DEFAULT_API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export async function fetchDevices({ apiBase = DEFAULT_API_BASE, fetchImpl = globalThis.fetch, signal } = {}) {
  if (typeof fetchImpl !== "function") throw new TypeError("fetch unavailable");
  const response = await fetchImpl(`${apiBase.replace(/\/+$/, "")}/devices`, {
    headers: { Accept: "application/json" },
    signal,
  });
  if (!response.ok) throw new Error(`Device API error HTTP ${response.status}`);
  const rows = await response.json();
  if (!Array.isArray(rows)) throw new TypeError("Device API must return an array");
  return rows.map((row) => {
    if (!row || typeof row !== "object" || typeof row.ip !== "string") {
      throw new TypeError("Malformed device in API response");
    }
    return {
      id: row.id,
      ip: row.ip,
      name: row.name || "Unnamed device",
      alive: Boolean(row.alive),
    };
  });
}
