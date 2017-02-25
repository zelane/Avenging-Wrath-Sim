from __future__ import division

import json 

from copy import deepcopy
from random import choice
from time import sleep

### Calculators.com

class Target(object):

    __slots__ = ('health', 'name')

    @property
    def dead(self):
        return self.health == 0

    def hit(self, damage):
        self.health = max(0, self.health - damage)

    def __str__(self):
        return "%s: %s" % (self.name, self.health)


class Face(Target):

    def __init__(self):
        self.health = 30
        self.name = "The face"


class Minion(Target):

    def __init__(self, name, health):
        self.health = health
        self.name = name



shots_variants = [8, 7]
dps_variants = [
    1,
    # 2
]
minions_variants = [
    # [1],
    # [2],
    # [3],
    [4],
    # [8],
    # [1, 1],
    # [2, 2],
    # [3, 3],
    # [4, 4],
    # [6, 2]
]

tests = []

for shots in shots_variants:
    for dps in dps_variants:
        for minions in minions_variants:
            tests.append({
                "shots": shots,
                "dps": dps,
                "minions": minions
            })       

results = {}

shots = 8
damage_per_shot = 1


for test in tests:
    died_count = 0
    runs = 100000
    for run in xrange(runs):
        
        shots = test["shots"]
        dps = test['dps']
        minions = [Minion(chr(65+index), health) for index, health in enumerate(test['minions'])]
        targets = [Face()] + minions

        for shot in xrange(shots):
            target = choice(targets)
            # print [t.name for t in targets], target.name
            target.hit(dps)
            targets = [target for target in targets if not target.dead]

        if all([minion.dead for minion in minions]):
            died_count += 1


    print "\n######### Result ##########"
    probability_of_death = 0
    if died_count != 0:
        probability_of_death = (died_count / runs) * 100

    print json.dumps(test, indent=4, default=lambda x: str(x))
    print "Die", died_count,
    print "Survive", runs - died_count
    print "Probability of death: %s%%" % probability_of_death