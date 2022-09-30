from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recipe

from .models import Follow, User


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request and not request.user.is_anonymous
                and Follow.objects.filter(user=self.context['request'].user,
                                          author=obj).exists())


class ShowFollowingRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class AddDeleteSubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)

    def get_recipes(self, author):
        recipes = author.recipes.all()
        return ShowFollowingRecipeSerializer(recipes, many=True).data

    def get_is_subscribed(self, author):
        return Follow.objects.filter(author=author,
                                     user=self.context['request']
                                     .user).exists()

    def get_recipes_count(self, author):
        return author.recipes.count()
