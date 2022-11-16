import random

#Global Variables
population = 10
generations = 10000
num = int(input("How big is your gene pool? \n"))
num+=1
domain = []

choice = int(input("""
Pick your choice of optimization: \n
(1) Maximize
(2) Minimize
"""))

for x in range(1, num):
    domain.append(x)

#Organism Class 
class Organism:

    def __init__(self, code):
        self.code = code
        self.fitness = 0

    def __str__(self):

        return 'DNA Code: ' + str(self.code) + ' Fitness: ' + str(self.fitness)

#Mathematical Functions
def rosenbrockvalley(i,j):
    
    r = 0
    r += (1.0 - i)*(1.0 - i)+100.0*((j-i*i)*(j-i*i))

    return r


def dnageneration():

    dnalist = []

    while len(dnalist) != (population):
        a = random.choice(domain)
        b = random.choice(domain)
        c = random.choice(domain)
        dnalist.append((a,b,c))



    return dnalist
    

def ga():

    indicator = input("Type r for Rosenbrock's Valley:  \n")

    organisms = init_organisms(dnageneration())

    for generation in range(generations):
        print('Generation: ' + str(generation)) 

        organisms = fitness(organisms, indicator)
        organisms = selection(organisms)
        organisms = crossover(organisms)
        organisms = mutation(organisms)

        if choice == 1:
            if any(organism.code == (max(domain),max(domain),max(domain)) for organism in organisms):
                print('Function Maximized on generation ' + str(int(generation+1)))
                exit(0)
        
        else:
            if any(organism.code == (min(domain),min(domain),min(domain)) for organism in organisms):
                print('Function Minimized on generation ' + str(int(generation+1)))
                exit(0)




def init_organisms(dnalist):

    sample = []
    for x in range(len(dnalist)):
        sample.append(Organism(dnalist[x]))

    return sample


def fitness(organisms, indicator):

    if indicator.lower() == 'r':
        for organism in organisms:
            organism.fitness = rosenbrockvalley((organism.code[0]*organism.code[1]*organism.code[2]), sum(list(organism.code)))

    return organisms


def selection(organisms):

    organisms = sorted(organisms, key=lambda organism: organism.fitness, reverse=True)
    print('\n'.join(map(str, organisms)))

    if choice == 1:
        organisms = organisms[:int(0.4 * len(organisms))]

    else: 
        organisms = organisms[int(0.4 * len(organisms)):]

    return organisms


def crossover(organisms):

    offspring = []


    for x in range(int((population - len(organisms)) / 2)):

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


def mutation(organisms):

    for organism in organisms:

        for x in range(len(organism.code)):

            if random.uniform(0.0, 1.0) <= 0.1:

                code = list(organism.code)
                code[x] = random.choice(domain)
                organism.code = tuple(code)

    return organisms



ga()
