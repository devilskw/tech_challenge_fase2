import random
from deap import base, creator, tools, algorithms

# Define the problem
NUM_DRIVERS = 5
NUM_DELIVERIES = 10
DELIVERY_POINTS = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(NUM_DELIVERIES)]

# Define the genetic algorithm parameters
POPULATION_SIZE = 100
GENERATIONS = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1

# Define the fitness function
def evaluate_route(individual):
    distance = 0
    for i in range(len(individual) - 1):
        distance += ((DELIVERY_POINTS[individual[i]][0] - DELIVERY_POINTS[individual[i+1]][0]) ** 2 +
                     (DELIVERY_POINTS[individual[i]][1] - DELIVERY_POINTS[individual[i+1]][1]) ** 2) ** 0.5
    return distance,

# Create the DEAP framework
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=NUM_DELIVERIES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_route)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run the genetic algorithm
population = toolbox.population(n=POPULATION_SIZE)
fitnesses = list(map(toolbox.evaluate, population))
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

for gen in range(GENERATIONS):
    descendentes = algorithms.varOr(population, toolbox, CROSSOVER_RATE, MUTATION_RATE)
    fits = list(map(toolbox.evaluate, descendentes))
    for ind, fit in zip(descendentes, fits):
        ind.fitness.values = fit

    population[:] = descendentes
    fits = [ind.fitness.values[0] for ind in population]
    best_ind = tools.selBest(population, k=1)[0]
    best_fit = best_ind.fitness.values[0]
    print(f"Generation {gen}: Best fitness = {best_fit}")

# Output the best route for each driver
for driver in range(NUM_DRIVERS):
    print(f"Driver {driver}: {[i for i, bit in enumerate(best_ind) if bit == 1]}")

