import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email']


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_whoami(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Authentication Failure: Your must be signed in")
        return user

    @login_required
    def resolve_users(self, info, **kwargs):
        user = info.context.user
        return get_user_model().objects.all() if user.is_superuser else [user]


schema = graphene.Schema(query=Query)
