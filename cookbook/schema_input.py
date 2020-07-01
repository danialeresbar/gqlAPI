import graphene
import graphql_jwt
import ingredients.schema_input

class Query(ingredients.schema_input.Query, graphene.ObjectType):
    pass

class Mutation(ingredients.schema_input.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
