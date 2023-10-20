import math
import os
import time
from typing import Tuple
from copy import deepcopy

cur_dir = os.path.dirname(__file__)
infile = os.path.join(cur_dir, 't.txt')

print('\nStarting optimized version...')

# Set globals
overall_start = time.time()

MAX_MINUTE = 24
ore_index = 0
clay_index = 1
obsidian_index = 2
geode_index = 3
resource_map = {
    'ore': 0,
    'clay': 1,
    'obsidian': 2,
    'geode': 3,
}
index_map = {
    0: 'ore',
    1: 'clay',
    2: 'obsidian',
    3: 'geode',
}

fourtuple = Tuple[int, int, int, int]

def parse_costs(cost_str: str) -> fourtuple:
    cost_list = [0,0,0,0]

    # chop to costs, then split on "and"
    _, cost_str = cost_str.split('costs ')
    # each resource cost is a str like '4 ore', connected by 'and'
    resource_costs = [c.split() for c in cost_str.split(' and ')]
    for amount, resource_type in resource_costs:
        resource_index = resource_map[resource_type]
        cost_list[resource_index] += int(amount)
        
    return tuple(cost_list)


# Parse blueprints from input
blueprints = {}
for l in open(infile).readlines():
    l = l.strip()
    if not l:
        continue

    blueprint_str, pieces = l.split(':')
    blueprint_number = blueprint_str.split()[1]
    costs = pieces.split('.')[:4]

    blueprint_costs = []
    for i, cur_cost in enumerate(costs):
        cur_type = index_map[i]
        resource_costs = [0, 0, 0, 0]
        
        resource_costs = parse_costs(cur_cost)
        blueprint_costs.append(resource_costs)
    blueprints[int(blueprint_number)] = blueprint_costs
#print(blueprints)


# Helpers for mapping addition over tuples
def tuple_add(t1, t2):
    return tuple(map(lambda i, j: i + j, t1, t2))

def tuple_sub(t1, t2):
    return tuple(map(lambda i, j: i - j, t1, t2))


class State():
    """Primary class to reflect the current state of the game"""
    def __init__(self):
        self.resources = (0, 0, 0, 0)
        self.robots = (1, 0, 0, 0)
        self.minute = 1

    def collect_resources(self, n=1):
        self.resources = tuple(
            self.resources[i] + self.robots[i] * n
            for i in range(4)
        )
        self.minute += n

    def get_build_choices(self):
        if self.robots[geode_index] > 0:
            return [3, 2]
        elif self.robots[obsidian_index] > 0:
            return [3, 2, 1]
        elif self.robots[clay_index] > 0:
            return [2, 1, 0]
        else:
            # optimization: don't try to build ore bots late in the game
            if self.minute < 18:
                return [1, 0]
            else:
                return [1]
    
    def calculate_wait(self, choice: int, blueprint) -> int:
        max_turns_required = 0
        for i, cost in enumerate(blueprint[choice]):
            if cost == 0:
                continue
            resources_required = cost - self.resources[i]
            if resources_required:
                turns_required = math.ceil(resources_required / self.robots[i])
                max_turns_required = max(max_turns_required, turns_required)
        return max_turns_required

    
    def build_robot(self, choice: int, blueprint):
        # Subtract resources, add a robot
        robot_cost = blueprint[choice]
        self.resources = tuple_sub(self.resources, robot_cost)

        choice_list = [
            1 if i == choice
            else 0
            for i in range(4)
        ]
        self.robots = tuple_add(self.robots, choice_list)
    
    def run_til_end(self) -> int:
        '''Return the number of geodes at the end'''
        minutes_left = 25 - self.minute
        self.collect_resources(minutes_left)
        return self.resources[geode_index]

    def get_cache_key(self):
        return (
            self.resources,
            self.robots,
            self.minute
        )


state_cache = {}
cache_hits = 0
# PERF OPTIMIZATION: store blueprint in a global instead of the State class
g_cur_blueprint = {}
def run(cur_state: State) -> int:
    """Explore all of the choices (DFS) and find the optimal strategy"""
    global state_cache, cache_hits

    cache_key = cur_state.get_cache_key()
    cached_value = state_cache.get(cache_key)
    if cached_value:
        cache_hits += 1
        return cached_value

    if cur_state.minute > MAX_MINUTE:
        return cur_state.resources[geode_index]

    max_geodes = 0
    build_choices = cur_state.get_build_choices()
    for choice in build_choices:
        new_state = deepcopy(cur_state)
        # plus one because it takes a turn to build the robot
        turns_required = new_state.calculate_wait(choice, g_cur_blueprint) + 1

        # if we've got time left, keep playing
        if turns_required + new_state.minute <= MAX_MINUTE:
            new_state.collect_resources(turns_required)
            # minutes and resources are now adjusted, now build the robot
            new_state.build_robot(choice, g_cur_blueprint)

            potential_geodes = run(new_state)
            max_geodes = max(max_geodes, potential_geodes)
        # if we'd go over time, return the geode result
        else:
            # don't bother simulating if we don't have geode bots
            if new_state.robots[geode_index]:
                potential_geodes = new_state.run_til_end()
                max_geodes = max(max_geodes, potential_geodes)
    
    state_cache[cache_key] = max_geodes

    return max_geodes


def get_most_geodes():
    """Get the best answer for the given blueprint"""
    global state_cache
    cur_state = State()
    state_cache = {}

    max_geodes = run(cur_state)

    return max_geodes


def main():
    """Assess each of the blueprints to get the best answer"""
    global g_cur_blueprint

    total_quality = 0
    for blueprint_number, cur_blueprint in blueprints.items():

        start_time = time.time()
        g_cur_blueprint = cur_blueprint
        num_geodes = get_most_geodes()
        print(f'{blueprint_number} best geodes: {num_geodes}')

        total_quality += num_geodes * blueprint_number

    print('Answer: ', total_quality)

    overall_duration = time.time() - start_time
    print(f'Duration {overall_duration:0.2f}')


main()
