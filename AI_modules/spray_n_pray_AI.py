## SPRAY_N_PRAY_AI
## Author: arda-guler
##
## Simplest AI I could come up with.
## Places points randomly, attacks randomly.
##
## Obligatory disclaimer: This is just a "game AI", and not a true Artificial Intelligence.

import random

def make_decisions(country, number_of_attacks, num_of_points):

    # place points
    point_placement_regions = []

    for i in range(num_of_points):
        r = random.choice(country.get_regions())
        point_placement_regions.append(r)

    list_of_regions_on_border = []
    for region in country.get_regions():
        if region.is_bordering_enemy():
            list_of_regions_on_border.append(region)

    # perform attack
    attack_origin = random.choice(list_of_regions_on_border)

    possible_targets = []
    for r in attack_origin.get_neighbours():
        if not r.get_owner() == country:
            possible_targets.append(r)

    attack_target = random.choice(possible_targets)
    
    return [[attack_origin, attack_target], point_placement_regions]
