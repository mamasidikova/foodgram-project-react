from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, RecipeShowViewSet, TagsViewSet

router = SimpleRouter()

router.register('tags', TagsViewSet)
router.register('recipes', RecipeShowViewSet, basename="recipe")
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
