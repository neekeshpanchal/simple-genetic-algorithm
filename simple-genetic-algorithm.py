import random
import matplotlib.pyplot as plot

#Global Variables and Inputs
poplength = 40
generations = 100000
bitlength = 24
crossover_rate = 0.4
mutation_rate = 0.04


indicator = input("""
Select your Function: \n
    (r) Rosenbrock's Valley
    (h) Himmelblau Function
    (d) De Jong Sphere Function \n
""")

choice = int(input("""
Select your choice of optimization: \n
    (1) Optimize
    (2) Optimize Please \n"""))

    
#Organism
class Organism:

    def __init__(self, code):
        self.code = code
        self.fitness = 0
        self.decoded = 0

    def __str__(self):

        return 'DNA Code: ' + str(self.code) + ' Fitness: ' + str(self.fitness)

# Objective Functions
def rosenbrockvalley(x):
    xrange = range(len(x)-1)
    return sum(100 * (x[i+1] - x[i]**2)**2 + (1-x[i])**2 for i in xrange)

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def dejong(x):
    return sum(xi**2 for xi in x)

# Objective Function Auxiliary

def string_split(code, n):
    return [code[i:i+n] for i in range(0, len(code), n)]

def decoder_r(individual):
    n = 3
    bits_list = string_split(individual.code, n)
    print(bits_list)


    num_signs = [(-1 if bits[0] == '0' else 1, int((float(bits))))
                  for bits in bits_list]


    x = [sign * (num % 2.048) for sign, num in num_signs]
    individual.decoded = x

    print(x)

    if x == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]:
        print("""Found the Optimal Value \n
                 Organism: """ + str(individual.code) + '\n' 
                 "Fitness: " + str(individual.fitness) + '\n')

        print(individual.decoded)

        exit(0)

    return x

def decoder_d(individual):
    n = 4
    bits_list = string_split(individual.code, n)

    num_signs = [(-1 if bits[0] == '0' else 1, int(float(bits)))
                 for bits in bits_list]

    ilist = [sign * (num % 5.12) for sign, num in num_signs]

    individual.decoded = ilist

    if ilist == [-0.0, -0.0, -0.0, -0.0, -0.0]:
            print("FOUND THE OPTIMAL VALUE:\nGlobal Optimum: " + str(individual.code) + '\n' "Fitness: " + str(individual.fitness))
            print(individual.decoded)
            exit(0)

    return ilist

def decoder_h(individual):
    mid = int(len(individual.code)/2)
    # Separate X and Y parameters
    binx, biny = individual.code[:mid], individual.code[mid:]
    # Establish Interval Multipliers
    xmult, ymult = int(binx, 2), int(biny, 2)
    # Highest possible x and y value is applied 

    x = interval(-4, 4, xmult, 2**len(binx))
    y = interval(-4, 4, ymult, 2**len(biny))

    if x == 3.0 and y== 2.0 or x == -2.805118 and y == 3.131312 or x == -3.779310 and y == -3.283186 or x == 3.584428 and y == -1.848126:
            print("FOUND THE GLOBAL MINIMA VALUE:\nGlobal Minima: " + str(individual.code) + '\n' "Fitness: " + str(individual.fitness))
            print(x,y)
            exit(0)

    elif x == -0.270845 and y == -0.923039:
            print("FOUND THE LOCAL MAXIMA VALUE:\nLocal Maxima: " + str(individual.code) + '\n' "Fitness: " + str(individual.fitness))
            print(x,y)
            exit(0)

    return x, y

def interval(lowest, highest, m, steps):
    step_size = (highest - lowest)/steps 
    return lowest + m*step_size

# Population Generation Methods

def chance(probability):

    return random.random() > probability

def random_binary(bitlength):

    return ''.join('0' if chance(0.5) else '1' for _ in range(bitlength))

def init_organism(dna):

    return Organism(dna)

def population_generate(poplength, bitlength):

    dnalist = []

    for x in range(0, poplength):
        dnalist.append(init_organism(random_binary(bitlength)))

    return dnalist


# Genetic Algorithm Operators

def reproduction(organisms, OF, choice):
    
    minimum_fitness = min(OF(organism) for organism in organisms)

    def weight(organism):

        fitness = OF(organism)
        organism.fitness = fitness

        if choice == 1:
            return (fitness - minimum_fitness + 1)

        elif choice == 2:
            return (1/(fitness - minimum_fitness + 1))
        
    # Organize weights according to the total weight (Biased Roulette % of Total Calculation)
    weights = [(organism, weight(organism)) for organism in organisms]
    weights_total = sum(x for organism, x in weights)
    all = [(node, x/weights_total) for node, x in weights]
 

    population_new = []

    for i in range(len(organisms)):
        rand = random.random()
        total = 0
        for organism, bias in all:
            total += bias
            if rand <= total:
                population_new.append(organism)
                break 
    
    print('\n'.join(map(str, population_new)))

    return population_new


def crossover(bin1, bin2, indice):
    node_i, node_j = bin1.code[:indice], bin1.code[indice:]
    node_i1, node_j1 = bin2.code[:indice], bin2.code[indice:]

    return node_i+node_j1, node_i1+node_j

def complete_crossover(population, crossover_rate):

    node_pairs = []
    final_population = []

    while len(population) > 1:
        node_pairs.append((population.pop(), population.pop()))

    if len(population) == 1:
        final_population.append(population.pop())

    for x1, x2 in node_pairs:

        if not chance(crossover_rate):
            final_population += [x1, x2]


        else:
            index = random.randint(1, len(x1.code) - 1)
            new_x1, new_x2 = crossover(x1, x2, index)
            final_population.append(init_organism(new_x1))
            final_population.append(init_organism(new_x2))

    return final_population

def mutation(organism, mutation_rate):
    
    flip = lambda x: '1' if x == '0' else '0'

    character = (flip(character) if chance(mutation_rate) else character for character in organism.code)

    return ''.join(character)

def population_mutation(population, mutation_rate):

    for organism in population:
        organism.code = mutation(organism, mutation_rate)

    return population

def ga():

    organisms = population_generate(poplength, bitlength)

    if indicator == 'h':
        OF = lambda code: himmelblau((decoder_h(code))[0],(decoder_h(code))[1])

    if indicator == 'r':
        OF = lambda code: rosenbrockvalley(decoder_r(code))

    if indicator == 'd':
        OF = lambda code: dejong(decoder_d(code))


    for generation in range(generations):

        print('Generation: ' + str(generation)) 

        organisms = reproduction(organisms, OF, choice)
        organisms = complete_crossover(organisms, crossover_rate)
        organisms = population_mutation(organisms, mutation_rate)



ga()
