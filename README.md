# Online Cinema API

A modern web-based cinema platform for browsing, purchasing, and watching movies. Includes authentication, user roles, payments via Stripe, cart functionality, order management, and more.

---

## 1. Features

1.1. User registration, login (JWT-based), password reset, and account activation via email  
1.2. Movie catalog: browse, filter, search, rate, comment, like/dislike  
1.3. Add movies to favorites and cart  
1.4. Stripe payment integration  
1.5. Role-based permissions: User, Moderator, Admin  
1.6. Order system: place, cancel, pay   
1.7. Dockerized for development and production  
1.8. Celery + Redis for background jobs (e.g., deleting expired tokens, Telegram notifications)  
1.9. API documentation (Swagger / ReDoc / OpenAPI 3.0)  

---

## 2. Tech Stack

2.1. Python 3.11  
2.2. FastAPI  
2.3. SQLAlchemy 2.x (async)  
2.4. Alembic  
2.5. PostgreSQL  
2.6. Redis + Celery + Celery Beat  
2.7. Stripe API  
2.8. Docker & docker-compose  
2.9. pytest, httpx, coverage  

---

## 3. Quickstart (Docker)

### 3.1. Clone the repository

```bash
git clone https://github.com/your-username/online-cinema.git
cd online-cinema
```

### 3.2. Create and configure `.env`

```bash
cp .env.sample .env
# Edit the .env file to fill in all required variables.
```

### 3.3. Build and start all services

```bash
docker-compose up --build
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3.4. Apply database migrations

```bash
docker-compose exec web alembic upgrade head
```

### 3.5. Create a superuser

```bash
docker-compose exec web python scripts/create_superuser.py
```

---

## 4. Environment Variables

See `.env.sample` for all required variables. Must define:

- `DATABASE_URL`, `TEST_DATABASE_URL`  
- `REDIS_URL`  
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`  
- `STRIPE_API_KEY`  
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`

---

## 5. API Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI schema: `/openapi.json`

Interactive docs let you register, login, filter movies, add to cart, and make payments.

---

## 6. Endpoints Overview

| Resource   | Endpoint(s)                                     | Description                              |
|------------|--------------------------------------------------|------------------------------------------|
| Auth       | `/accounts/register`, `/login`, `/reset-password` | Registration, login, password reset      |
| Users      | `/accounts/me`, `/accounts/update-role`          | User profile, group management           |
| Movies     | `/movies/`, `/movies/{id}`                       | View, filter, rate, comment              |
| Favorites  | `/favorites/`                                    | Add/remove favorites                     |
| Cart       | `/cart/`, `/cart/clear/`                         | Add/remove/view cart                     |
| Orders     | `/orders/`, `/orders/{id}`                       | Create, view, cancel orders              |
| Payments   | `/payments/`, Stripe webhook                     | Stripe payments                          |


---

## 7. Running Tests

### 7.1. Locally

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=60
```

### 7.2. Inside Docker

```bash
docker-compose exec web pytest --cov
```

To generate HTML coverage report:

```bash
pytest --cov=src --cov-report=html
```

> ✅ Target coverage: **60%+**

---

## 8. User Roles & Permissions

- **Guest**: can view public movie catalog  
- **User**: all guest rights + cart, favorites, order, payments  
- **Moderator**: all user rights + manage movies via admin  
- **Admin**: full access to user groups, moderation, admin rights

---

## 9. Docker Compose Services

| Service        | Description                          |
|----------------|--------------------------------------|
| `web`          | FastAPI backend                      |
| `db`           | PostgreSQL                           |
| `redis`        | Celery broker                        |
| `celery`       | Celery worker                        |
| `celery-beat`  | Periodic tasks                       |

---


---

## 10. Security

- Set `DEBUG=False` in production  
- Use strong secrets & tokens  
- Validate all input and JWT scopes  
- Restrict admin panel access
