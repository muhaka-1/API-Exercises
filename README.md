# NovaStore API

Simple Docker-based project for learning how to use and extend a REST API.

A RESTful API built with **Python** and **Flask**, containerised with **Docker Compose**. This project was built as a hands-on exercise to learn how clients and APIs communicate, how APIs protect backend systems, and how HTTP status codes describe the result of a request.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Status Codes](#status-codes)
- [Running the Client](#running-the-client)
- [Exercise Overview](#exercise-overview)
- [Example Requests](#example-requests)

---

## Project Structure

```
API-Exercises/
├── docker-compose.yml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── client/
    ├── Dockerfile
    ├── requirements.txt
    └── client.py
```

---

## Tech Stack

| Layer     | Technology          |
|-----------|---------------------|
| Language  | Python 3.12         |
| Framework | Flask 3.0           |
| Client    | Requests            |
| Container | Docker + Compose    |

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### 1. Clone the repository

```bash
git clone https://github.com/muhaka-1/API-Exercises.git
cd API-Exercises
```

### 2. Run API Server

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

### 3. Run Client Specifically

`client` is a one-off helper container and is not started by default. Run it on demand:

```bash
docker compose run --rm client
```

Expected output is a list of products from the API.

---

## API Endpoints

| Method   | Endpoint            | Description                        | Status Codes     |
|----------|---------------------|------------------------------------|------------------|
| `GET`    | `/products`         | List all products                  | 200              |
| `GET`    | `/products/{id}`    | Get a single product by ID         | 200, 404         |
| `POST`   | `/products`         | Create a new product               | 201, 400         |
| `PUT`    | `/products/{id}`    | Update an existing product         | 200, 400, 404    |
| `DELETE` | `/products/{id}`    | Delete a product                   | 204, 404         |
| `GET`    | `/health`           | Health check                       | 200              |
| `GET`    | `/crash`            | Simulate a server error            | 500              |

---

## Status Codes

| Code  | Name                  | Meaning                                      | Whose fault?       |
|-------|-----------------------|----------------------------------------------|--------------------|
| `200` | OK                    | Request succeeded, data returned             | —                  |
| `201` | Created               | New resource was successfully created        | —                  |
| `204` | No Content            | Success, nothing to return (e.g. DELETE)     | —                  |
| `400` | Bad Request           | Client sent invalid or missing data          | Client / user      |
| `404` | Not Found             | The requested resource does not exist        | Client / user      |
| `500` | Internal Server Error | Unexpected failure on the server             | Developer          |

---

## Running the Client

The client (`client/client.py`) demonstrates every exercise by calling the API and printing results. It automatically waits for the API to be ready before making requests.

```bash
docker compose run --rm client
```

To rebuild the client image after editing `client.py`:

```bash
docker compose build client
docker compose run --rm client
```

---

## Exercise Overview

### Morning – Consuming an API

| Task | Description |
|------|-------------|
| 1 | Start the stack with `docker compose up --build` |
| 2 | Open `GET /products` in the browser and observe JSON vs HTML |
| 3 | Run the client and print the raw JSON response |
| 4 | Print the HTTP status code and understand what it means |
| 5 | Extract `id`, `name`, and `price` from the JSON response |
| 6 | Add the `category` field to the API response |
| 7 | Add more products and observe the client handles them automatically |
| 8 ⭐ | Return even more products in the list |
| 9 ⭐ | Verify that `stock` is printed in the client |
| 10 ⭐ | Add a `GET /health` endpoint |

### Afternoon – Building a Robust API

| Task | Description |
|------|-------------|
| 1 | Implement `GET /products/{id}` to fetch a single product |
| 2 | Return `404 Not Found` when a product does not exist |
| 3 | Implement `POST /products` to create new products |
| 4 | Return `400 Bad Request` for missing or invalid input |
| 5 | Implement `GET /crash` to simulate a `500 Internal Server Error` |
| 6 ⭐ | Verify that products created via POST appear in `GET /products` |
| 7 ⭐ | Implement `PUT /products/{id}` to update a product |
| 8 ⭐ | Implement `DELETE /products/{id}` to delete a product |
| 9 ⭐ | Return `201 Created` when a product is successfully created |
| 10 ⭐ | Return `204 No Content` when a product is deleted |

> ⭐ = Extra task

---

## Example Requests

### Get all products

```bash
curl http://localhost:5001/products
```

### Get a single product

```bash
curl http://localhost:5001/products/1
```

### Create a product

```bash
curl -X POST http://localhost:5001/products \
     -H "Content-Type: application/json" \
     -d '{"name": "Bluetooth Speaker", "price": 599, "category": "Audio", "stock": 12}'
```

### Update a product

```bash
curl -X PUT http://localhost:5001/products/1 \
     -H "Content-Type: application/json" \
     -d '{"price": 11499}'
```

### Delete a product

```bash
curl -X DELETE http://localhost:5001/products/1
```

### Trigger a 400 Bad Request

```bash
# Missing name
curl -X POST http://localhost:5001/products \
     -H "Content-Type: application/json" \
     -d '{"price": 99}'

# Negative price
curl -X POST http://localhost:5001/products \
     -H "Content-Type: application/json" \
     -d '{"name": "Widget", "price": -50}'
```

### Simulate a 500 error

```bash
curl http://localhost:5001/crash
```

---

## Key Takeaways

- **4xx errors** are the client's fault — bad data, wrong ID, wrong method.
- **5xx errors** are the developer's fault — the server failed unexpectedly.
- APIs act as a **gatekeeper**: validating input before it reaches the database prevents data corruption.
- **Status codes** let clients make decisions without parsing the response body.
- **JSON** is additive — adding new fields to an API response doesn't break existing clients.

---

## License

This project is for educational purposes.
