import random

#Global Variables
population = 10
generations = 10000

#Organism Class 
class Organism:

    def __init__(self, code):
        self.code = code
        self.fitness = 0

    def __str__(self):

        return 'DNA_Code: ' + str(self.code) + ' Fitness: ' + str(self.fitness)

#Mathematical Functions
def rosenbrockvalley(i,j):
    
    r = 0
    r += (1.0 - i)*(1.0 - i)+100.0*((j-i*i)*(j-i*i))

    return r


def dnageneration():

    domain = [1,2,3,4,5,6,7,8,9]
    dnalist = []

    while len(dnalist) != (population):
        a = random.choice(domain)
        b = random.choice(domain)
        c = random.choice(domain)
        dnalist.append((a,b,c))



    return dnalist
    

def ga():

    indicator = input("Type r for Rosenbrock's Valley:  ")

    organisms = init_organisms(population, dnageneration())

    for generation in range(generations):
        print('Generation: ' + str(generation)) 

        organisms = fitness(organisms, indicator)
        organisms = selection(organisms)
        organisms = crossover(organisms)
        organisms = mutation(organisms)

        if any(organism.fitness >= 10000000 for organism in organisms): #This line is a work in progress (dependent on type of optimization/function)

            print('Threshold met!')
            exit(0)


def init_organisms(population, dnalist):

    sample = []
    for x in range(len(dnalist)):
        sample.append(Organism(dnalist[x]))

    return sample


def fitness(organisms, indicator):

    if indicator.lower() == 'r':
        for organism in organisms:
            organism.fitness = rosenbrockvalley(organism.code[0],organism.code[1])

    return organisms


def selection(organisms):

    organisms = sorted(organisms, key=lambda organism: organism.fitness, reverse=True)
    print('\n'.join(map(str, organisms)))
    organisms = organisms[:int(0.4 * len(organisms))]

    return organisms


def crossover(organisms):

    offspring = []

    for x in range(int(population - len(organisms) / 2)):

        parent1 = organisms[0]
        parent2 = organisms[1]
        child1 = Organism(None)
        child2 = Organism(None)
        split = random.randint(0, 3)
        child1.code = parent1.code[0:split] + parent2.code[split:3]
        child2.code = parent2.code[0:split] + parent1.code[split:3]

        parent3 = organisms[2]
        parent4 = organisms[3]
        child3 = Organism(None)
        child4 = Organism(None)
        split = random.randint(0, 3)
        child3.code = parent3.code[0:split] + parent4.code[split:3]
        child4.code = parent4.code[0:split] + parent3.code[split:3]

        offspring.append(child1)
        offspring.append(child2)
        offspring.append(child3)
        offspring.append(child4)
    
    organisms.extend(offspring)


    return organisms
