import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta():
        model = Category


class CreateCategory(graphene.Mutation):
    class Arguments:
        # Los argumentos de entrada para esta mutación
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    def mutate(root, info, name):
        ok = True
        category_instance = Category(name=name)
        category_instance.save()
        return CreateCategory(ok=ok, category=category_instance)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        # Los argumentos de entrada para esta mutación
        name = graphene.String(required=True)
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    def mutate(self, info, name, id):
        ok = False
        category_instance = Category.objects.get(pk=id)
        if category_instance:
            ok = True
            category_instance.name = name
            category_instance.save()
            return UpdateCategory(ok=ok, category=category_instance)

        return UpdateCategory(ok=ok, category=None)


class IngredientType(DjangoObjectType):
    class Meta():
        model = Ingredient


class CreateIngredient(graphene.Mutation):
    class Arguments:
        # Los argumentos de entrada para esta mutación
        name = graphene.String(required=True)
        category_id = graphene.ID()

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    def mutate(root, info, name, category_id):
        ok = True
        category = Category.objects.get(id=category_id)
        if category == None:
            print("No se pudo crear el ingrediente")
            return CreateIngredient(ok=False, ingredient=None)

        ingredient_instance = Ingredient(name=name, notes="Ingredient notes", category=category)
        ingredient_instance.save()

        return CreateIngredient(ok=True, ingredient=ingredient_instance)


class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        notes = graphene.String()
        
    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    def mutate(self, info, name, notes, id):
        ok = False
        ingredient_instance = Ingredient.objects.get(pk=id)
        if ingredient_instance:
            ok = True
            ingredient_instance.name = name
            if notes:
                ingredient_instance.notes = notes

            ingredient_instance.save()
            return UpdateIngredient(ok=ok, ingredient=ingredient_instance)

        return UpdateIngredient(ok=ok, ingredient=None)


class Query(graphene.ObjectType):
    category = graphene.Field(
        CategoryType,
        id=graphene.Int(),
        name=graphene.String()
    )
    all_categories = graphene.List(CategoryType)
    ingredient = graphene.Field(
        IngredientType,
        id=graphene.Int(),
        name=graphene.String()
    )
    all_ingredients = graphene.List(IngredientType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        if id is not None:
            return Category.objects.get(pk=id)

        elif name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        if id is not None:
            return Ingredient.objects.get(pk=id)

        elif name is not None:
            return Ingredient.objects.get(name=name)

        return None

    def resolve_all_ingredients(self, info, **kwargs):
        # Se optimiza la consulta desde acá
        return Ingredient.objects.select_related('category').all()


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)