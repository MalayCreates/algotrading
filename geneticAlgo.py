import backtest
import random
import numpy as np
import datetime
from strategies import MacdStrategy

# Author: Malay Agarwal

#####################################################################
# This is a simple genetic algorithm with an O(mng) complexity
# Runs each individual through a backtest 
# through a random quarter each generation to not overfit
# Each trait is a signal for BTO/STO/BTC/STC
# Crossover is handled by randomly selecting which traits get crossed
# Two random individuals from top 7 get picked to crossover
#####################################################################

# generate first gen population with random traits
def generate_population(size):
    population = []
    for i in range(size):
        t1 = random.uniform (-15,15)
        t2 = random.uniform (-15,15)
        t3 = random.uniform (-15,15)
        t4 = random.uniform (-15,15)
        individual = [t1,t2,t3,t4]
        population.append(individual)
    return population

# run backtest using the traits as signals
# return the end portfolio value
def apply_function(individual):
    backtest_hourly.signalValues = individual
    x = backtest.main()
    return x

# picks a random top 10 individual to be a parent
def choice_by_fitness(sorted_population):
    temp = random.randint(1,10)
    temp = temp * (-1)
    individual = sorted_population[(temp)]
    return individual

# Sort population by fitness/largest profit 
def sort_population_by_fitness(population):
    return sorted(population, key=apply_function)

# crossover traits
def crossover(individualA, individualB):
    # traits of parent A
    t1a,t2a,t3a,t4a = individualA[0],individualA[1],individualA[2],individualA[3]
    # traits of parent B
    t1b,t2b,t3b,t4b = individualB[0],individualB[1],individualB[2],individualB[3]
    # set child as identical copy of parent A
    newT1,newT2,newT3,newT4 = t1a,t2a,t3a,t4a
    crossed = [newT1,newT2,newT3,newT4]
    # Iterates through each trait
    for i in range(0,4):
        # 50/50 chance it crosses 
        # if it does, replace the trait at that index with parent B trait
        toCross = random.randint(0,1)
        if toCross == 0:
            crossed[i] = individualB[i]
    # return as new individual in next generation
    return crossed

# randomly add/subtract value of random trait
def mutate(individual):
    lower_bound, upper_bound = (-20,20)
    randT = random.randint(0,3)
    # add/subtract up to 5.5
    mutatedT = (individual[randT] + random.uniform(-5.5,5.5))
    # make sure it does not exceed bounds -20,20
    nextT = min(max(mutatedT, lower_bound),upper_bound)
    individual[randT] = nextT

    return individual

# create next generation
def create_next_gen(previous_population):

    next_generation = []
    sorted_by_fitness_population = sort_population_by_fitness(previous_population)
    population_size = len(previous_population)
    # each individual needs to be offspring from past generation
    # pick two parents
    for i in range(population_size):
        first_choice = choice_by_fitness(sorted_by_fitness_population)
        second_choice = choice_by_fitness(sorted_by_fitness_population)

        # crossover the two parents
        individual = crossover(first_choice, second_choice)
        # individual has a 1/7 chance if mutating
        toMutate = random.randint(1,7)
        if toMutate == 1:
            individual = mutate(individual)
        next_generation.append(individual)

    return next_generation


# 50 gens
generations = 50

# 100 pop size
population = generate_population(size=100)

i = 1

while i <= generations:
    print(f"🧬 GENERATION " + str(i))

    # uncomment for loop to have each individual print their final portfolio value
    # for speed recommended to comment out

    # for individual in population:
    #     print(individual, apply_function(individual))
    
    i += 1

    # this was redundant, but wanted to be sure to clear memory
    prev_gen = population
    population = create_next_gen(prev_gen)
    del(prev_gen)

    # Very important as to not overfit
    # randomizes which quarter is getting backtested each generation
    pickQ = random.randint(1,4)

    if pickQ == 1:
        backtest_hourly.startdate = datetime.datetime(2018,1,1)
        backtest_hourly.enddate = datetime.datetime(2018,4,1)
    elif pickQ == 2:
        backtest_hourly.startdate = datetime.datetime(2018,4,1)
        backtest_hourly.enddate = datetime.datetime(2018,7,1)
    elif pickQ == 3:
        backtest_hourly.startdate = datetime.datetime(2018,7,1)
        backtest_hourly.enddate = datetime.datetime(2018,10,1)
    else:
        backtest_hourly.startdate = datetime.datetime(2018,10,1)
        backtest_hourly.enddate = datetime.datetime(2018,1,1)


# Prints the final result
best_individual = sort_population_by_fitness(population)[-1]
print("\n🔬 FINAL RESULT")
print(best_individual, apply_function(best_individual))
