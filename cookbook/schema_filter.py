import graphene
import ingredients.schema_filter

class Query(ingredients.schema_filter.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
