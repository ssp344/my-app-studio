# Individual review deployment

The application reuses the existing FastAPI foundation and DigitalOcean Docker/Traefik setup. A separate Compose project, `is373-individual-review`, uses the existing external `hosting-web` network. The existing proxy, domains, QA, production, and calculator remain separately owned services.

- Portfolio: https://shiv-is373.xyz/portfolio
- Assistant: https://shiv-is373.xyz/rag
- Routes added to Traefik: `/portfolio`, `/portfolio/*`, `/rag`, `/api/review/*`, `/review-static/*` on the existing HTTPS hostname only.
- No host ports are published. The app is non-root, drops Linux capabilities, and has a 192 MB memory cap and 0.5 CPU cap.
- A new Docker volume stores account and corpus SQLite databases. No previous local accounts were copied.
- Runtime signing material is generated on the server and kept in `.env.review`, excluded from Git and Docker build context.

## Reproduce the scoped deployment

The actual isolated directory is `/home/deploy/apps/is373-individual-review`. The deploy account permits passwordless Docker but not passwordless creation of `/opt` directories, so no sudo permissions were changed. Transfer only `app/`, `studio_tools/`, `corpus/`, `Dockerfile.review`, `requirements-runtime.txt`, `.dockerignore`, and `compose.review.yaml` from the source revision. Generate `APP_SECRET` privately in `.env.review` (at least 32 random bytes; file mode 0600). Do not paste it into a report or command-line argument.

Run from that directory:

```sh
sudo docker compose -f compose.review.yaml config --quiet
sudo docker compose -f compose.review.yaml up -d --build
```

To stop only this deployment, use `sudo docker compose -f compose.review.yaml stop review`. Do not stop the shared proxy or other Compose projects. Do not remove the volume to roll back code. Existing services' before/after identities and live responses are recorded in `live-checks.json` / `deployment-checks.json` when verified.

The new review service is deployed directly from a checked source bundle. It is not attached to the older static-site automatic deployment workflow. The app repo's existing CI continues to test the bookstore and new HTTP tests.
