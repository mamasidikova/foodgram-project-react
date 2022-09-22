from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, TagsViewSet, RecipeShowViewSet


router = SimpleRouter()

router.register('tags', TagsViewSet)
router.register('recipes', RecipeShowViewSet)
router.register('ingredients', IngredientsViewSet)


urlpatterns = [
    # path('recipes/<int:id>/favorite/', APIFavorite.as_view()),
    path('', include(router.urls)),
]
