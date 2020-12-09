import numpy as np
from random import randint
from random import random
import copy


# We will use Manhattan distance
def l1(p1, p2):
    return np.sum(np.abs(np.array(p1) - np.array(p2)))


def l2(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def total_dist(data, dist_method=l1):
    answer = 0
    for i in range(len(data) - 1):
        answer += dist_method(data[i], data[i + 1])
    return answer


# =================MONTE CARLO=================#

def monte_carlo(cur_order, iters=100000, printDist=False, dist_method=l1):
    best_cost = total_dist(cur_order, dist_method)
    best_order = copy.deepcopy(cur_order)
    for _ in range(iters):
        cur_order = cur_order[np.random.permutation(cur_order.shape[0]), :]
        cur_cost = total_dist(cur_order, dist_method)
        if cur_cost < best_cost:
            if printDist:
                print(cur_cost, end=' ')
            best_order = copy.deepcopy(cur_order)
            best_cost = cur_cost
    return best_order, best_cost


# =================RANDOM WALK=================#

def random_walk(cur_order, iters=100000, printDist=False, dist_method=l1):
    def neighbour_dist(i, dist_method=l1):
        answer = 0
        if i != 0:
            answer += dist_method(cur_order[i], cur_order[i - 1])
        if i != len(cur_order) - 1:
            answer += dist_method(cur_order[i], cur_order[i + 1])
        return answer

    cur_order = cur_order[np.random.permutation(cur_order.shape[0]), :]
    best_order = copy.deepcopy(cur_order)
    cur_cost = total_dist(cur_order, dist_method)
    best_cost = cur_cost

    n = len(cur_order)

    for _ in range(iters):
        i1 = randint(0, n - 1)
        i2 = randint(0, n - 1)
        # to be sure that i1 != i2
        while i1 == i2:
            i2 = randint(0, n - 1)

        cur_cost -= neighbour_dist(i1, dist_method) + neighbour_dist(i2, dist_method)
        cur_order[[i1, i2]] = cur_order[[i2, i1]]
        cur_cost += neighbour_dist(i1, dist_method) + neighbour_dist(i2, dist_method)
        if cur_cost < best_cost:
            if printDist:
                print(cur_cost, end=' ')
            best_order = copy.deepcopy(cur_order)
            best_cost = cur_cost
    return best_order, best_cost


# =================HILL CLIMB=================#

# this is separate function for checking all neighbours
def try_all_swaps(cur_order, cur_cost, n, printDist=False, dist_method=l1):
    def neighbour_dist(i, dist_method=l1):
        answer = 0
        if i != 0:
            answer += dist_method(cur_order[i], cur_order[i - 1])
        if i != len(cur_order) - 1:
            answer += dist_method(cur_order[i], cur_order[i + 1])
        return answer

    best_order = copy.deepcopy(cur_order)
    best_cost = cur_cost

    for i1 in range(n):
        for i2 in range(n):
            if i1 == i2:
                continue
            this_cost = cur_cost
            cur_cost -= neighbour_dist(i1, dist_method) + neighbour_dist(i2, dist_method)
            cur_order[[i1, i2]] = cur_order[[i2, i1]]
            cur_cost += neighbour_dist(i1, dist_method) + neighbour_dist(i2, dist_method)
            if cur_cost < best_cost:
                if printDist:
                    print(cur_cost, end=' ')
                best_order = copy.deepcopy(cur_order)
                best_cost = cur_cost
            cur_order[[i1, i2]] = cur_order[[i2, i1]]
            cur_cost = this_cost
    return best_order, best_cost


def hill_climb(cur_order, iters=100000, printDist=False, dist_method=l1):
    cur_order = cur_order[np.random.permutation(cur_order.shape[0]), :]
    cur_cost = total_dist(cur_order, dist_method)
    best_cost = cur_cost
    best_order = copy.deepcopy(cur_order)
    n = len(cur_order)

    for _ in range(iters):
        best_order, best_cost = try_all_swaps(best_order, best_cost, n, printDist=printDist, dist_method=dist_method)

    return best_order, best_cost


# =================SIMULATED ANNEALING=================#

def annealing(cur_order, iters=100, delta_t=0.0001, t_max=100, printDist=False, dist_method=l1):
    t_max = max(t_max, 2)  # for protection
    cur_order = cur_order[np.random.permutation(cur_order.shape[0]), :]
    cur_order = cur_order.tolist()
    n = len(cur_order)
    cur_cost = total_dist(cur_order, dist_method)
    best_order = copy.deepcopy(cur_order)
    best_cost = cur_cost
    for _ in range(iters):
        for T in np.arange(t_max, 1, -1 * delta_t):
            i1 = randint(0, n - 1)
            i2 = randint(i1 + 1, n)
            cur_order[i1: i2] = reversed(cur_order[i1: i2])
            new_cost = total_dist(cur_order, dist_method)
            dE = cur_cost - new_cost
            if dE > 0 and np.exp(-dE / T) > random():
                cur_cost = new_cost
                if cur_cost < best_cost:
                    if printDist:
                        print(cur_cost, end=' ')
                    best_cost = cur_cost
                    best_order = copy.deepcopy(cur_order)
            else:
                cur_order[i1: i2] = reversed(cur_order[i1: i2])
    return np.array(best_order), best_cost


# =================GENETIC ALGORITHM=================#

def generate_pair(n):
    i1 = randint(0, n - 1)
    return i1, randint(i1 + 1, n)


def crossover(parent1, parent2):
    i1, i2 = generate_pair(len(parent1))
    child = [[-1, -1] for _ in range(len(parent1))]
    child[i1:i2] = parent1[i1:i2]
    pivot = 0
    for el in parent2:
        if pivot == i1:
            pivot = i2
        if el not in parent1[i1:i2]:
            child[pivot] = el
            pivot += 1
    return child


def genetic_algo(cur_order, iters, size=500, sel_rate=0.1, mut_rate=0.05, printDist=False, dist_method=l1):
    mut_rate = min(1.0, mut_rate)  # for protection
    best_order = copy.deepcopy(cur_order)
    best_cost = total_dist(best_order, dist_method)

    world = [cur_order[np.random.permutation(cur_order.shape[0]), :].tolist() for _ in range(size)]
    n = len(cur_order)
    for i in range(iters):
        # Selection: take best 10%
        cur_relatives = sorted(world, key=total_dist)[0:int(size * sel_rate)]
        world = []
        # Making offsprings using crossover
        for _ in range(size):
            p1, p2 = generate_pair(int(size * sel_rate) - 1)  # choose 2 random persons
            new_order = crossover(cur_relatives[p1], cur_relatives[p2])
            new_cost = total_dist(new_order, dist_method)
            world.append(new_order)
            if new_cost < best_cost:
                if printDist:
                    print(new_cost, end=' ')
                best_cost = new_cost
                best_order = copy.deepcopy(new_order)

        # Big mutations (reverse subarrays)
        for _ in range(int(size * mut_rate)):
            j = randint(0, size - 1)
            i1, i2 = generate_pair(n)
            world[j][i1: i2] = reversed(world[j][i1: i2])
        # Make small mutations (swaps)
        for _ in range(int(size * mut_rate)):
            j = randint(0, size - 1)
            i1, i2 = generate_pair(n - 1)
            world[j][i1], world[j][i2] = world[j][i2], world[j][i1]

    return np.array(best_order), best_cost
