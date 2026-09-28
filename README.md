# SovereignChat

Mode-adaptive operator chat for Garcar Enterprise. Local engine. Optional HTTP API. Live $47 checkout on the sell page.

## Live

- Repo: https://github.com/Garrettc123/sovereign-chat
- Chat: https://sovereign-chat.netlify.app/
- Offer: https://sovereign-chat.netlify.app/sell.html
- Checkout: https://buy.stripe.com/dRm8wPbb72pY2Mz8BR43S1D
- Storefront: https://garrettc123.github.io/

## Run locally

```bash
python3 tests/test_engine.py
python3 run.py
```

Python 3.10+. No third-party packages.

- Chat — http://127.0.0.1:8787/index.html
- Offer — http://127.0.0.1:8787/sell.html

Open `web/index.html` directly if you only need the client engine.

## Money path

- SKU: Contractor Lead Leak Audit — $47
- Leads land in `data/leads.jsonl` when `/api/lead` is used against the local server.

## API

`POST /api/chat` `{ "text": "...", "session": "optional" }`

`POST /api/reset` `{ "session": "optional" }`

`POST /api/lead` `{ "name", "email", "trade", "note" }`
