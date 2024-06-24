import graphene

from enrollments.schema import schema as enrollments_schema


class Query(enrollments_schema.Query, graphene.ObjectType):
    pass


class Mutation(enrollments_schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
