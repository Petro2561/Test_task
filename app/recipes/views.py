from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

from recipes.models import Product, Recipe, RecipeProduct


def add_product_to_recipe(request, recipe_id, product_id, weight):
    recipe, created = RecipeProduct.objects.get_or_create(
        recipe_id=recipe_id, product_id=product_id, defaults={"weight": weight}
    )
    if not created:
        recipe.weight = weight
        recipe.save()
        return HttpResponse(
            f'Новый вес продукта "{recipe.product.name}" - {weight}г.'
        )
    return HttpResponse(f'Добавлен новый продукт: "{recipe.product.name}"')


@transaction.atomic
def cook_recipe(request, recipe_id):
    recipes = RecipeProduct.objects.filter(recipe=recipe_id)
    for recipe in recipes:
        recipe.product.used_count += 1
        recipe.save()
    recipes_names = ", ".join([recipe.product.name for recipe in recipes])
    return HttpResponse(f"Счетчик блюд для продуктов {recipes_names} изменен.")


def show_recipes_without_product(request, product_id):
    recipes = Recipe.objects.exclude(
        recipes__product=product_id, recipes__weight__gte=10
    )
    product = Product.objects.get(id=product_id).name
    return render(
        request,
        "recipes_without_product.html",
        {"recipes": recipes, "product": product},
    )
