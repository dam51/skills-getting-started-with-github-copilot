import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app, activities


@pytest.mark.asyncio
async def test_signup_nonexistent_activity_returns_404():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.post("/activities/Nonexistent/signup?email=foo@bar.com")
        assert resp.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_signup_returns_400():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Use an existing participant
        activity = next(iter(activities))
        existing = activities[activity]["participants"][0]
        resp = await client.post(f"/activities/{activity}/signup?email={existing}")
        assert resp.status_code == 400
