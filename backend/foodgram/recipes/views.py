from urllib import request
from rest_framework import permissions, viewsets

from .models import Tag, Recipe, Ingredient, Favorite, ShoppingList, IngredientInRecipe
from .permissions import AuthorOrReadOnly
from .mixins import RetriveAndListViewSet
from .serializers import ShowRecipeSerializer, TagsSerializer, IngredientSerializer, AddRecipeSerializer, FavoriteSerializer, ShoppingListSerializer
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .filters import IngredientSearchFilter, RecipeFilter
from .utils import make_file


class TagsViewSet(RetriveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientsViewSet(RetriveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeShowViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ShowRecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ShowRecipeSerializer
        return AddRecipeSerializer

    def get_queryset(self):
        favorite_flag = self.request.query_params.get("is_favorited")
        shopping_flag = self.request.query_params.get("is_in_shopping_cart")
        if favorite_flag:
            queryset = self.queryset.filter(
                favorite_recipe__user=self.request.user.id)
            return queryset
        elif shopping_flag:
            queryset = self.queryset.filter(
                shopping_cart__user=self.request.user.id)
            return queryset
        else:
            return self.queryset

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[AuthorOrReadOnly],
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"Ошибка": "Рецепт уже добавлен в избранное"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(favorite,
                                            context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[AuthorOrReadOnly],
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"error": "Этот рецепт уже в корзине покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shopping_cart = ShoppingList.objects.create(user=user,
                                                       recipe=recipe)
            serializer = ShoppingListSerializer(
                shopping_cart, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            delete_shoping_cart = ShoppingList.objects.filter(user=user,
                                                              recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        queryset = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).prefetch_related('ingredient')
        value_for_file = self.get_value(queryset)
        return make_file(value_for_file)

    def get_value(self, data):
        ingredients = {}
        for item in data:
            if item.ingredient in ingredients:
                ingredients[item.ingredient] += item.amount
            else:
                ingredients[item.ingredient] = item.amount
        return ingredients
