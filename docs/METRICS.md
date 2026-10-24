# Prometheus device metrics

The FastAPI backend exposes `GET /metrics` in the Prometheus text format.
Each scrape queries the configured device database afresh; metrics are not
incremented for incoming HTTP requests, and there is no separate collector
process to run.

| Metric | Meaning |
| --- | --- |
| `rpi_devices_total` | Total monitored devices |
| `rpi_devices_alive` | Devices with `alive != 0` |
| `rpi_devices_down` | Devices marked unreachable (`total - alive`) |

Install the dependencies with `python -m pip install -r requirements.txt`,
start the API with `python -m uvicorn app.main:app`, then check:

    curl http://localhost:8000/metrics

Prometheus scrape configuration (when Prometheus can reach the API):

    scrape_configs:
      - job_name: "rpi-monitoring"
        static_configs:
          - targets: ["localhost:8000"]

Metrics currently expose aggregate device counts only; they contain no IP
addresses, credentials or other per-device identifying labels. The endpoint
is unauthenticated for scraping, so place the app behind an appropriate
network boundary when deployed outside a trusted local network.
