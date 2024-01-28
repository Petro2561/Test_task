from django.contrib import admin

from recipes.models import Product, Recipe, RecipeProduct


class ProductInRecipeAdmin(admin.TabularInline):
    model = RecipeProduct


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "get_products")
    list_filter = ("name",)
    search_fields = ("name",)

    inlines = [
        ProductInRecipeAdmin,
    ]

    def get_products(self, obj):
        return ", ".join(
            [
                f"{ingredient.product.name} ({ingredient.weight}г)"
                for ingredient in obj.recipes.all()
            ]
        )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Product)
