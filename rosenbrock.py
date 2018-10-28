from __future__ import division
import random

'''

Abbreviations:
gen:    generation, a set of peer solutions
sol:    solution, coordinates with SOL_DIM dimensions

Rosenbrock function: f(x, y) = (a - x) ^ 2 + b * (y - x ^ 2) ^ 2
Example parameters: a = 1 and b = 100
Goal: find the closest solution to the min of f(x, y)

'''

GEN_SIZE = 100
GEN_COUNT = 100
BOUNDS = ((-100, 100), (-100, 100))


def random_generation():
    generation = []
    for _ in xrange(GEN_SIZE):
        random_point = (random.randint(BOUNDS[0][0], BOUNDS[0][1]), random.randint(BOUNDS[1][0], BOUNDS[1][1]))
        generation.append(random_point)
    return generation


def rosenbrock(solution):
    return abs((1 - solution[0]) ** 2 + 100 * (solution[1] - solution[0] ** 2) ** 2)


def inverse(value):
    if value == 0:
        return 1
    else:
        return 1 / value


def fitness(solution):
    return inverse(rosenbrock(solution))


def probability(fitness_score, total):
    assert total != 0
    return fitness_score / total


def weighted_choice(items):
    weight_total = sum((item[1] for item in items))
    n = random.uniform(0, weight_total)
    for item, weight in items:
        if n < weight:
            return item
        n = n - weight
    return item


def crossover(solution1, solution2):
    # pos = int(random.random() * 2)    # this is a good line, but
    pos = 1                             # let's simplify
    return solution1[:pos] + solution2[pos:], solution2[:pos] + solution1[pos:]


def mutate(solution):
    tmp_sol = [solution[0], solution[1]]
    mutation_threshold = 0.2
    for i in range(len(solution)):
        if random.random() > mutation_threshold:
            tmp_sol[i] = random.randint(BOUNDS[i][0], BOUNDS[i][1])
    mutated_sol = (tmp_sol[0], tmp_sol[1])
    return mutated_sol


if __name__ == "__main__":
    cur_gen_count = 0
    gens = []

    # Step 1. Create an initial generation
    gen = random_generation()

    gens.append(gen)
    cur_gen_count += 1

    # Step 2. Calculate fitness
    fitness_scores = []
    for sol in gen:
        fitness_score = fitness(sol)
        fitness_scores.append(fitness_score)
    total_value = 0
    for score in fitness_scores:
        total_value += score
    probas = []
    for score in fitness_scores:
        proba = probability(score, total_value)
        probas.append(proba)
    weighted_gen = []
    for i, sol in enumerate(gen):
        weighted_gen.append(((sol[0], sol[1]), probas[i]))

    print "INITIAL GENERATION"
    print "\tGENERATION #%s" % cur_gen_count
    for i, sol in enumerate(weighted_gen):
        print "\t\tSolution #%s: %s, probability: %s%%" % \
              (i + 1, sol[0], int(sol[1] * 100))

    # Step 3. Create next generations
    print "NEXT GENERATIONS"

    for _ in xrange(GEN_SIZE - cur_gen_count):
        gen = []
        cur_gen_count += 1
        print "\tGENERATION #%s" % cur_gen_count

        for pair_i in xrange(int(GEN_SIZE / 2)):
            # Step 3.a Select parents
            print "\t\tPair #%s" % (pair_i + 1)
            parent1 = weighted_choice(weighted_gen)
            parent2 = weighted_choice(weighted_gen)
            print "\t\t\tParent 1: %s, Parent 2: %s" % (parent1, parent2)

            # Step 3.b Create children
            child1, child2 = crossover(parent1, parent2)
            print "\t\t\tChild 1: %s, Child 2: %s" % (child1, child2)

            # Step 3.c Mutate children
            print '\t\t\tChild Mutation:'
            child1 = mutate(child1)
            child2 = mutate(child2)
            print "\t\t\tChild 1: %s, Child 2: %s" % (child1, child2)

            gen.append(child1)
            gen.append(child2)

        gens.append(gen)

    print "LAST GENERATION"
    print "\tGENERATION #%s" % cur_gen_count

    weighted_gen = []
    fitness_scores = []
    for sol in gen:
        fitness_score = fitness(sol)
        fitness_scores.append(fitness_score)
    total_value = 0
    for score in fitness_scores:
        total_value += score
    probas = []
    for score in fitness_scores:
        proba = probability(score, total_value)
        probas.append(proba)
    weighted_gen = []
    for i, sol in enumerate(gen):
        weighted_gen.append(((sol[0], sol[1]), probas[i]))

    for i, sol in enumerate(weighted_gen):
        print "\t\tSolution #%s: %s, probability: %s%%" % \
              (i + 1, sol[0], int(sol[1] * 100))

    print("\nSUMMARY")

    for gen_i, gen in enumerate(gens):
        print "\tGENERATION #%s" % (gen_i + 1)
        for sol in enumerate(gen):
            print "\t\t", sol[1],
        print

    fittest_sol = gen[0]
    fitness_max = fitness(gen[0])
    for sol in gen:
        sol_fitness = fitness(sol)
        if sol_fitness >= fitness_max:
            fittest_sol = sol
            fitness_max = sol_fitness
    print "\nFittest solution: ", fittest_sol

    exit(0)