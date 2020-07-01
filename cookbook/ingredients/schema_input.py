import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Category, Dog, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="Nombre de la categoría")


class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, input=None):
        print(info.context.user)
        if info.context.user.is_anonymous:
            return None
            
        ok = True
        category_instance = Category(name=input.name)
        category_instance.save()
        return CreateCategory(ok=ok, category=category_instance)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CategoryInput(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        category_instance = Category.objects.get(pk=id)
        if category_instance:
            ok = True
            category_instance.name = input.name
            category_instance.save()
            return UpdateCategory(ok=ok, category=category_instance)

        return UpdateCategory(ok=ok, category=None)


class DogType(DjangoObjectType):
    class Meta:
        model = Dog


class DogInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)


class CreateDog(graphene.Mutation):
    class Arguments:
        input = DogInput(required=True)

    ok = graphene.Boolean()
    dog = graphene.Field(DogType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        dog_instance = Dog(pk=input.id, name=input.name)
        dog_instance.save()
        return CreateDog(ok=ok, dog=dog_instance)


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class IngredientInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True, description="Nombre del ingrediente")
    notes = graphene.String(description="Notas sobre el ingrediente", default_value="Ingredient notes")
    category_id = graphene.Int(description="Id de la categoría del ingrediente")
    
class CreateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientInput(required=True)

    ok = graphene.Boolean()
    errors = graphene.String()
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        category_instance = Category.objects.get(pk=input.category_id)
        if category_instance:
            ok = True
            ingredient_instance = Ingredient(name=input.name, notes=input.notes, category=category_instance)
            ingredient_instance.save()
            return CreateIngredient(ok=ok, ingredient=ingredient_instance)
        
        return CreateIngredient(ok=ok, errors="Id de la categoría no existe", ingredient=None)


class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = IngredientInput(required=True)

    ok =graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        ingredient_instance = Ingredient.objects.get(pk=id)
        if ingredient_instance:
            ok = True
            ingredient_instance.name = input.name
            ingredient_instance.notes = input.notes
            ingredient_instance.save()
            return UpdateIngredient(ok=ok, ingredient=ingredient_instance)

        return UpdateIngredient(ok=ok, ingredient=None)

class Query(ObjectType):
    category = graphene.Field(
        CategoryType,
        id=graphene.Int(),
        name=graphene.String()
    )
    categories = graphene.List(CategoryType)
    dog = graphene.Field(
        DogType,
        id=graphene.Int(),
        name=graphene.String()
    )
    dogs = graphene.List(DogType)
    ingredient = graphene.Field(
        IngredientType,
        id=graphene.Int(),
        name=graphene.String()
    )
    ingredients = graphene.List(IngredientType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get("id")
        if id:
            return Category.objects.get(pk=id)
        
        name = kwargs.get("name")
        if name:
            return Category.objects.get(name=name)
        
        return None

    
    def resolve_categories(self, info, **kwargs):
        categories = Category.objects.all()
        if categories:
            return categories

        return None

    def resolve_dog(self, info, **kwargs):
        id = kwargs.get("id")
        if id:
            print(Dog.objects.get(pk=id).data.get("owner"))
            return Dog.objects.get(pk=id)
        
        name = kwargs.get("name")
        if name():
            return Dog.objects.get(name=name)
        return None

    def resolve_dogs(self, info, **kwargs):
        dogs = Dog.objects.all()
        if dogs:
            return dogs

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get("id")
        if id:
            return Ingredient.objects.get(pk=id)

        name = kwargs.get("name")
        if name:
            return Ingredient.objects.get(name=name)

        return None

    def resolve_ingredients(self, info, **kwargs):
        ingredients = Ingredient.objects.all()
        if ingredients:
            return ingredients

        return None


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_dog = CreateDog.Field()
    create_ingredient = CreateIngredient.Field()
    update_category = UpdateCategory.Field()
    update_ingredient = UpdateIngredient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)