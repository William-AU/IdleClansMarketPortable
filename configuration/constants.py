from datetime import timedelta
CACHE_REFRESH_TIME = timedelta(hours=4)
TIME_FORMAT_STRING = "%y/%m/%d %H:%M:%S"
# When calculating the price of a recipe, we consider breakpoints for number of recipes that the market must support for us to consider them
# For example, 1000 means that there must be 1000 * (required input items) sell orders on the market, and 1000 * (output item) buy orders on the market
RECIPE_AMOUNTS_TO_CHECK = [1, 10, 1_000, 10_000, 100_000]

