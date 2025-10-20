import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app


@pytest.mark.asyncio
async def test_root_redirects_to_static_index():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/", follow_redirects=False)
        # FastAPI RedirectResponse uses 307 by default
        assert resp.status_code in (301, 302, 307, 308)
        # Location header should point to /static/index.html
        assert resp.headers.get("location") == "/static/index.html"


@pytest.mark.asyncio
async def test_static_index_returns_html():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/static/index.html")
        assert resp.status_code == 200
        assert "Mergington High School" in resp.text
