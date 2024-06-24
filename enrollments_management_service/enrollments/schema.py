import graphene
from graphene_django import DjangoObjectType

from .models import Enrollment


class EnrollmentType(DjangoObjectType):
    class Meta:
        model = Enrollment


class Query(graphene.ObjectType):
    enrollments = graphene.List(EnrollmentType)
    enrollment = graphene.Field(EnrollmentType, id=graphene.Int())

    def resolve_enrollments(self, info):
        return Enrollment.objects.all()

    def resolve_enrollment(self, info, id):
        return Enrollment.objects.get(pk=id)


class CreateEnrollment(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        course_id = graphene.Int(required=True)

    enrollment = graphene.Field(EnrollmentType)

    def mutate(self, info, user_id, course_id):
        enrollment = Enrollment.objects.create(
            user_id=user_id,
            course_id=course_id
        )
        return CreateEnrollment(enrollment=enrollment)


class Mutation(graphene.ObjectType):
    create_enrollment = CreateEnrollment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
