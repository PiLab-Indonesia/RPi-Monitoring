import { build } from "esbuild";
const apiBase = process.env.REACT_APP_API_BASE || "http://localhost:8000";
await build({
  entryPoints: ["src/index.jsx"],
  outfile: "public/app.js",
  bundle: true,
  minify: true,
  target: ["es2020"],
  define: { "process.env.REACT_APP_API_BASE": JSON.stringify(apiBase) },
  logLevel: "info",
});
console.log(`Built dashboard with API: ${apiBase}`);
