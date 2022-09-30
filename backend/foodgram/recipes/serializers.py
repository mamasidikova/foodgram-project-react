import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingList, Tag, User)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class ShowIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class ShowRecipeSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = ShowIngredientInRecipeSerializer(
        source="ingredient_to_recipe", many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:

        model = Recipe
        fields = ('id', 'tags', 'author',
                  'ingredients', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time'
                  )

    def _get_is_state(self, obj, model):
        request = self.context.get('request', None)
        return (request and not request.user.is_anonymous
                and model.objects.filter(recipe=obj,
                                         user=request.user).exists())

    def get_is_favorited(self, obj):
        return self._get_is_state(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self._get_is_state(obj, ShoppingList)


class ShowRecipeMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class AddRecipeSerializer(serializers.ModelSerializer):
    ingredients = AddIngredientInRecipeSerializer(
        source="ingredient_to_recipe", many=True
    )
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image',
                  'name', 'image', 'text', 'cooking_time')

    def validate_ingredients(self, data):
        ingredients_list = []
        for elem in data:
            ingredient = elem['id']
            amount = elem['amount']

            if ingredient in ingredients_list:
                raise serializers.ValidationError([{
                    'Ошибка': ['Ингредиент уже добавлен']
                }])
            elif amount < 1:
                raise serializers.ValidationError([{
                    'Ошибка': ['Количество ингредиентов должно быть целым'
                               ' положительным числом']
                }])
            else:
                ingredients_list.append(ingredient)
        return data

    def validate_tags(self, data):
        if len(data) == 0:
            raise serializers.ValidationError(
                'Добавьте тег',
            )
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError('Время готовки должно быть'
                                              ' больше нуля минут')
        return data

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            if IngredientInRecipe.objects.filter(
                    recipe=recipe,
                    ingredient=ingredient_id,
            ).exists():
                amount += ingredient['amount']
            IngredientInRecipe.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient_id,
                defaults={'amount': amount},
            )

    def create(self, validated_data):
        author = self.context["request"].user
        ingredients = validated_data.pop('ingredient_to_recipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.add_recipe_ingredients(
            ingredients,
            recipe,
        )
        return recipe

    def update(self, instance, validated_data):
        if 'ingredient_to_recipe' in validated_data:
            ingredients = validated_data.pop('ingredient_to_recipe')
            instance.ingredients.clear()
            self.add_recipe_ingredients(
                ingredients,
                instance,
            )
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        if Favorite.objects.filter(
                user=self.context.get('request').user,
                recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже добавлен в избранное '
            })
        return data

    def to_representation(self, instance):
        return ShowRecipeMinSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRecipeSerializer(instance.recipe, context=context).data
