import re
import requests
import json

from randomrecipe.recipe import Ingredient, Recipe


class MealDB:
    API_BASE = "https://www.themealdb.com/api/json/v1/1/"
    API_KEY = "1"
    RANDOM_MEAL_ENDPOINT = "random.php"
    DETAILS_ENDPOINT = "lookup.php?i="

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_random_recipe():
        recipe_response = requests.get(
            url=MealDB.API_BASE + MealDB.RANDOM_MEAL_ENDPOINT
        )
        if recipe_response.status_code != 200:
            print(f"Error {recipe_response.status_code}: {recipe_response.reason}")
            raise RuntimeError(
                f"Error fetching recipe - {recipe_response.status_code}: {recipe_response.reason}"
            )

        recipe_json: str = recipe_response.content.decode("utf-8")
        recipe_dict = json.loads(recipe_json)["meals"][0]

        details_response = requests.get(
            url=MealDB.API_BASE + MealDB.DETAILS_ENDPOINT + recipe_dict["idMeal"]
        )

        if details_response.status_code != 200:
            print(f"Error {details_response.status_code}: {details_response.reason}")
            raise RuntimeError(
                f"Error fetching recipe details - {details_response.status_code}: {details_response.reason}"
            )

        details_json: str = details_response.content.decode("utf-8")
        details_dict = json.loads(details_json)["meals"][0]

        return details_dict

    @staticmethod
    def to_recipe(recipe_dict: dict[str : str | None]) -> Recipe:
        ingredients_zip = {
            "strIngredient1": "strMeasure1",
            "strIngredient2": "strMeasure2",
            "strIngredient3": "strMeasure3",
            "strIngredient4": "strMeasure4",
            "strIngredient5": "strMeasure5",
            "strIngredient6": "strMeasure6",
            "strIngredient7": "strMeasure7",
            "strIngredient8": "strMeasure8",
            "strIngredient9": "strMeasure9",
            "strIngredient10": "strMeasure10",
            "strIngredient11": "strMeasure11",
            "strIngredient12": "strMeasure12",
            "strIngredient13": "strMeasure13",
            "strIngredient14": "strMeasure14",
            "strIngredient15": "strMeasure15",
            "strIngredient16": "strMeasure16",
            "strIngredient17": "strMeasure17",
            "strIngredient18": "strMeasure18",
            "strIngredient19": "strMeasure19",
            "strIngredient20": "strMeasure20",
        }

        ingredients: list[Ingredient] = []
        for ingredient_key, measure_key in ingredients_zip.items():
            print(ingredient_key, measure_key)
            ingredient_name = recipe_dict.get(ingredient_key)
            measure = recipe_dict.get(measure_key)

            if (ingredient_name is None) or (ingredient_name == ""):
                break

            note = None
            if (measure is None) or (measure == ""):
                print(f"Ingredient {ingredient_name} supplied without measure.")
                measure = ""
                note = "Ingredient has no measure."

            ingredient = Ingredient(
                name=ingredient_name,
                quantity=measure,
                notes=note,
            )

            ingredients.append(ingredient)

        instructions: str | None = recipe_dict.get("strInstructions")
        if instructions is None:
            print("strInstructions key not present")
            raise ValueError("strInstructions key not present")
        elif instructions == "":
            print("strInstructions value was blank for recipe")

        instructions = instructions.replace("\r", "")
        steps: list[str] = instructions.splitlines()
        steps = MealDB.remove_step_x_from_steps(steps)

        name: str = recipe_dict.get("strMeal", "<No name provided>")

        image_url: str = recipe_dict.get("strMealThumb", "")

        recipe = Recipe(
            name=name,
            ingredients=ingredients,
            steps=steps,
            image_url=image_url,
        )

        return recipe

    @staticmethod
    def remove_step_x_from_steps(steps: list[str]) -> list[str]:
        """
        If a steps[] contains like

        ```
        [
        "step 1",
        "blah",
        "step 2",
        "blah"
        ]
        ```

        we need to remove the 'step 1' and 'step 2' etc.
        """

        expression = r"step [0-9]*"
        expression2 = r"[0-9]*"

        new_steps: list[str] = []

        for step in steps:
            if (
                (re.fullmatch(expression, step.lower()) is None)
                and (re.fullmatch(expression2, step.lower()) is None)
                and (step != "")
            ):
                # it is a `step X`
                new_steps.append(step)

        return new_steps
