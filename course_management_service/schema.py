import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models import Course as CourseModel


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


