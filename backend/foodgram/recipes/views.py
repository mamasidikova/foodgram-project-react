from rest_framework import permissions, viewsets

from .models import Tag, Recipe, Ingredient, Favorite, ShoppingList
from .mixins import RetriveAndListViewSet
from .serializers import ShowRecipeSerializer, TagsSerializer, IngredientSerializer, AddRecipeSerializer, FavoriteSerializer, ShoppingListSerializer
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


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


class RecipeShowViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ShowRecipeSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ShowRecipeSerializer
        return AddRecipeSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        # url_path="favorite",
        # permission_classes=[IsAuthorOrAdmin],
    )
    def favorite(self, request, pk=None):
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
        url_path="shopping_cart",
        # permission_classes=[IsAuthorOrAdmin],
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"error": "Этот рецепт уже в корзине покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shoping_cart = ShoppingList.objects.create(user=user,
                                                       recipe=recipe)
            serializer = ShoppingListSerializer(
                shoping_cart, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            delete_shoping_cart = ShoppingList.objects.filter(user=user,
                                                              recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
