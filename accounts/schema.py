import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


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
        if not user.is_superuser:
            return [user]
        return get_user_model().objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, email, password):
        user = get_user_model()(
            username=email,
            email=email,
        )
        user.set_password(password)
        user.save()
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, token=token, refresh_token=refresh_token)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
