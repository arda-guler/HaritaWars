## OPPORTUNIST_AI
## Author: arda-guler
##
## This AI module is a simple opportunist AI (hence the name).
##
## If the country is stronger than its neighbouring enemies, it places power points to strengthen its weakest borders.
## Otherwise, it tries to place them to inland regions to protect its power points and increase its power
## generation to be able to withstand powerful attacks without capitulating.
##
## As for attacks, it choses to attack the weakest enemy regions to get the most number of territories as quickly as possible.
##
## Obligatory disclaimer: This is just a "game AI", and not a true Artificial Intelligence.

import random

def make_decisions(country, number_of_attacks, points_to_place):
    
    # get regions with neighbours with max and min power differences
    best_attack_spots = []
    worst_defense_spots = []

    point_placement_regions = []

    for region in country.get_regions():
        if region.is_bordering_enemy():
            # [region, neighbour, power diff]
            if not len(worst_defense_spots) or worst_defense_spots[0][2] == region.get_strongest_enemy()[1]:
                worst_defense_spots.append([region, region.get_strongest_enemy()[0], region.get_strongest_enemy()[1]])
            elif len(worst_defense_spots) and worst_defense_spots[0][2] > region.get_strongest_enemy()[1]:
                worst_defense_spots = [[region, region.get_strongest_enemy()[0], region.get_strongest_enemy()[1]]]

            # [region, neighbour, power diff]
            if not len(best_attack_spots) or best_attack_spots[0][2] == region.get_weakest_enemy()[1]:
                best_attack_spots.append([region, region.get_weakest_enemy()[0], region.get_weakest_enemy()[1]])
            elif len(best_attack_spots) and best_attack_spots[0][2] < region.get_weakest_enemy()[1]:
                best_attack_spots = [[region, region.get_weakest_enemy()[0], region.get_weakest_enemy()[1]]]

    # attack!
    attack = random.choice(best_attack_spots)
    attack_origin = attack[0]
    attack_target = attack[1]

    inland_regions = []
    # we are weak, place points inland to protect our points and get stronger
    if country.get_power() < random.choice(worst_defense_spots)[1].get_owner().get_power():
        
        for r in country.get_regions():
            if not r.is_bordering_enemy():
                inland_regions.append(r)

        if inland_regions:
            for i in range(points_to_place):
                point_placement_regions.append(random.choice(inland_regions))

        else:
            for i in range(points_to_place):
                point_placement_regions.append(random.choice(best_attack_spots)[0])
    else:
    # we are strong, place power to defend borders
        for i in range(points_to_place):
            point_placement = random.choice(worst_defense_spots)
            point_placement_regions.append(point_placement[0])

    return [[attack_origin, attack_target], point_placement_regions]
