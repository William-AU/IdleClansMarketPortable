import json
import logging

from backend.recipes.recipe_encoder import RecipeEncoder, Recipe, RecipeContainer
from configuration.log.logconfig import setup_logging
logger = logging.getLogger(__name__)

"""
Manual script for creating recipes (most information taken from the wiki)
"""

def save_recipe_container_to_json(container, filename):
    with open(filename, 'w') as f:
        json.dump(container, f, cls=RecipeEncoder, indent=4)


def load_recipe_container_from_json(path="../data/recipes.json", item_id_path="../data/item_ids.json"):
    with open(path, 'r') as f:
        data = json.load(f)
        recipes = [Recipe(**recipe_data, path=item_id_path) for recipe_data in data["recipes"]]
        return RecipeContainer(recipes)


def check_if_recipe_exists(container, recipe):
    for existing_recipe in container.recipes:
        if existing_recipe.output_item == recipe.output_item:
            return True
    return False


def create_recipe(input_items, output_item, category, xp, time_seconds, output_amount=1):
    recipe_container = load_recipe_container_from_json()
    new_recipe = Recipe(input_items, output_item, output_amount, category, xp, time_seconds)
    if check_if_recipe_exists(recipe_container, new_recipe):
        raise Exception("Recipe already exists!")
    recipe_container.recipes.append(new_recipe)
    save_recipe_container_to_json(recipe_container, "../data/recipes.json")
    logger.info(f"Created Recipe: {output_item}")


def load_from_json(output_item):
    with open(f"../data/recipes/{output_item}.json", 'r') as file:
        logger.debug(Recipe(**json.load(file)))


def create_simple(input_item, output_item, category, time, input_amount=1):
    input_items = {input_item: input_amount}
    create_recipe(input_items, output_item, category, 0, time)


def create_manual():
    input_items = {"cooked_zander": 3, "cooked_pufferfish": 1, "onion": 1, "cooked_quality_meat": 2}
    output_item = "power_pizza"
    time_seconds = 10
    category = "Cooking/Dishes"
    xp = 0
    create_recipe(input_items, output_item, category, xp, time_seconds)


def create_smelting_armor(material):
    create_recipe({f"{material}_bar": 6}, f"{material}_platebody", f"Smithing/{material}", 0, 9)
    create_recipe({f"{material}_bar": 4}, f"{material}_platelegs", f"Smithing/{material}", 0, 9)
    create_recipe({f"{material}_bar": 2}, f"{material}_helmet", f"Smithing/{material}", 0, 9)
    create_recipe({f"{material}_bar": 4}, f"{material}_shield", f"Smithing/{material}", 0, 9)


def create_smelting_accessory(material):
    create_recipe({f"{material}_bar": 2}, f"{material}_amulet", f"Smithing/{material}", 0, 3)
    create_recipe({f"{material}_bar": 2}, f"{material}_ring", f"Smithing/{material}", 0, 3)
    create_recipe({f"{material}_bar": 2}, f"{material}_bracelet", f"Smithing/{material}", 0, 3)
    create_recipe({f"{material}_bar": 2}, f"{material}_earrings", f"Smithing/{material}", 0, 3)

    create_recipe({f"{material}_bar": 1, f"{material}_precision_symbol": 1}, f"{material}_precision_ring",
                  f"Smithing/{material}", 0, 0)
    create_recipe({f"{material}_bar": 1, f"{material}_berserker_symbol": 1}, f"{material}_berserker_ring",
                  f"Smithing/{material}", 0, 0)
    create_recipe({f"{material}_bar": 1, f"{material}_arcane_symbol": 1}, f"{material}_arcane_ring",
                  f"Smithing/{material}", 0, 0)

    create_recipe({f"{material}_bar": 1, f"{material}_marksman_symbol": 1}, f"{material}_marksman_bracelet",
                  f"Smithing/{material}", 0, 0)
    create_recipe({f"{material}_bar": 1, f"{material}_brute_symbol": 1}, f"{material}_brute_bracelet",
                  f"Smithing/{material}", 0, 0)
    create_recipe({f"{material}_bar": 1, f"{material}_sorcerer_symbol": 1}, f"{material}_sorcerer_bracelet",
                  f"Smithing/{material}", 0, 0)


def create_cooking_fish_recipe(fish_name, time):
    create_recipe({f"raw_{fish_name}": 1}, f"cooked_{fish_name}", "Cooking/Fish", 0, time)


def create_trouser_coat(material):
    material_prefix = f"{material}_"
    if material == "":
        material_prefix = ""
    create_simple(f"{material_prefix}leather", f"{material_prefix}leather_trousers", "Crafting/Leather Gear", 7.5)
    create_simple(f"{material_prefix}leather", f"{material_prefix}leather_coat", "Crafting/Leather Gear", 7.5)


def create_ammunition(output_material, log_material):
    input_items = {f"{output_material}_bar": 1, f"{log_material}_log": 1}
    amount = 10
    if output_material == "astronomical":
        amount = 1000
    create_recipe(input_items, f"{output_material}_arrow", "Crafting/Ammunition", 0, 6, amount)


def create_fabric(material):
    robe_output_amount = 15
    trousers_output_amount = 10
    if material == "astronomical":
        robe_output_amount = 6
        trousers_output_amount = 4
    create_simple(f"{material}_flax", f"{material}_robe", "Crafting/Fabric", 7.5, robe_output_amount)
    create_simple(f"{material}_flax", f"{material}_trousers", "Crafting/Fabric", 7.5, trousers_output_amount)


