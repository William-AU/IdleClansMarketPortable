import json
from backend.recipes.recipe import Recipe
from backend.recipes.recipe_container import RecipeContainer

class RecipeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Recipe):
            return {
                "input_items": obj.input_items,
                "output_item": obj.output_item,
                "output_amount": obj.output_amount,
                "category": obj.category,
                "xp": obj.xp,
                "time_seconds": obj.time_seconds
            }
        if isinstance(obj, RecipeContainer):
            return {
                "recipes": obj.recipes  # List of Recipe objects
            }
        return super().default(obj)