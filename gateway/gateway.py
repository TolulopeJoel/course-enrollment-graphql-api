import datetime
from typing import List, Optional

import strawberry
from aiohttp import ClientSession
from fastapi import FastAPI, HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.scalars import JSON as json_type

app = FastAPI()

USER_MANAGEMENT_URL = "http://user-management:8000/graphql/"

COURSE_MANAGEMENT_URL = "http://course-management:3000/graphql"

ENROLLMENTS_MANAGEMENT_URL = "http://enrollments-management:8001/graphql/"


async def fetch_from_service(url: str, query: str, variables: dict = None, headers: dict = None):
    """
    Fetches data from a microservice using a POST request with the
    provided URL, query, variables, and headers.
    """
    async with ClientSession() as session:
        request_headers = {
            "Content-Type": "application/json",
            **(headers or {})
        }

        async with session.post(
            url,
            json={"query": query, "variables": variables},
            headers=request_headers
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
@strawberry.type
class Course:
    id: str
    title: str
    description: str
    authorId: int

@strawberry.type
class Enrollment:
    id: int
    courseId: int
    userId: int
    enrollmentDate: datetime.datetime


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
class CreateEnrollmentResponse:
    enrollment: Enrollment


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
        headers = {
            "Authorization": info.context["request"].headers.get("Authorization")}
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, headers=headers)
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
        headers = {
            "Authorization": info.context["request"].headers.get("Authorization")}
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, headers=headers)
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
    async def enrollments(self, info) -> List[Enrollment]:
        query = """
        query {
            enrollments{
                id
                courseId
                userId
                enrollmentDate
            }
        }
        """
        response = await fetch_from_service(ENROLLMENTS_MANAGEMENT_URL, query)
        return [Enrollment(**enrollment) for enrollment in response["enrollments"]]

    @strawberry.field
    async def course(self, info, id: str) -> Optional[Course]:
        query = """
        query($id: String!) {
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

    @strawberry.mutation
    async def create_user(self, info, email: str, password: str) -> CreateUserResponse:
        query = """
        mutation($email: String!, $password: String!) {
            createUser(email: $email, password: $password) {
                user {
                    id
                    email
                }
            }
        }
        """
        variables = {"email": email, "password": password}
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, variables)
        return CreateUserResponse(user=User(**response["createUser"]["user"]))

    @strawberry.mutation
    async def create_course(self, info, title: str, description: str) -> CreateCourseResponse:
        query = """
        mutation($title: String!, $description: String!) {
            createCourse(title: $title, description: $description) {
                course {
                    id
                    title
                    description
                    authorId
                }
            }
        }
        """
        variables = {
            "title": title,
            "description": description,
        }
        headers = {
            "Authorization": info.context["request"].headers.get("Authorization")}
        response = await fetch_from_service(COURSE_MANAGEMENT_URL, query, variables, headers)
        return CreateCourseResponse(course=Course(**response["createCourse"]["course"]))

    @strawberry.mutation
    async def create_enrollment(self, info, courseId: int) -> CreateEnrollmentResponse:
        query = """
        mutation($courseId: Int!) {
            createEnrollment(courseId: $courseId) {
                enrollment {
                    id
                    userId
                    courseId
                    enrollmentDate
                }
            }
        }
        """
        variables = {
            "courseId": courseId,
        }
        headers = {
            "Authorization": info.context["request"].headers.get("Authorization")}
        response = await fetch_from_service(ENROLLMENTS_MANAGEMENT_URL, query, variables, headers)
        return CreateEnrollmentResponse(enrollment=Enrollment(**response["createEnrollment"]["enrollment"]))

    @strawberry.mutation
    async def refresh_token(self, info, refresh_token: str) -> AuthResponse:
        query = """
        mutation($refreshToken: String!) {
            refreshToken(refreshToken: $refreshToken) {
                token
                payload
                refreshToken
                refreshExpiresIn
            }
        }
        """
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, {"refreshToken": refresh_token})
        return AuthResponse(**response["refreshToken"])

    @strawberry.mutation
    async def verify_token(self, info, token: str) -> json_type:
        query = """
        mutation($token: String!) {
            verifyToken(token: $token) {
                payload
            }
        }
        """
        response = await fetch_from_service(USER_MANAGEMENT_URL, query, {"token": token})
        return response["verifyToken"]


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4001)
