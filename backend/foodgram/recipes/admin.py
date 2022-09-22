from django.contrib import admin
from .models import Ingredient, Recipe, IngredientInRecipe, Tag, Favorite


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ['name']
    search_fields = ('name',)


class RecipeIngredientsInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1
    raw_id_fields = ("ingredient",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'in_favorite_count')
    list_filter = ['name', 'author', 'tags']
    inlines = (RecipeIngredientsInline,)

    def in_favorite_count(self, obj):
        return obj.favorite_recipe.all().count()

