from unicodedata import category

from backend.recipes.recipe_extractor import get_all_recipes
from config.character_config import get_total_time_boost, get_smelting_magic_level, get_fisherman_level, \
    get_farming_trickery_level, get_most_efficient_fisherman_level, get_power_forager_level, get_the_lumberjack_level, \
    get_potion_duration
from market.market import get_info, get_detailed_info
from utils.item_id_lookup import lookup_item
import utils.constants as constants

import sys


def get_detailed_item_price(item_id, minimum_selling_stock, minimum_buying_demand, timeout):
    data, new_timeout = get_detailed_info(item_id, "cache/", timeout)
    sell_listings = data["lowestSellPricesWithVolume"]
    sell_listing_best_price = sys.maxsize
    supply = 0
    for entry in sell_listings:
        price = entry["key"]
        amount = entry["value"]
        supply += amount
        if supply > minimum_selling_stock:
            sell_listing_best_price = int(price)
            break
    buy_listings = data["highestBuyPricesWithVolume"]
    buy_listing_best_price = 0
    supply = 0
    for entry in buy_listings:
        price = entry["key"]
        amount = entry["value"]
        supply += amount
        if supply > minimum_buying_demand:
            buy_listing_best_price = int(price)
            break

    # if sell_listing_best_price == sys.maxsize and minimum_selling_stock > 0:
    #    print(f"Unable to find sell listing price with enough volume for item {item_id} ({minimum_selling_stock})")
    # if buy_listing_best_price == 0:
    #    print(f"Unable to find buy listing price with enough volume for item {item_id} ({minimum_buying_demand})")
    return sell_listing_best_price, buy_listing_best_price, new_timeout


def get_item_price(item_id, minimum_selling_stock, minimum_buying_demand, timeout):
    # Special case for recipes with no input (gathering). This can only happen to input items, and they are by definition "free"
    if item_id == -1:
        return 0, 0, timeout
    data, new_timeout = get_info(item_id, "cache/", timeout)
    if data["lowestPriceVolume"] > minimum_selling_stock:
        sell_listing_best_price = data["lowestSellPrice"]
    else:
        # demand = data["lowestPriceVolume"]
        # print(f"Lowest sell order not sufficient to covert need for item {item_id}, requires {minimum_selling_stock}, but found {demand}")
        return get_detailed_item_price(item_id, minimum_selling_stock, minimum_buying_demand, max(timeout, new_timeout))
    if data["highestPriceVolume"] > minimum_buying_demand:
        buy_listing_best_price = int(data["highestBuyPrice"])
    else:
        # demand = data["highestPriceVolume"]
        # print(f"Lowest buy order volume not sufficient to cover need for item {item_id}, requires {minimum_buying_demand}, but found {demand}")
        return get_detailed_item_price(item_id, minimum_selling_stock, minimum_buying_demand, max(timeout, new_timeout))
    return sell_listing_best_price, buy_listing_best_price, new_timeout

def get_item_base_price(item_name, path="data/item_base_prices.csv"):
    with open(path, 'r') as file:
        for line in file:
            if item_name in line:
                return int(line.split(",")[1])
    print(f"Unable to find base item price for item {item_name}")
    return 0

def calculate_trickery_for_recipe(recipe, amount_of_recipes):
    raw_recipe_results, _ = calculate_for_recipe(recipe, amount_of_recipes, 0.0)
    trickery_potion_id = 413
    recipe_time = float(raw_recipe_results["adjusted_time"])
    potion_duration = 10.0 * get_potion_duration()
    recipes_per_potion = potion_duration / recipe_time
    potions_needed = amount_of_recipes / recipes_per_potion
    potion_price, _, _ = get_item_price(trickery_potion_id, potions_needed, 0, 0)
    price_per_output = potion_price / recipes_per_potion
    base_price = get_item_base_price(recipe.output_item)

    new_output_price = raw_recipe_results["output_cost"] + (0.15 * float(base_price))

    raw_recipe_results["input_costs"] = price_per_output
    raw_recipe_results["input_cost_total"] = price_per_output
    raw_recipe_results["output_cost"] = new_output_price
    raw_recipe_results["total_profit"] = new_output_price
    raw_recipe_results["profit_per_second_base"] = float(new_output_price) / float(recipe.time_seconds)
    new_profit_per_second_adjusted = float(new_output_price) / float(raw_recipe_results["adjusted_time"])
    old_profit_per_second_adjusted = raw_recipe_results["profit_per_second_adjusted"]
    raw_recipe_results["profit_per_second_adjusted"] = new_profit_per_second_adjusted
    raw_recipe_results["trickery_potion_added"] = new_profit_per_second_adjusted - old_profit_per_second_adjusted

    return raw_recipe_results

