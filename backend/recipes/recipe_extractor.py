from backend.recipes.recipe_generator import load_recipe_container_from_json

def get_all_recipes():
    container = load_recipe_container_from_json(path="data/recipes.json", item_id_path="data/item_ids.json")
    return container.recipes