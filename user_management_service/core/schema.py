import graphene

from apps.accounts import schema


class RootQuery(schema.Query):
    pass


class RootMutation(schema.Mutation):
    pass


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
