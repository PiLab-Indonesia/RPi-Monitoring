# Dashboard (Manager) — RPi-NMS (`docs/DASHBOARD.md`)

Comprehensive guide for managers and reviewers to run, configure, and validate the **RPi-Monitoring React Dashboard** locally when reviewing Pull Requests.

---

## 1. Prerequisites

- **Node.js** `>= 18.x` and **npm** `>= 9.x`
- **Backend API** running locally (`http://localhost:8000`) via Docker Compose or Uvicorn:
  ```bash
  docker compose up -d
  # OR locally:
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

---

## 2. Running the React Dashboard Locally

From the repository root:

```bash
cd frontend
npm install
npm start
```

The development server starts at **`http://localhost:3000`** and proxies API calls to `http://localhost:8000` (configurable via `REACT_APP_API_URL`).

### Custom Backend URL

```bash
REACT_APP_API_URL=http://192.168.1.10:8000 npm start
```

---

## 3. Manager PR Validation Checklist

When validating a contributor's Pull Request affecting the dashboard or backend API:

1. **Checkout the PR branch:**
   ```bash
   gh pr checkout <PR_NUMBER>
   ```
2. **Start Backend & Frontend:**
   - Verify `GET http://localhost:8000/docs` responds (`200 OK`).
   - Run `npm install && npm start` inside `frontend/`.
3. **Verify Core Views:**
   - **Device List & Status Badges:** Online/Offline indicators, CPU temperature, memory, and disk usage gauges update cleanly.
   - **Auto-Discovery & SNMP:** Newly discovered Raspberry Pi nodes appear without console errors.
   - **Alert Rules:** Triggering a threshold highlights the alert state in the UI.
4. **Production Build Verification:**
   ```bash
   cd frontend
   npm run build
   ```
   Ensure the production bundle compiles with zero TypeScript/ESLint errors.

---

## 4. Troubleshooting

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| `Network Error` / Empty device table | Backend not reachable or CORS blocked | Ensure backend runs on `:8000` and `REACT_APP_API_URL` matches |
| `ENOSPC` / watcher error on Linux | Low `fs.inotify.max_user_watches` | Run `sudo sysctl fs.inotify.max_user_watches=524288` |
| Port `3000` already in use | Another dev server running | Run `PORT=3001 npm start` |
