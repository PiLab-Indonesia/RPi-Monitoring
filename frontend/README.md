# React device dashboard

Minimal manager-facing frontend for the RPi-Monitoring `GET /devices` endpoint.

## Develop and build

From `frontend/` (Node 22 or newer):

```sh
npm install
npm test
npm run build
python -m http.server 8080 --directory public
```

Open http://localhost:8080. API defaults to http://localhost:8000.
Build-time override:

```sh
REACT_APP_API_BASE=https://monitor.example.com npm run build
```

On Windows PowerShell: `$env:REACT_APP_API_BASE="http://localhost:8000"; npm run build`.

**Browser CORS:** A separate frontend origin such as localhost:8080 requires
the FastAPI server to allow that origin or a same-origin reverse proxy.
This frontend does not disable browser security or send credentials.

The application is read-only. It handles initial loading, empty devices,
HTTP errors, manual refresh, responsive layout and online/offline badges.
`npm test` runs 7 isolated API tests with no hardware or backend.
Generated `public/app.js` and `public/app.css` are gitignored.
