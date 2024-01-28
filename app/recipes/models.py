from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    used_count = models.PositiveIntegerField(
        default=0, verbose_name="Раз использовано в рецепте"
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название рецепта")

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепта",
        related_name="recipes",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="products",
    )
    weight = models.PositiveIntegerField(verbose_name="В граммах")

    class Meta:
        unique_together = ["recipe", "product"]

    def __str__(self):
        return f"{self.weight}g of {self.product.name} in {self.recipe.name}"
