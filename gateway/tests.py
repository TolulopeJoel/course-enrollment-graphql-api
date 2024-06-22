import pytest
from aiohttp import ClientSession
from gateway import app, COURSE_MANAGEMENT_URL

@pytest.mark.asyncio
async def test_all_courses():
    async with ClientSession() as session:
        query = """
        query {
            allCourses {
                id
                title
                description
                authorId
            }
        }
        """
        async with session.post(
            COURSE_MANAGEMENT_URL,
            json={"query": query}
        ) as response:
            assert response.status == 200
            data = await response.json()
            assert "data" in data
            assert "allCourses" in data["data"]
            courses = data["data"]["allCourses"]
            assert isinstance(courses, list)
            if courses:
                assert all(
                    isinstance(course, dict) and
                    "id" in course and
                    "title" in course and
                    "description" in course and
                    "authorId" in course
                    for course in courses
                )

@pytest.mark.asyncio
async def test_gateway_all_courses():
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.post(
        "/graphql",
        json={
            "query": """
            query {
                allCourses {
                    id
                    title
                    description
                    authorId
                }
            }
            """
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "allCourses" in data["data"]
    courses = data["data"]["allCourses"]
    assert isinstance(courses, list)
    if courses:
        assert all(
            isinstance(course, dict) and
            "id" in course and
            "title" in course and
            "description" in course and
            "authorId" in course
            for course in courses
        )