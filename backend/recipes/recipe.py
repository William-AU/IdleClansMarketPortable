from backend.utils.item_validator import validate

class Recipe:
    def __init__(self, input_items, output_item, output_amount, category, xp, time_seconds, path="../data/recipes.json"):
        for item_name in input_items.keys():
            if not validate(item_name, path):
                raise Exception(f"Unknown item name: {item_name}")
        if not validate(output_item, path):
            raise Exception(f"Unknown output item: {output_item}")
        self.input_items = input_items
        self.output_item = output_item
        self.output_amount = output_amount
        self.category = category
        self.xp = xp
        self.time_seconds = time_seconds