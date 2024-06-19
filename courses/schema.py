import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required

from .models import Course, Enrollment


class EnrollmentType(DjangoObjectType):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrollment_date']


class CourseType(DjangoObjectType):
    course_enrollments = graphene.List(EnrollmentType)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

    def resolve_course_enrollments(self, info):
        return Enrollment.objects.filter(course=self)


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, course_id=graphene.ID(required=False))
    enrollments = graphene.List(EnrollmentType, course_id=graphene.ID(required=False))

    def resolve_courses(self, info, course_id=None):
        if course_id:
            return Course.objects.filter(id=course_id)
        return Course.objects.all()

    @login_required
    def resolve_enrollments(self, info, course_id=None):
        user = info.context.user
        if not course_id:
            return Enrollment.objects.filter(student=user)
        return Enrollment.objects.filter(student=user, course_id=course_id)


class CreateCourse(graphene.Mutation):
    class Arguments:
        course_name = graphene.String()
        description = graphene.String()

    course = graphene.Field(CourseType)

    @superuser_required
    def mutate(self, info, course_name, description):
        course = Course.objects.create(
            name=course_name, description=description)
        return CreateCourse(course=course)


class CreateEnrollment(graphene.Mutation):
    class Arguments:
        course_id = graphene.ID()

    enrollment = graphene.Field(EnrollmentType)

    @login_required
    def mutate(self, info, course_id):
        course = Course.objects.get(id=course_id)
        if not course:
            raise Exception('Course not found')
        enrollment = Enrollment.objects.create(
            student=info.context.user,
            course=course
        )
        return CreateEnrollment(enrollment=enrollment)


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    enroll_course = CreateEnrollment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