def calculate_for_recipe(recipe, amount_of_recipes, timeout):
    new_timeout = 0
    item_output_name = recipe.output_item
    item_output_id = lookup_item(item_output_name)
    character_boost = get_total_time_boost(recipe.category)
    adjusted_time = character_boost * float(recipe.time_seconds)
    input_costs = []
    input_cost_total = 0
    output_amount = recipe.output_amount

    extra_output = ""
    extra_output_amount = 0

    if recipe.category == "Fishing":
        recipe.output_amount = float(output_amount) - get_most_efficient_fisherman_level()
        if recipe.output_item == "bloodmoon_eel":
            extra_output = "cooked_bloodmoon_eel"
        else:
            extra_output = recipe.output_item.replace("raw", "cooked")
        extra_output_amount = get_most_efficient_fisherman_level()

    for input_item, amount in recipe.input_items.items():
        input_item_id = lookup_item(input_item)
        minimum_sell_orders = int(amount) * amount_of_recipes
        sell_listing_best_price, _, new_timeout = get_item_price(input_item_id, minimum_sell_orders, 0,
                                                                 max(timeout, new_timeout))
        input_item_price = int(amount) * int(sell_listing_best_price)
        input_costs.append(input_item_price)
        input_cost_total += input_item_price
    # A mistake when inputting the smithing tasks means we don't have Smithing/Smelting as expected, but no other category uses purely "smithing"
    if recipe.category == "Smithing":
        input_cost_total = input_cost_total * get_smelting_magic_level()

    if recipe.category == "Farming":
        input_cost_total = input_cost_total * get_farming_trickery_level()

    if recipe.category == "Fishing":
        output_amount = float(output_amount) + get_fisherman_level()

    if recipe.category == "Foraging":
        output_amount = float(output_amount) + get_power_forager_level()

    if recipe.category == "Woodcutting":
        output_amount = float(output_amount) + get_the_lumberjack_level()

    minimum_buy_orders = amount_of_recipes * float(output_amount)
    _, buy_listing_best_price, new_timeout = get_item_price(item_output_id, 0, minimum_buy_orders,
                                                            max(timeout, new_timeout))

    output_cost = float(buy_listing_best_price) * float(output_amount)

    if extra_output != "":
        extra_item_id = lookup_item(extra_output)
        _, extra_buy_listing_best_price, _ = get_item_price(extra_item_id, 0, minimum_buy_orders,
                                                            max(timeout, new_timeout))
        output_cost += float(extra_buy_listing_best_price) * float(extra_output_amount)

    total_profit = output_cost - input_cost_total
    profit_per_second_base = 0
    profit_per_second_adjusted = 0
    if recipe.time_seconds != 0:
        profit_per_second_base = float(total_profit) / float(recipe.time_seconds)
        profit_per_second_adjusted = float(total_profit) / float(adjusted_time)

    # print(f"Finished analysing recipe {item_output_name}")

    return {"output_name": item_output_name,
            "category": recipe.category,
            "amount_of_recipes": amount_of_recipes,
            "base_time": recipe.time_seconds,
            "adjusted_time": adjusted_time,
            "input_costs": input_costs,
            "input_cost_total": input_cost_total,
            "output_cost": output_cost,
            "total_profit": total_profit,
            "profit_per_second_base": profit_per_second_base,
            "profit_per_second_adjusted": profit_per_second_adjusted}, new_timeout


def split_output_tsv(path="data/out/raw_prices.tsv", trickery=False):
    tsv_map = {}
    header = "output_name\tcategory\tamount_of_recipes\tbase_time\tadjusted_time\tinput_costs\tinput_costs_total\toutput_cost\ttotal_profit\tprofit_per_second_base\tprofit_per_second_adjusted"
    if trickery:
        header += "\ttrickery_added"
    for amount in constants.RECIPE_AMOUNTS_TO_CHECK:
        tsv_map[amount] = path.replace("raw_prices", f"prices_{amount}")
        with open(tsv_map[amount], 'w') as sub_file:
            sub_file.write(header + "\n")

    with open(path, 'r') as raw_file:
        for line in raw_file:
            if "output_name" in line:
                continue
            line_amount = int(line.split("\t")[2])
            with open(tsv_map[line_amount], 'a') as sub_file:
                sub_file.write(line)


def save_recipes(recipe_results, path="data/out/raw_prices.tsv", trickery=False):
    with open(path, "w") as file:
        file.write(
            "output_name\tcategory\tamount_of_recipes\tbase_time\tadjusted_time\tinput_costs\tinput_costs_total\toutput_cost\ttotal_profit\tprofit_per_second_base\tprofit_per_second_adjusted")
        if trickery:
            file.write("\ttrickery_added")
        file.write("\n")
        for result in recipe_results:
            prefix = ""
            for value in result.values():
                file.write(f"{prefix}{value}")
                prefix = "\t"
            file.write("\n")


def calculate_all():
    all_recipes = get_all_recipes()
    all_recipe_results = []
    trickery_recipe_results = []
    timeout = 3.1
    iterations = 0
    for recipe in all_recipes:
        iterations += 1
        for amount in constants.RECIPE_AMOUNTS_TO_CHECK:
            recipe_result, new_timeout = calculate_for_recipe(recipe, amount, timeout)
            all_recipe_results.append(recipe_result)
            if recipe.category in ["Woodcutting", "Fishing", "Foraging", "Mining"]:
                trickery_recipe_results.append(calculate_trickery_for_recipe(recipe, amount))
            timeout = new_timeout
        if iterations % 10 == 0:
            # Update our saved recipes every 10 iterations
            save_recipes(all_recipe_results)
            save_recipes(trickery_recipe_results, "data/out/trickery/raw_prices.tsv", True)
            split_output_tsv()
            split_output_tsv("data/out/trickery/raw_prices.tsv", True)
