import graphene

import accounts.schema
import restaurant.schema
import courses.schema


class Query(
    restaurant.schema.Query,
    accounts.schema.Query,
    courses.schema.Query,
):
    class Meta:
        description = 'Root Query'


class Mutation(
    restaurant.schema.Mutation,
    accounts.schema.Mutation,
    courses.schema.Mutation,
):
    class Meta:
        description = 'Root Mutation'


schema = graphene.Schema(query=Query, mutation=Mutation)
