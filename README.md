# Secure Pipeline: a DevSecOps CI Demo

A small Flask API wrapped in a **security-first CI pipeline**. The app is intentionally tiny; the point is the pipeline: every push is linted, tested, scanned for code flaws, leaked secrets, vulnerable dependencies and image CVEs, and an SBOM is produced.

## Pipeline

```
push / PR
   |
   +--> lint + unit tests (flake8, pytest)
   +--> SAST (Bandit)
   +--> secret scan (Gitleaks)
   +--> dependency audit (pip-audit)
            |
            v  (all must pass)
   Dockerfile lint (Hadolint)
   -> build image
   -> Trivy scan (fails on HIGH/CRITICAL)
   -> SBOM (CycloneDX) uploaded as artifact
```

## Security choices in the image

- Multi-stage build, so build tooling stays out of the final image
- Slim base image, pinned dependency versions
- Runs as a **non-root user** (UID 10001)
- Served by gunicorn, not the Flask dev server
- `HEALTHCHECK` built in
- `.dockerignore` keeps tests, git history and `.env` out of the image

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
flake8 app tests --max-line-length=100
bandit -r app -ll
```

## Run with Docker

```bash
docker build -t secure-pipeline .
docker run -p 8080:8080 secure-pipeline
curl http://localhost:8080/health
```

## Seeing the gates work

Push to GitHub and watch the **Actions** tab. To see a gate fail, try on a branch:

- Pin an old vulnerable package version: pip-audit / Trivy fails
- Use `eval()` or `subprocess` with `shell=True`: Bandit fails
