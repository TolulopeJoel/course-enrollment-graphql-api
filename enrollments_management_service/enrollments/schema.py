import graphene
from graphene_django import DjangoObjectType
from .models import Enrollment
from .utilities import verify_token, get_user_from_token
import requests

API_GATEWAY_URL = "http://127.0.0.1:4001/graphql"


class EnrollmentType(DjangoObjectType):
    class Meta:
        model = Enrollment


class Query(graphene.ObjectType):
    enrollments = graphene.List(EnrollmentType)

    def resolve_enrollments(self, info):
        return Enrollment.objects.all()


class CreateEnrollment(graphene.Mutation):
    class Arguments:
        course_id = graphene.Int()

    enrollment = graphene.Field(EnrollmentType)

    def mutate(self, info, course_id):
        token = info.context.headers.get('Authorization')
        if not token or not verify_token(token):
            raise Exception('Invalid or missing token')
        
        print("I PASSEd")

        user = get_user_from_token(token)
        print("user: ", user)
        if not user:
            raise Exception('User not found')

        # Fetch course details from course management service
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
        variables = {"id": course_id}
        response = requests.post(
            API_GATEWAY_URL,
            json={'query': query, 'variables': variables},
            headers={'Authorization': token}
        )
        print(response.json())
        course_data = response.json().get('data', {}).get('course')
        if not course_data:
            raise Exception('Course not found')

        enrollment = Enrollment(user_id=user['id'], course_id=course_id)
        enrollment.save()
        return CreateEnrollment(enrollment=enrollment)


class Mutation(graphene.ObjectType):
    pass
    create_enrollment = CreateEnrollment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
