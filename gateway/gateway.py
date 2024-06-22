from typing import List, Optional

import strawberry
from aiohttp import ClientSession
from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.scalars import JSON as json_type

app = FastAPI()

USER_MANAGEMENT_URL = "http://127.0.0.1:8000/graphql/"

COURSE_MANAGEMENT_URL = "http://127.0.0.1:5000/graphql"


async def fetch_from_service(url: str, query: str, variables: dict = None, headers: dict = None):
    """
    Fetches data from a microservice using a POST request with the
    provided URL, query, and variables.
    """
    async with ClientSession() as session:
        async with session.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Error fetching data from {url}"
                )

            result = await response.json()
            if "errors" in result:
                raise HTTPException(status_code=400, detail=result["errors"])
            return result["data"]


@strawberry.type
class User:
    id: str
    email: str


@strawberry.type
class Course:
    id: int
    title: str
    description: str
    authorId: int


@strawberry.type
class AuthResponse:
    token: str
    refreshToken: str
    payload: json_type
    refreshExpiresIn: int


@strawberry.type
class CreateUserResponse:
    user: User


@strawberry.type
class CreateCourseResponse:
    course: Course


@strawberry.type
class Query:
    """
    Defines GraphQL queries that resolve to different microservices.
    """
    @strawberry.field
    async def users(self, info) -> List[User]:
        query = """
        query {
            users {
                id
                email
            }
        }
        """
        response = await fetch_from_service(USER_MANAGEMENT_URL, query)
        return [User(**user) for user in response["users"]]

    @strawberry.field
    async def whoami(self, info) -> Optional[User]:
        query = """
        query {
            whoami{
                id
                email
            }
        }
        """
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, {})
        return User(**response["whoami"]) if response.get("whoami") else None

    @strawberry.field
    async def all_courses(self, info) -> List[Course]:
        query = """
        query {
            allCourses{
                id
                title
                description
                authorId
            }
        }
        """
        response = await fetch_from_service(COURSE_MANAGEMENT_URL, query)
        return [Course(**course) for course in response["allCourses"]]

    @strawberry.field
    async def course(self, info, id: str) -> Optional[Course]:
        query = """
        query($id: Int!) {
            course(id: $id) {
                id
                title
                description
                authorId
            }
        }
        """
        response = await fetch_from_service(COURSE_MANAGEMENT_URL, query, {"id": id})
        return Course(**response["course"])


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def token_auth(self, info, username: str, password: str) -> AuthResponse:
        query = """
        mutation($username: String!, $password: String!) {
            tokenAuth(username: $username, password: $password) {
                token
                payload
                refreshToken
                refreshExpiresIn
            }
        }
        """
        variables = {"username": username, "password": password}
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, variables)
        return AuthResponse(**response["tokenAuth"])


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4001)
