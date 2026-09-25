# Smart Campus Backend

Django backend for Smart Campus. It provides authentication/security
endpoints used by the frontend, including account registration, email
OTP, device checks, and WebAuthn. PostgreSQL is used as the database.

This repository also contains `docker-compose.yml` for running the
complete Smart Campus system.

## Key features

- **WebAuthn / passkey security** — backend endpoints for device registration and authentication used by the frontend's biometric/passkey flow.
- **Email OTP verification** — supports the enrollment and account-security workflow before WebAuthn registration.
- **Authentication and user accounts** — registration and authentication backed by the custom Smart Campus user model.
- **Employee ID login support** — custom authentication supports the employee-based account flow used by the client.
- **PostgreSQL persistence** — application data is backed by PostgreSQL and integrated into the full Docker stack.

## Stack

Python 3.12, Django 6, Django REST Framework, PostgreSQL, Simple JWT,
WebAuthn, Uvicorn, and the private `django-saintrelion-libs` package.

## Access to private dependencies

This project depends on private SaintRelion packages. The required access keys/tokens are **not included in this repository**.

If you need access to build or run the project, please contact the developer to request the required keys.

## Setup

Copy `.env.example` to `.env` and configure:

``` env
SECRET_KEY=

DB_NAME=smartcampus
DB_USER=smartcampus
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

RP_ID=localhost
RP_NAME=Smart Campus
ORIGIN=http://localhost:5173
```

For normal local development, `DB_HOST=localhost` and `ORIGIN` should
match the frontend Vite URL.

Install the Python dependencies and run the backend using the project's
normal Django/ASGI workflow:

``` bash
pip install -r requirements.txt
```

The private Django SaintRelion dependency requires
`SR_DJANGO_LEGACY_TOKEN` while installing.

## Full application with Docker

Keep both repositories beside each other:

``` text
SmartCampus/
├── CL-Smart-Campus-System/
│   └── .env
└── Django-SmartCampus/
    ├── .env
    └── docker-compose.yml
```

Before building, provide the two private package tokens in your shell:

``` text
SR_DJANGO_LEGACY_TOKEN
SR_REACT_GITHUB_TOKEN
```

Example PowerShell:

``` powershell
$env:SR_DJANGO_LEGACY_TOKEN="YOUR_TOKEN"
$env:SR_REACT_GITHUB_TOKEN="YOUR_TOKEN"
```

Then, from `Django-SmartCampus`:

``` bash
docker compose up -d --build
```

The stack runs:

``` text
Frontend   http://localhost:8080
Backend    http://localhost:8000
Database   PostgreSQL (`db` inside Compose)
```

Compose overrides the local-only values needed inside Docker:

``` yaml
environment:
  DB_HOST: db
  ORIGIN: http://localhost:8080
```

This lets the same backend `.env` remain suitable for local development
(`localhost:5173`) while Docker uses the frontend served on port `8080`.

Check the containers with:

``` bash
docker compose ps
```

Stop them with:

``` bash
docker compose down
```

Do not add `-v` unless you intentionally want to delete the PostgreSQL
volume.

## First administrator

A fresh/restored system can create its first administrator through the
frontend's temporary:

``` text
/setup-admin
```

After creation, sign in through `/login` and complete the existing email
OTP and WebAuthn/fingerprint setup.

Remove the frontend `/setup-admin` page and route after the first
administrator is created.

## WebAuthn

For local Vite development:

``` env
RP_ID=localhost
ORIGIN=http://localhost:5173
```

For Docker, Compose overrides the origin to:

``` text
http://localhost:8080
```

`RP_ID` remains `localhost`; it does not include a scheme or port.

## Before production

The current source is configured primarily for development/restoration.
Before a public deployment, review Django `DEBUG`/`ALLOWED_HOSTS`, use
production secrets and HTTPS, configure the production WebAuthn
domain/origin, remove `/setup-admin`, and do not use permissive
Firestore rules.

## Author

**June Aurelius Jacinto**  
Full-Stack Software Developer

GitHub: https://github.com/SaintRelion

