# Jensen API Exercises

Simple Docker-based project for learning how to use and extend a REST API.

## Run API Server

Start the long-running backend services:

```bash
docker compose up --build
```

What runs:
- `api` (Flask)

API endpoint:
- `http://localhost:5001/products`

Stop services:

```bash
docker compose down
```

## Run Client Specifically

`client` is a one-off helper container and is not started by default.

Run it on demand:

```bash
docker compose run --rm client
```

Expected output is a list of products from the API.
