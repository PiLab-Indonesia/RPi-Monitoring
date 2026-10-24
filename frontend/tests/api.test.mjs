import { test } from "node:test";
import assert from "node:assert/strict";
import { fetchDevices } from "../src/api.js";

test("normalizes server data and strips API base trailing slash", async () => {
  const rows = await fetchDevices({
    apiBase: "http://localhost:8000/",
    fetchImpl: async (url, options) => {
      assert.equal(url, "http://localhost:8000/devices");
      assert.equal(options.headers.Accept, "application/json");
      return { ok: true, json: async () => [
        { id: 1, ip: "192.0.2.1", name: "Pi", alive: true },
        { id: 2, ip: "192.0.2.2", name: null, alive: 0 },
      ] };
    },
  });
  assert.deepEqual(rows, [
    { id: 1, ip: "192.0.2.1", name: "Pi", alive: true },
    { id: 2, ip: "192.0.2.2", name: "Unnamed device", alive: false },
  ]);
});
test("accepts empty records", async () => assert.deepEqual(await fetchDevices({
  fetchImpl: async () => ({ ok: true, json: async () => [] }),
}), []));
test("reports HTTP error", async () => assert.rejects(fetchDevices({
  fetchImpl: async () => ({ ok: false, status: 503 }),
}), /503/));
test("rejects malformed outer payload", async () => assert.rejects(fetchDevices({
  fetchImpl: async () => ({ ok: true, json: async () => ({ devices: [] }) }),
}), /array/));
test("rejects malformed entries", async () => assert.rejects(fetchDevices({
  fetchImpl: async () => ({ ok: true, json: async () => [{ id: 1 }] }),
}), /Malformed/));
test("passes abort signal", async () => {
  const controller = new AbortController();
  await fetchDevices({ signal: controller.signal, fetchImpl: async (_, opts) => {
    assert.equal(opts.signal, controller.signal);
    return { ok: true, json: async () => [] };
  } });
});
test("requires fetch implementation", async () => assert.rejects(fetchDevices({
  fetchImpl: null,
}), /unavailable/));
