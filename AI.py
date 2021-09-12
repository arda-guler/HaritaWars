import random
import importlib
import math

default_AI = "opportunist_AI"

def get_AI_commands(country):
    # this function provides AI with country, the number of attacks a country
    # can perform at that turn, and the number of points it can place

    # No AI should exceed these parameters EVER for it to be a fair fight
    
    points_to_place = 1 + int(math.log(country.get_power())/(0.5 * country.get_number_of_regions()**2))

    # num. of attacks per turn is not a variable for now
    number_of_attacks = 1

    # use default AI
    if not country.get_AI() or country.get_AI() == "default_AI" or country.get_AI() == "":
        AI_module = importlib.import_module("AI_modules.opportunist_AI")
        return make_decisions(country, number_of_attacks, points_to_place)

    # use custom AI
    else:
        AI_module = importlib.import_module("AI_modules." + country.get_AI())
        return AI_module.make_decisions(country, number_of_attacks, points_to_place)

    
