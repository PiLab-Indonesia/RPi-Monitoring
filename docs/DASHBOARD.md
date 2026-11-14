# Dashboard (Manager) — RPi-NMS

This document explains how to run the React Dashboard locally and how managers can use it to validate pull requests.

## Overview

The dashboard is a React application that communicates with the RPi-NMS backend API. By default, the backend is expected to be available at:

```text
http://localhost:8000
```

The frontend is typically started with the React development server and is available at:

```text
http://localhost:3000
```

If the frontend starts on a different port, use the URL printed in the terminal.

## Prerequisites

Install the following tools before running the dashboard:

- Node.js and npm
  - Use the Node.js version required by `frontend/package.json`.
  - Node.js LTS is recommended.
- Docker and Docker Compose, if running the backend in a container.
- Python 3.9+ and pip, if running the backend directly without Docker.
- Git, to check out pull request branches.

## Run the Backend

The dashboard needs the backend API to be running. Start the backend from the repository root.

### Option A: Run with Docker Compose

From the repository root:

```bash
docker compose up --build
```

This starts the backend on:

```text
http://localhost:8000
```

The Docker Compose configuration mounts:

- `./app` to `/app`
- `./config` to `/config`

It also sets:

```text
CONFIG_PATH=/config/config.yml
```

To stop the backend:

```bash
docker compose down
```

### Option B: Run Locally Without Docker

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

Confirm the backend is responding at:

```text
http://localhost:8000
```

If the backend uses a health endpoint or API documentation endpoint, open that endpoint in a browser to confirm it is running.

## Run the Dashboard

From the repository root:

```bash
cd frontend
npm install
npm start
```

Then open the URL printed by the React development server, usually:

```text
http://localhost:3000
```

You do not need to run `npm install` every time. Run it again when frontend dependencies change.

## Configure the Dashboard API URL

The dashboard must be able to reach the backend API.

By default, the backend is expected at:

```text
http://localhost:8000
```

If the backend is running on a different host or port, update the frontend API base URL before starting the dashboard.

If the frontend is configured through an environment variable, set it before running `npm start`. For example:

```bash
REACT_APP_API_BASE_URL=http://localhost:8000 npm start
```

Use the environment variable name and configuration mechanism defined by the frontend project. If the project does not use an environment variable, update the frontend API configuration file before starting the development server.

## Manager PR Validation Workflow

Use this workflow to validate dashboard-related pull requests.

### 1. Check Out the PR Branch

Check out the pull request branch using your normal GitHub workflow.

From the repository root, confirm you are on the expected branch:

```bash
git status
git branch --show-current
```

### 2. Start the Backend

Start the backend using Docker Compose:

```bash
docker compose up --build
```

Or start it locally without Docker:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Confirm the backend is available at:

```text
http://localhost:8000
```

### 3. Start the Dashboard

In a second terminal, from the repository root:

```bash
cd frontend
npm install
npm start
```

Open the dashboard at the URL printed by the development server, usually:

```text
http://localhost:3000
```

### 4. Validate the Dashboard

Confirm the following:

- The dashboard loads without a blank screen.
- The browser developer console does not show new errors.
- The dashboard can reach the backend API.
- Monitoring data is displayed when the backend is running.
- Loading states appear correctly while data is being fetched.
- Empty states appear correctly when no data is available.
- Error states appear correctly when the backend is unavailable.
- Navigation between dashboard views works.
- Refreshing the browser does not break the dashboard.
- The changes described in the PR match the expected behavior.

### 5. Validate the PR-Specific Changes

Review the pull request description and acceptance criteria. Then verify:

- The new or changed UI is visible and usable.
- The changed behavior works with real backend data.
- The changed behavior works when the backend returns no data.
- The changed behavior works when the backend is unavailable.
- Existing dashboard features still work.
- No unrelated UI regressions were introduced.

### 6. Capture Evidence

For the PR review, capture evidence such as:

- A screenshot of the dashboard after the change.
- A screenshot of any new loading, empty, or error state.
- Browser console output if relevant.
- Backend terminal output if relevant.
- A short note describing what was tested.

### 7. Stop Local Services

Stop the frontend development server with:

```text
Ctrl+C
```

Stop the Docker Compose backend with:

```bash
docker compose down
```

If the backend was started locally with `uvicorn`, stop it with:

```text
Ctrl+C
```

## PR Validation Checklist

Use this checklist when reviewing dashboard pull requests:

- [ ] Backend starts without errors.
- [ ] Frontend dependencies install successfully.
- [ ] Frontend development server starts without errors.
- [ ] Dashboard loads at the local development URL.
- [ ] Browser console has no new errors.
- [ ] Dashboard can reach the backend API.
- [ ] Monitoring data is displayed correctly.
- [ ] Loading states behave correctly.
- [ ] Empty states behave correctly.
- [ ] Error states behave correctly when the backend is unavailable.
- [ ] Navigation and refresh work correctly.
- [ ] PR-specific changes match the acceptance criteria.
- [ ] Existing dashboard features still work.
- [ ] No unrelated regressions were introduced.
- [ ] Screenshots or logs are attached to the PR review when useful.

## Troubleshooting

### Dashboard Cannot Reach the Backend

Check that the backend is running at:

```text
http://localhost:8000
```

If the backend is running on another host or port, update the frontend API base URL and restart the dashboard.

### CORS Errors in the Browser Console

If the browser reports CORS errors, confirm that the backend allows requests from the frontend origin, for example:

```text
http://localhost:3000
```

Restart the backend after changing CORS or configuration settings.

### Port 8000 Is Already in Use

Stop the process using port 8000, or start the backend on a different port. If you change the backend port, update the frontend API base URL before starting the dashboard.

### Port 3000 Is Already in Use

The React development server may choose another port automatically. Use the URL printed in the terminal. If needed, stop the process using port 3000 and restart the dashboard.

### `npm install` Fails

Confirm that Node.js and npm are installed and that the Node.js version matches the frontend requirements.

Check versions:

```bash
node --version
npm --version
```

If dependency installation still fails, remove local frontend dependencies and reinstall:

```bash
cd frontend
rm -rf node_modules
npm install
```

On Windows, remove `node_modules` using File Explorer or:

```powershell
Remove-Item -Recurse -Force node_modules
```

Then run:

```powershell
npm install
```

### Dashboard Shows No Data

Confirm that:

- The backend is running.
- The frontend API base URL points to the correct backend.
- The backend has valid configuration at `CONFIG_PATH=/config/config.yml` when using Docker Compose.
- The browser network tab does not show failed API requests.
- The backend terminal does not show request errors.

### Docker Compose Backend Fails to Start

Check the Docker Compose logs:

```bash
docker compose logs
```

Confirm that:

- Docker is running.
- Port 8000 is available.
- The `app` and `config` directories exist.
- `config/config.yml` is present and valid.

## Notes for Managers

- Run the backend and frontend in separate terminals.
- Keep the backend running while validating the dashboard.
- Use the browser developer console and network tab when investigating UI or API issues.
- Do not commit `node_modules`, local environment files, or generated build output.
- When in doubt, validate the dashboard with both a running backend and an unavailable backend to confirm loading, empty, and error behavior.
