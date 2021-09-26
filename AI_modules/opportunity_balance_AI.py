## OPPORTUNITY_BALANCE_AI
## Author: arda-guler
##
## Sometimes attacks like opportunist_AI, sometimes attacks like power_shift_AI, thanks to the power of
## the random number generator.
##
## Obligatory disclaimer: This is just a "game AI", and not a true Artificial Intelligence.

import random

def make_decisions(country, number_of_attacks, points_to_place):
    
    # get regions with neighbours with max and min power differences
    best_attack_spots = []
    worst_defense_spots = []

    power_shift_attacks = []

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

            # [region, neighbour, power diff]
            for neighbour in region.get_neighbours():
                if not neighbour.get_owner() == country:
                    if not len(power_shift_attacks) or (power_shift_attacks[0][2] == region.get_power() - neighbour.get_power() and region.get_power() - neighbour.get_power() >= 1):
                        power_shift_attacks.append([region, neighbour, region.get_power() - neighbour.get_power()])
                    elif len(best_attack_spots) and (power_shift_attacks[0][2] > region.get_power() - neighbour.get_power() and region.get_power() - neighbour.get_power() >= 1):
                        power_shift_attacks = [[region, neighbour, region.get_power() - neighbour.get_power()]]
             

    # attack!
    if len(power_shift_attacks):
        attack = random.choice([random.choice(best_attack_spots), random.choice(power_shift_attacks)])
    else:
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
