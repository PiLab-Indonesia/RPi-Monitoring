# Dashboard (Manager) — RPi-NMS

This guide documents how to run, configure, and validate the React Dashboard for the **RPi Network Monitoring System (RPi-NMS)** locally and during Pull Request reviews.

---

## 1. Prerequisites

- **Backend API**: Python 3.9+ running FastAPI (`uvicorn app.main:app --host 0.0.0.0 --port 8000`) or Docker container (`docker-compose up -d`).
- **Node.js & npm**: Node.js 18+ LTS and `npm` (or `pnpm`/`yarn`).

---

## 2. Running the Dashboard Locally

1. **Start the FastAPI Backend** (from the repository root):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Verify the health check endpoint responds at `http://localhost:8000/`:
   ```json
   {"status": "ok", "version": "0.1.0"}
   ```

2. **Start the React Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```
   The React development server will launch at `http://localhost:3000` and connect to `http://localhost:8000` by default (configurable via `REACT_APP_API_URL`).

---

## 3. Core API Endpoints Consumed by the Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check and backend version status |
| `GET` | `/devices` | List all discovered/monitored devices (`id`, `ip`, `name`, `alive`) |
| `GET` | `/devices/{device_id}` | Fetch detailed status for a single monitored device |
| `POST` | `/auth/token` | Authenticate manager/operator credentials and issue JWT bearer token |

---

## 4. Manager Guidance: Validating Pull Requests

When reviewing and validating dashboard or backend PRs, managers should follow this checklist:

1. **Automated CI Verification**:
   - Confirm the GitHub Actions `CI` workflow (`pytest -q` and `flake8 --max-line-length=120`) passes on the PR branch.
2. **Backend + Dashboard Smoke Test**:
   - Start the backend (`uvicorn app.main:app --port 8000`) and frontend (`cd frontend && npm start`).
   - Verify the device table renders all entries returned by `GET /devices` and accurately reflects `alive: true/false` status indicators.
3. **Alert & Discovery Regression Check**:
   - Trigger a state transition (online -> offline) and confirm `AlertRules.process_state` records the transition in `device_history` without breaking dashboard polling.
4. **Build Verification**:
   - Run `npm run build` inside `frontend/` to ensure zero TypeScript/JSX compilation or bundle errors before merging.
