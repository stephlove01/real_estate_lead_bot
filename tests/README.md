# Tests

Project-level and cross-cutting tests live here.

Backend unit/integration tests primarily live under `backend/tests/`.

## Planned Coverage Areas

- Backend API (health, auth, leads, conversations, messages, follow-ups)
- Database models, constraints, migrations
- AI extraction scenarios (BUY / RENT / LAND / missing info / handoff)
- n8n workflow success & failure paths
- Frontend interaction flows
- End-to-end customer → lead → notification journeys

See `docs/TESTING_SPEC.md` for the full testing strategy.
