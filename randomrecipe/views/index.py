from django.shortcuts import render

from randomrecipe.api import MealDB
from randomrecipe.recipe import Recipe


def index(request):
    meal = MealDB.get_random_recipe()
    recipe = MealDB.to_recipe(meal)
    context = {"recipe": recipe}
    return render(request, "recipe.html", context)
