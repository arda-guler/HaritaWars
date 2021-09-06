import random

def make_decisions(country):

    points_to_place = max(int(country.get_power()/10), 1)

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
            elif len(best_attack_spots) and best_attack_spots[0][2] > region.get_weakest_enemy()[1]:
                best_attack_spots = [[region, region.get_weakest_enemy()[0], region.get_weakest_enemy()[1]]]

    # attack!
    attack = random.choice(best_attack_spots)
    attack_origin = attack[0]
    attack_target = attack[1]

    # place power to defend
    for i in range(points_to_place):
        point_placement = random.choice(worst_defense_spots)
        point_placement_regions.append(point_placement[0])

    return [[attack_origin, attack_target], point_placement_regions]
