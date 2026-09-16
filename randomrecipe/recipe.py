class Ingredient:
    name: str
    quantity: str
    notes: str | None

    def __init__(self, name: str, quantity: str, notes: str | None = None) -> None:
        self.name = name
        self.quantity = quantity
        self.notes = notes


class Recipe:
    name: str
    ingredients: list[Ingredient]
    steps: list[str]
    image_url: str | None

    def __init__(
        self,
        name: str,
        ingredients: list[Ingredient],
        steps: list[str],
        image_url: str | None = None,
    ) -> None:
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.image_url = image_url

    @staticmethod
    def pasta() -> Recipe:
        ingredients = [
            Ingredient(name="spaghetto", quantity="a handful"),
            Ingredient(name="tinned tomato", quantity="1 tin"),
            Ingredient(name="onion", quantity="1", notes="roughly chopped"),
        ]
        steps = [
            "Chop onions and fry on a medium heat until translucent",
            "Add tinned tomato and simmer for 20 mins",
            "Boil pasta for 9 mins for last 9 mins of vegetables simmering",
        ]
        recipe = Recipe(
            name="Pasta",
            ingredients=ingredients,
            steps=steps,
        )
        return recipe
