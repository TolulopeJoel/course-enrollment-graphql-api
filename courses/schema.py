import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Course, Enrollment


class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_at']


class EnrollmentType(DjangoObjectType):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)
    enrollments = graphene.List(EnrollmentType)

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()

    @login_required
    def resolve_enrollments(self, info, **kwargs):
        user = info.context.user
        return Enrollment.objects.filter(student=user)


class CreateEnrollment(graphene.Mutation):
    class Arguments:
        course_id = graphene.ID()

    enrollment = graphene.Field(EnrollmentType)

    # @login_required
    def mutate(self, info, course_id):
        course = Course.objects.get(id=course_id)
        if not course:
            raise Exception('Course not found')
        enrollment = Enrollment.objects.create(
            user=info.context.user,
            course=course
        )
        return CreateEnrollment(enrollment=enrollment, course=course)


class Mutation(graphene.ObjectType):
    create_enrollment = CreateEnrollment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
