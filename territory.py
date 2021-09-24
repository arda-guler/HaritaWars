import random

class region():
    def __init__(self, name, owner, development, pos):
        self.name = name
        self.owner = owner
        self.development = development
        self.power = development
        self.pos = pos
        self.neighbours = []

    def get_pos(self):
        return self.pos

    def get_neighbours(self):
        return self.neighbours

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def get_name(self):
        return self.name

    def get_development(self):
        return self.development

    def get_power(self):
        return self.power

    def set_power(self, power):
        self.power = power

    def set_owner(self, owner):
        self.owner = owner

    def get_owner(self):
        return self.owner

    def get_weakest_enemy(self):
        weakest_enemy = None
        max_positive_diff = 0
        for n in self.get_neighbours():
            if not n.get_owner() == self.get_owner() and (not max_positive_diff or max_positive_diff < self.get_power() - n.get_power()):
                max_positive_diff = self.get_power() - n.get_power()
                weakest_enemy = n

        return (weakest_enemy, max_positive_diff)

    def get_strongest_enemy(self):
        strongest_enemy = None
        max_negative_diff = 0
        for n in self.get_neighbours():
            if not n.get_owner() == self.get_owner() and (not max_negative_diff or max_negative_diff > self.get_power() - n.get_power()):
                max_negative_diff = self.get_power() - n.get_power()
                strongest_enemy = n

        return (strongest_enemy, max_negative_diff)

    def is_bordering_enemy(self):
        is_bordering_enemy = False
        for n in self.get_neighbours():
            if not n.get_owner() == self.get_owner():
                is_bordering_enemy = True
                break

        return is_bordering_enemy

class country():
    def __init__(self, name, color, AI=None):
        self.name = name
        self.color = color
        self.regions = []
        self.AI = AI

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def get_regions(self):
        return self.regions

    def get_AI(self):
        if self.AI:
            return self.AI
        else:
            return None

    def get_power(self):
        power = 0
        for region in self.get_regions():
            power += region.get_power()

        return power

    def set_regions(self, regions):
        self.regions = regions

    def add_region(self, region):
        self.regions.append(region)

    def remove_region(self, region):
        self.regions.remove(region)

    def get_number_of_regions(self):
        return len(self.regions)

    def has_regions(self):
        if len(self.regions):
            return True
        else:
            return False

    def attack(self, origin, target):
        success = False
        
        if origin.get_owner() == target.get_owner():
            print("Can't attack self!")
            return

        if origin.get_power() > target.get_power():
            attack_strength = origin.get_power() * random.uniform(1, 1.5)
            defense_strength = target.get_power() * random.uniform(0.9, 1.25)
        elif origin.get_power() == target.get_power():
            attack_strength = origin.get_power() * random.uniform(0.9, 1.25)
            defense_strength = target.get_power() * random.uniform(0.9, 1.25)
        else:
            attack_strength = origin.get_power() * random.uniform(0.9, 1.25)
            defense_strength = target.get_power() * random.uniform(1, 1.5)

        if attack_strength > defense_strength:
            # attack success, change owner
            target.get_owner().remove_region(target)
            target.set_owner(self)
            self.add_region(target)

            # change values to after-war values
            o_p = origin.get_power()
            t_p = target.get_power()
            target.set_power(max(int(-defense_strength/2 + (o_p + attack_strength)/2), 1))
            origin.set_power(max(int((attack_strength + o_p)/4 - defense_strength/2), 1))

            success = True
            
        else:
            o_p = origin.get_power()
            t_p = target.get_power()
            target.set_power(max(int(t_p + o_p/2 + (attack_strength - defense_strength)/2), 1))
            origin.set_power(max(int(o_p/2 + (attack_strength - defense_strength)/2), 1))

        return success

    def place_point(self, region):
        region.set_power(region.get_power() + 1)

class game_map():
    def __init__(self, regions):
        self.regions = regions

    def get_regions(self):
        return self.regions

    def add_region(self, region):
        self.regions.append(region)

    def remove_region(self, region):
        self.regions.remove(region)
