import graphene

import accounts.schema
import restaurant.schema


class Query(restaurant.schema.Query, accounts.schema.Query):
    pass


class Mutation(restaurant.schema.Mutation, accounts.schema.Mutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
