# Environment configuration

The backend reads configuration from `app.config.settings` using Pydantic
`BaseSettings`. All variables are optional locally; the defaults are declared
in `app/config.py`. Python environment variables take precedence over values
in an optional repository-root `.env` file.

## Run locally

1. Install dependencies: `python -m pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` and change values for your machine.
3. Launch from the repository root: `python -m uvicorn app.main:app --reload`.
4. Open `http://127.0.0.1:8000/docs` for the generated API schema.

**Never commit real `.env` credentials.** For deployments exposed beyond a
trusted development machine, replace the example `SECRET_KEY` with a strong,
random secret and configure any authentication layer before sharing endpoints.

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_NAME` | FastAPI application title | `RPi-NMS` |
| `ENV` | Deployment environment label | `development` |
| `DB_PATH` | SQLite database file used by API, discovery and alerts | `data/rpi_nms.db` |
| `DEFAULT_NETWORK` | Configured discovery network | `192.168.1.0/24` |
| `SCAN_INTERVAL_MINUTES` | Discovery scheduling interval | `5` |
| `TELEGRAM_TOKEN` / `TELEGRAM_CHAT_ID` | Alert destination (optional) | Unset |
| `SECRET_KEY` | Auth token signing secret (must be changed for production) | Development placeholder |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration in minutes | `60` |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM` | Optional mail notifications | Unset / port `587` |
| `WEBHOOK_URLS` | Optional comma-separated webhook list | Unset |

In Python, import `from app.config import settings`. Use explicit values only
when a component intentionally overrides the deployment configuration; otherwise
reuse `settings.db_path` and notification settings.

## Compatibility

Pydantic 1.10 and Pydantic 2.x expose the established BaseSettings behavior
through the `pydantic.v1` namespace. The code falls back to the direct
Pydantic 1.x import where necessary. The `python-dotenv` dependency is required
to parse an actual `.env` file. The settings model does not require a real
Raspberry Pi or network connection to test.
