import graphene
import ingredients.schema_basic


class Query(ingredients.schema_basic.Query, graphene.ObjectType):
    # Esta clase heredará más consultas a medida que instalemos más apps
    pass

class Mutation(ingredients.schema_basic.Mutation, graphene.ObjectType):
    # Esta clase heredará más consultas a medida que instalemos más apps
    pass

schema= graphene.Schema(query=Query, mutation=Mutation)