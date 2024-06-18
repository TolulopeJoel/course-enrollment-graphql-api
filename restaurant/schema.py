import graphene
from graphene_django import DjangoObjectType

from .models import Restaurant


class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = '__all__'


class Query(graphene.ObjectType):
    restaurants = graphene.List(RestaurantType)

    def resolve_restaurants(self, info, **kwargs):
        return Restaurant.objects.all()


class CreateRestaurant(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        address = graphene.String()
        suffix = graphene.String()

    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    def mutate(self, info, name, address, suffix=""):
        restaurant = Restaurant.objects.create(
            name=name + ' ' + suffix,
            address=address
        )

        return CreateRestaurant(ok=True, restaurant=restaurant)


class DeleteRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    def mutate(self, info, id):
        restaurant = Restaurant.objects.get(id=id)
        restaurant.delete()
        return DeleteRestaurant(ok=True)


class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        address = graphene.String()

    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    def mutate(self, info, id, name, address):
        restaurant = Restaurant.objects.get(id=id)
        restaurant.name = name
        restaurant.address = address
        restaurant.save()
        return UpdateRestaurant(ok=True, restaurant=restaurant)


class Mutation(graphene.ObjectType):
    create_restaurant = CreateRestaurant.Field()
    delete_restaurant = DeleteRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