def create_remaining_leather():
    create_recipe({"basilisk_scale": 2, "black_leather_trousers": 1}, "basilisk_scale_trousers",
                  "Crafting/Leather Gear", 0, 7.5)
    create_recipe({"basilisk_scale": 3, "black_leather_coat": 1}, "basilisk_scale_coat", "Crafting/Leather Gear", 0,
                  7.5)

    create_simple("astronomical_leather", "astronomical_leather_trousers", "Crafting/Leather Gear", 7.5, 4)
    create_simple("astronomical_leather", "astronomical_leather_coat", "Crafting/Leather Gear", 7.5, 6)


def create_no_input(name, time, category):
    create_simple("NONE", name, category, time)


def create_mining():
    category = "Mining"

    create_no_input("copper_ore", 3, category)
    create_no_input("tin_ore", 3, category)
    create_no_input("iron_ore", 4.5, category)
    create_no_input("silver_ore", 6, category)
    create_no_input("coal_ore", 7.5, category)
    create_no_input("gold_ore", 21, category)
    create_no_input("platinum_ore", 18, category)
    create_no_input("meteorite_ore", 26, category)
    create_no_input("diamond_ore", 29.5, category)
    create_no_input("titanium_ore", 35, category)


def create_woodcutting():
    category = "Woodcutting"

    create_no_input("spruce_log", 3, category)
    create_no_input("pine_log", 5, category)
    create_no_input("oak_log", 6, category)
    create_no_input("maple_log", 6.5, category)
    create_no_input("teak_log", 8, category)
    create_no_input("chestnut_log", 10, category)
    create_no_input("mahogany_log", 12.5, category)
    create_no_input("yew_log", 15, category)
    create_no_input("redwood_log", 17.5, category)
    create_no_input("magical_log", 20, category)


def create_fishing():
    category = "Fishing"

    create_no_input("raw_piranha", 5.25, category)
    create_no_input("raw_perch", 7.5, category)
    create_no_input("raw_mackerel", 9, category)
    create_no_input("raw_cod", 12, category)
    create_no_input("raw_trout", 9, category)
    create_no_input("raw_salmon", 13.5, category)
    create_no_input("raw_carp", 9.5, category)
    create_no_input("raw_zander", 15, category)
    create_no_input("raw_pufferfish", 18.75, category)
    create_no_input("raw_anglerfish", 30, category)
    create_no_input("raw_tuna", 45, category)
    create_simple("bloodmoon_worm", "bloodmoon_eel", category, 90)


def create_foraging():
    category = "Foraging"

    create_no_input("nettle", 6, category)
    create_no_input("kiwi", 7, category)
    create_no_input("onion", 7.5, category)
    create_no_input("magical_flax", 8, category)
    create_no_input("blueberry", 8, category)
    create_no_input("enchanted_flax", 8.5, category)
    create_no_input("porcini", 9, category)
    create_no_input("cursed_flax", 10, category)
    create_no_input("seaweed", 12.5, category)


def create_brewing():
    category = "Brewing"

    create_recipe({"tomato": 10, "nettle": 5, "pine_log": 2}, "potion_of_swiftness", category, 0, 55)
    create_recipe({"tomato": 10, "magical_flax": 15, "oak_log": 2}, "potion_of_negotiation", category, 0, 65)
    create_recipe({"cabbage": 15, "enchanted_flax": 10, "chestnut_log": 2}, "potion_of_resurrection", category, 0, 72.5)
    create_recipe({"strawberry": 10, "enchanted_flax": 15, "mahogany_log": 2}, "potion_of_forgery", category, 0, 85)
    create_recipe({"watermelon": 10, "magical_flax": 15, "teak_log": 2}, "potion_of_great_sight", category, 0, 97.5)
    create_recipe({"grapes": 10, "porcini": 15, "yew_log": 2}, "potion_of_trickery", category, 0, 115)
    create_recipe({"papaya": 10, "cursed_flax": 15, "redwood_log": 2}, "potion_of_dark_magic", category, 0, 132.5)
    create_recipe({"papaya": 15, "seaweed": 20, "magical_log": 2}, "potion_of_pure_power", category, 0, 155)
    create_recipe({"dragonfruit": 20, "seaweed": 50, "magical_log": 2}, "potion_of_ancient_knowledge", category, 0, 180)

def create_single_carpentry(material, time=9):
    category = "Carpentry"
    log = f"{material}_log"
    plank = f"{material}_plank"
    create_simple(log, plank, category, time)

# Carpentry assumes no gold cost for simplicity
def create_carpentry():
    create_single_carpentry("spruce")
    create_single_carpentry("pine")
    create_single_carpentry("oak")
    create_single_carpentry("maple")
    create_single_carpentry("teak")
    create_single_carpentry("chestnut")
    create_single_carpentry("mahogany")
    create_single_carpentry("yew")
    create_single_carpentry("redwood", 12)
    create_single_carpentry("magical", 15)

def create_single_farming(material, time):
    category = "Farming"
    seed = f"{material}_seed"
    if material == "grapes":
        seed = "grape_seed"
    create_recipe({seed:1}, material, category, 0, time, 5)

def create_farming():
    create_single_farming("potato", 30)
    create_single_farming("carrot", 40)
    create_single_farming("tomato", 60)
    create_single_farming("cabbage", 60)
    create_single_farming("strawberry", 90)
    create_single_farming("watermelon", 120)
    create_single_farming("grapes", 150)
    create_single_farming("papaya", 165)
    create_single_farming("dragonfruit", 180)

if __name__ == '__main__':
    setup_logging()
    # create_manual()
    create_farming()