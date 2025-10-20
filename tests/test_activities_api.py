import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app, activities


@pytest.mark.asyncio
async def test_get_activities_contains_chess_club():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/activities")
        assert resp.status_code == 200
        data = resp.json()
        assert "Chess Club" in data


@pytest.mark.asyncio
async def test_signup_and_remove_participant():
    test_activity = "Chess Club"
    test_email = "test_student@mergington.edu"

    # Ensure test_email not present initially
    if test_email in activities[test_activity]["participants"]:
        activities[test_activity]["participants"].remove(test_email)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Sign up
        signup_resp = await client.post(f"/activities/{test_activity}/signup?email={test_email}")
        assert signup_resp.status_code == 200
        assert test_email in activities[test_activity]["participants"]

        # Remove
        delete_resp = await client.delete(f"/activities/{test_activity}/participants?email={test_email}")
        assert delete_resp.status_code == 200
        assert test_email not in activities[test_activity]["participants"]
