import re, sys
from operator import attrgetter

class Attack:
    def __init__(self, type, damage, initiative):
        self.type = type
        self.damage = damage
        self.initiative = initiative

    def __str__(self):
        return f'({self.type} D: {self.damage} I: {self.initiative})'

class Group:
    REGEX = re.compile('(\d+) units each with (\d+) hit points (\((weak|immune) to \w+(, \w+)*(; (weak|immune) to \w+(, \w+)*)*\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    def __init__(self, description):
        m = self.REGEX.match(description)
        assert m
        self.num_units = int(m.group(1))
        self.hit_points = int(m.group(2))
        self.attack = Attack(m.group(m.lastindex - 1), int(m.group(m.lastindex - 2)), int(m.group(m.lastindex)))
        self.weaknesses = []
        self.immunities = []
        self.target = None
        if m.group(3):
            for defense in m.group(3).split(';'):
                defense = defense.strip('() ')
                if defense.startswith('weak'):
                    self.weaknesses = defense[len('weak to '):].split(', ')
                elif defense.startswith('immune'):
                    self.immunities = defense[len('immune to '):].split(', ')

    def attack_target(self):
        if self.is_alive and self.target:
            self.target.num_units -= int(self.attack_damage(self.target) / self.target.hit_points)
        self.target = None

    def attack_damage(self, other):
        if self.attack.type in other.immunities:
            return 0
        elif self.attack.type in other.weaknesses:
            return self.effective_power * 2
        else:
            return self.effective_power

    @property
    def is_alive(self):
        return self.num_units > 0

    def set_target(self, target):
        self.target = target

    @property
    def effective_power(self):
        return self.num_units * self.attack.damage

    def __str__(self):
        return f'#: {self.num_units} HP: {self.hit_points} A: {self.attack} W: {self.weaknesses} I: {self.immunities}'

class Army:
    def __init__(self, name):
        self.name = name
        self.groups = []

    def add_group(self, group):
        group.army = self
        self.groups.append(group)

    @property
    def is_alive(self):
        return len(self.groups) > 0

    @property
    def unit_count(self):
        unit_count = 0
        for g in self.groups:
            unit_count += g.num_units
        return unit_count

    def remove_dead_groups(self):
        self.groups = [u for u in self.groups if u.is_alive]

    def __str__(self):
        return self.name + '\n' + '\n'.join([str(g) for g in self.groups])

class War:
    def __init__(self, description_file):
        self.armies = []
        for line in description_file:
            line = line.strip()
            if line:
                m = re.match('(.+):', line)
                if m:
                    self.armies.append(Army(m.group(1)))
                else:
                    self.armies[-1].add_group(Group(line))

    def attack(self):
        for g in self.attack_groups:
            g.attack_target()

    @property
    def attack_groups(self):
        groups = []
        for a in self.armies:
            groups += a.groups
        return sorted(groups, key=attrgetter('attack.initiative'), reverse=True)

    def fight(self):
        while self.armies[0].is_alive and self.armies[1].is_alive:
            self.select_targets()
            self.attack()
            self.remove_dead_groups()
        return self.armies[0] if self.armies[0].is_alive else self.armies[1]

    def get_targets(self, group):
        targets = self.armies[1].groups if group.army == self.armies[0] else self.armies[0].groups
        targets = sorted(targets, key=attrgetter('effective_power', 'attack.initiative'), reverse=True)
        targets = sorted(targets, key=lambda t: group.attack_damage(t), reverse=True)
        return [t for t in targets if group.attack_damage(t) > 0]

    def remove_dead_groups(self):
        for a in self.armies:
            a.remove_dead_groups()

    def select_targets(self):
        targeted_groups = []
        for g in self.targeting_groups:
            for t in self.get_targets(g):
                if t not in targeted_groups:
                    g.set_target(t)
                    targeted_groups.append(t)
                    break

    @property
    def targeting_groups(self):
        groups = []
        for a in self.armies:
            groups += a.groups
        return sorted(groups, key=attrgetter('effective_power', 'attack.initiative'), reverse=True)

    def __str__(self):
        return '\n'.join([str(army) for army in self.armies])

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        war = War(file)

victor = war.fight()

print(f'"{victor.name}" won with {victor.unit_count} units remaining')
