from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=250,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name + ', ' + self.measurement_unit


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=250,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        max_length=250,
        verbose_name='Слаг'
    )
    color = models.CharField(
        unique=True,
        max_length=250,
        verbose_name='Цветовой HEX-код',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Картинка',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Минуты',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиент',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_to_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_to_recipe',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Ингредиент',
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='favorite_user',
        verbose_name='Подписчик'
    )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='уникальные рецепты в избранном'
        ),
        )
        ordering = ('-id',)
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='unique_shopping_cart'
        ),
        )
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
