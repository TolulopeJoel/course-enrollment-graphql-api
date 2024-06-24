import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from .database import db_session
from .models import Course as CourseModel
from .utils import check_user_exists, validate_token


class CourseType(SQLAlchemyObjectType):
    class Meta:
        model = CourseModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    all_courses = graphene.List(CourseType)
    course = graphene.Field(CourseType, id=graphene.Int())

    def resolve_all_courses(self, info):
        return CourseModel.query.all()

    def resolve_course(self, info, id):
        return CourseModel.query.get(id)


class CreateCourse(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()

    course = graphene.Field(CourseType)

    def mutate(self, info, title, description):
        token = info.context.headers.get('Authorization')

        if not token or not validate_token(token):
            raise Exception('Invalid or missing token')

        user = check_user_exists(token)
        if not user:
            raise Exception('User not found')

        course = CourseModel(
            title=title,
            description=description,
            author_id=user["id"]
        )
        db_session.add(course)
        db_session.commit()
        return CreateCourse(course=course)


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
