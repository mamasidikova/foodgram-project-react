from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, TagsViewSet, RecipeShowViewSet


router = SimpleRouter()

router.register('tags', TagsViewSet)
router.register('recipes', RecipeShowViewSet, basename="recipe")
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
