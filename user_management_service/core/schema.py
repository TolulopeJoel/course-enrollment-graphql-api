import graphene

from apps.accounts import schema


class RootQuery(schema.Query):
    pass


schema = graphene.Schema(query=RootQuery)
