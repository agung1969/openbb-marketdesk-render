# OpenBB MarketDesk API

This repository packages OpenBB ODP 4.7.2 as a production-ready Docker service.
It uses the stable `openbb-yfinance` provider, so the core market feed does not
require a vendor API key.

## Local start

```powershell
docker build -t openbb-marketdesk-api .
docker run --rm -p 8000:8000 --env-file .env.example openbb-marketdesk-api
```

The service will be available at:

- Health: `http://127.0.0.1:8000/health`
- Swagger: `http://127.0.0.1:8000/docs`
- Historical prices:
  `http://127.0.0.1:8000/api/v1/equity/price/historical?provider=yfinance&symbol=AAPL`

## Production deployment

Deploy `Dockerfile` to any HTTPS-capable container host. The included
`render.yaml` creates a free Render web service in Singapore. Configure:

```text
PORT=8000
CORS_ORIGINS=https://openbb-marketdesk-lab.stomper-bdg.chatgpt.site
OPENBB_API_AUTH=True
OPENBB_API_USERNAME=<generated username>
OPENBB_API_PASSWORD=<long random password>
OPENBB_AUTO_BUILD=False
OPENBB_DEBUG_MODE=False
OPENBB_DEV_MODE=False
```

The host must expose port `$PORT`, retain `/home/openbb/.openbb_platform` when
provider credentials are added, and route `/health` as its health check.

After deployment, configure the frontend's Sites environment:

```text
OPENBB_API_URL=https://your-openbb-api.example.com
OPENBB_PROVIDER=yfinance
OPENBB_API_USERNAME=<same username>
OPENBB_API_PASSWORD=<same password>
```

Do not commit `.env`, provider API keys, usernames, or passwords.
