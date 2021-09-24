import math

def get_human_commands(country, globe):
    
    def get_region_by_name(name):
        for r in globe.get_regions():
            if r.get_name() == name:
                return r

    def get_region_in_country_by_name(name):
        for r in country.get_regions():
            if r.get_name() == name:
                return r

    print(country.get_name())
    points_to_place = 1 + int(math.log(country.get_power())/(0.5 * country.get_number_of_regions()**2))
    print("Points to place: " + str(points_to_place))

    # num. of attacks per turn is not a variable for now
    number_of_attacks = 1
    print("Number of attacks: " + str(number_of_attacks))

    point_placement_regions = []
    for i in range(points_to_place):
        point_placement_regions.append(get_region_in_country_by_name(input("Place +1 to region: ")))

    attack_origin = None
    attack_target = None
    for i in range(number_of_attacks):
        attack_origin = get_region_in_country_by_name(input("Attack origin: "))
        attack_target = get_region_by_name(input("Attack target: "))
        
    return [[attack_origin, attack_target], point_placement_regions]

    
