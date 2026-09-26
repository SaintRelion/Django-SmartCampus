# Smart Campus Backend

Django backend for **Smart Campus**, providing the authentication and
security services used by the React frontend. The backend handles user
accounts, email OTP, device/passkey workflows, and PostgreSQL
persistence.

## Key features

-   **WebAuthn / passkey security** --- device registration and
    authentication endpoints for the frontend's passkey flow.
-   **Email OTP verification** --- supports account verification and
    enrollment before device registration.
-   **Authentication and user accounts** --- registration and
    authentication using the Smart Campus user model.
-   **Employee ID login** --- custom authentication supports
    employee-based accounts.
-   **PostgreSQL persistence** --- application data is stored in
    PostgreSQL.
-   **Dockerized full stack** --- Compose can run the React frontend,
    Django backend, and PostgreSQL database together.

## Stack

-   Django + Django REST Framework
-   PostgreSQL
-   WebAuthn / passkeys and email OTP
-   Uvicorn / ASGI
-   Astral `uv` for Python dependency and environment management
-   Docker / Docker Compose
-   Private `django-saintrelion-libs` dependency

## Private dependencies

This project depends on private SaintRelion packages. Required access
tokens are **not included in the repository**.

To build the complete application, request the required credentials from
the developer:

-   `SR_DJANGO_LEGACY_TOKEN` --- private Django dependency
-   `SR_REACT_GITHUB_TOKEN` --- private frontend packages

## Run with Docker

The simplest way to run the project is with Docker Compose. Keep the
frontend and backend repositories beside each other:

``` text
SmartCampus/
├── CL-Smart-Campus-System/
│   └── .env
└── Django-SmartCampus/
    ├── .env
    ├── Dockerfile
    └── docker-compose.yml
```

Copy `.env.example` to `.env` and provide the required application
values. Then expose the private package credentials in your shell.

PowerShell:

``` powershell
$env:SR_DJANGO_LEGACY_TOKEN="YOUR_TOKEN"
$env:SR_REACT_GITHUB_TOKEN="YOUR_TOKEN"

docker compose up -d --build
```

Compose starts:

``` text
Frontend     http://localhost:8080
Backend      http://localhost:8000
PostgreSQL   localhost:5435
```

The backend waits for PostgreSQL, applies Django migrations, and then
starts the ASGI application with Uvicorn.

Inside Docker, Compose overrides environment values that differ from
local development, including the database host and WebAuthn frontend
origin.

Useful commands:

``` powershell
docker compose ps
docker compose logs -f --tail=100 backend
docker compose logs -f --tail=100 frontend
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to
delete the PostgreSQL volume.

### Dependency management

Python dependencies are managed with **Astral uv** through
`pyproject.toml` and `uv.lock`. The Docker image also uses
`uv sync --frozen` so the container installs the locked dependency graph
rather than maintaining a separate `requirements.txt` installation path.

The private Django dependency is fetched during the Docker build using a
BuildKit secret; the access token is not stored in `pyproject.toml` or
committed to the repository.

## First administrator

A fresh/restored system can create its first administrator through the
frontend's temporary:

``` text
/setup-admin
```

After creating the account, sign in through `/login` and complete the
existing email OTP and WebAuthn/passkey setup.

The `/setup-admin` route is intended only for initial setup and should
be removed or disabled after the first administrator is created.

## WebAuthn configuration

For local frontend development:

``` env
RP_ID=localhost
ORIGIN=http://localhost:5173
```

For the Docker frontend:

``` env
RP_ID=localhost
ORIGIN=http://localhost:8080
```

`RP_ID` is the relying-party domain only; it does not include a scheme
or port.

## Local setup without Docker

This section is only needed if you want to run the Django backend
directly on your machine.

### 1. Install uv

On Windows:

``` powershell
winget install --id=astral-sh.uv -e
```

Verify:

``` powershell
uv --version
```

The repository uses `pyproject.toml` and `uv.lock`, so restore the
environment with:

``` powershell
uv sync
```

### 2. Configure PostgreSQL

Create a PostgreSQL database and configure `.env` for your local
instance:

``` env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smartcampus
DB_USER=smartcampus
DB_PASSWORD=

SECRET_KEY=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

RP_ID=localhost
RP_NAME=Smart Campus
ORIGIN=http://localhost:5173
```

The private Django package still requires access to the SaintRelion
repository when dependencies need to be installed.

### 3. Run Django

The application source lives under `src/`.

Apply migrations:

``` powershell
uv run python src/manage.py migrate
```

Start the ASGI server:

``` powershell
uv run uvicorn --app-dir src core.asgi:application --reload --host 127.0.0.1 --port 8000
```

The frontend can then use:

``` text
http://localhost:8000
```

## Before production

The current configuration is intended primarily for
development/restoration. Before public deployment, review Django `DEBUG`
and `ALLOWED_HOSTS`, use production secrets and HTTPS, configure the
production WebAuthn domain/origin, and remove or disable the initial
`/setup-admin` flow.

## Author

**June Aurelius Jacinto**\
Full-Stack Software Developer

GitHub: https://github.com/SaintRelion
