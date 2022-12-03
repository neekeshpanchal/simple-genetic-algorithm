import random
import matplotlib.pyplot as plot
import plotly.graph_objects as go


#Global Variables and Inputs
poplength = 40
generations = 10000
bitlength = 24
crossover_rate = 0.4
mutation_rate = 0.04

#User input 
indicator = input("""
Select your Function: \n
    (r) Rosenbrock's Valley
    (h) Himmelblau Function
    (d) De Jong Sphere Function \n
""")

choice = int(input("""
Select your choice of optimization: \n
    (1) Natural Selection
    (2) Eliteism \n"""))

    
'''
This is the class definition for each 
Organism in the population. 
'''
class Organism:

    def __init__(self, code):
        self.code = code
        self.fitness = 0
        self.decoded = 0

    def __str__(self):

        return 'DNA Code: ' + str(self.code) + ' Fitness: ' + str(self.fitness)

'''
The Objective function takes the binary
genome and tells us how good/fit the 
genome is. 
'''
def rosenbrockvalley(x):
    xrange = range(len(x)-1)
    return sum(100 * (x[i+1] - x[i]**2)**2 + (1-x[i])**2 for i in xrange)

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def dejong(x):
    return sum(xi**2 for xi in x)

# Objective Function Auxiliary

'''
This is an objective function which splits the 
string and returns all substrings. 
input: string, int
output: list[string]
'''
def string_split(code, n):
    return [code[i:i+n] for i in range(0, len(code), n)]

'''
This is the decoder for the rosenbrockvalley 
objective function. 
input: organism class object
output: decoded genome
'''
def decoder_r(individual):
    n = int(len(individual.code)/2)
    bits_list = string_split(individual.code, n)
    #print(bits_list)


    num_signs = [(-1 if bits[0] == '0' else 1, int((float(bits))))
                  for bits in bits_list]


    x = [sign * (num % 2.048) for sign, num in num_signs]
    individual.decoded = x

    #print(x)

    if x == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]:
        print("""Found the Optimal Value \n
                 Organism: """ + str(individual.code) + '\n' 
                 "Fitness: " + str(individual.fitness) + '\n')

        print(individual.decoded)

        exit(0)

    return x
'''
This is the decoder for De jong objective 
function. 
input: Organism class object 
output: decoded genome
'''
def decoder_d(individual):
    n = int(len(individual.code)/2)
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
'''
This is the decoder for the HimmelBlau's 
Objective funtion.
input: organism class object
output: decoded genome
'''
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
'''
This gives the interval between highest and lowest
given the multiplier and steps. 
input: lowest integer, highest integer, 
multiplier integer, steps integer
output: interval integer
'''
def interval(lowest, highest, m, steps):
    step_size = (highest - lowest)/steps 
    return lowest + m*step_size

# Population Generation Methods

'''
Finds if the input probabily if greater than
the randomized.
input: floating probability
output: boolean 
'''
def chance(probability):

    return random.random() > probability
'''
Creates a random binary for the given bit
length.
input: integer bitlength
output: binary string
'''
def random_binary(bitlength):

    return ''.join('0' if chance(0.5) else '1' for _ in range(bitlength))
'''
Initializes the organism object based on 
the input genome.
input: string 
output: Organism class object
'''
def init_organism(dna):
    return Organism(dna)
'''
Generate a population of varied organisms of random
DNA sequence
input: population length int, dna length int
output: List[string]
'''
def population_generate(poplength, bitlength):

    dnalist = []

    for x in range(0, poplength):
        dnalist.append(init_organism(random_binary(bitlength)))

    return dnalist


# Genetic Algorithm Operators

'''
This function using a biased roullete chooses
which organism objects proceed into the next generation
input: List[organisms], Lambda objective function, 
int selection choice
output: List[organisms]
'''
def reproduction(organisms, OF, gen):
    
    minimum_fitness = min(OF(organism) for organism in organisms)

    def weight(organism):
        if gen == 0:
            fitness = OF(organism)
            organism.fitness = fitness
        else:
            fitness = organism.fitness
        return (fitness - minimum_fitness + 1)
        
    # Organize weights according to the total weight (Biased Roulette % of Total Calculation)
    weights = []
    weights_total = 0
    for organism in organisms:
        weights.append((organism, weight(organism)))
        weights_total += weight(organism)
    all = []
    sum_of_weights_ratio = 0
    for node,x in weights:
        all.append((node, x/weights_total))
        sum_of_weights_ratio += (x/weights_total)
    population_new = []
    for j in range(len(organisms)):
        rand = random.uniform(0,sum_of_weights_ratio) + j/10000
        total = 0
        for organism, bias in all:
            total+= bias
            if rand<=total:
                population_new.append(organism)
                break

    
    #print('\n'.join(map(str, population_new)))

    return population_new

'''
Auxillary function which splices the gene on the given
index and swaps binary code.
input: string gene1, string gene2, int index
output stiring gene1, string gene2
'''
def crossover(bin1, bin2, indice):
    node_i, node_j = bin1.code[:indice], bin1.code[indice:]
    node_i1, node_j1 = bin2.code[:indice], bin2.code[indice:]

    return node_i+node_j1, node_i1+node_j
'''
Randomly chooses a pair of binary genes within a population
and swaps binary code between the two
input: List[Organisms], float probability
output: List[Organisms]
'''
def complete_crossover(population, crossover_rate, OF):

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
            org1 = init_organism(new_x1)
            org1.fitness = OF(org1) 
            final_population.append(org1)
            org2 = init_organism(new_x2)
            org2.fitness = OF(org2)
            final_population.append(org2)

    return final_population
'''
Auxilary flips a binary bit of an organism
input: organism class object, float probability
output: string
'''
def mutation(organism, mutation_rate):
    
    flip = lambda x: '1' if x == '0' else '0'

    character = (flip(character) if chance(mutation_rate) else character for character in organism.code)

    return ''.join(character)
'''
Iterates through the list of organisms and mutates the 
binary code according to the mutation rate
input: List[organism], flat probability
output: List[organism]
'''
def population_mutation(population, mutation_rate, OF):

    for organism in population:
        if chance(mutation_rate):
            organism.code = mutation(organism, mutation_rate)
            organism.fitness = OF(organism)

    return population

#Plotting results
'''
To plot the evolution graph
input: List[float], list[float], list[float], int
output: None
'''
def plot_gen_diagram(best, worst, avg, generation):
    plot.plot(range(0,generation), best, label="min pop fitness")
    plot.plot(range(0,generation), worst, label="max pop fitness")
    plot.plot(range(0,generation),avg, label = "avg pop fitness")
    plot.legend()
    plot.title('Evolution')
    plot.xlabel('Generations')
    plot.ylabel('Fitness')
    plot.show()
    return

'''
To plot the evolution graph
input: List[organism], List[Tuple(organism,int)]
output: None
'''
def new_plot(organisms, min):
    x1 = []
    x2 = []
    fit = []

    for i in organisms:
        x1.append(i[0].decoded[0])
        x2.append(i[0].decoded[1])
        fit.append(i[0].fitness)
    
    fig = go.Figure(layout=dict(scene = dict(xaxis_title ='x1',yaxis_title ='x2',zaxis_title ='f')))

    fig.add_scatter3d(x=x1,y=x2,z=fit,mode='markers',marker=dict(color=fit))
    if(len(min) == 1):
        min = min[0][0]
        fig.add_traces(go.Scatter3d(x=[min.decoded[0]],y=[min.decoded[1]],z=[min.fitness],mode='markers',marker=dict(color='cyan')))
    else:
        min_x1 = []
        min_x2 = []
        min_fit = []

        for i in min:
            min_x1.append(i[0].decoded[0])
            min_x2.append(i[0].decoded[1])
            min_fit.append(i[0].fitness)

        fig.add_traces(go.Scatter3d(x=min_x1,y=min_x2,z=min_fit,mode='markers',marker=dict(color='cyan')))

    fig.show()
    return

'''
Controller function for the algorithm
input: None
output: None
'''
def ga():

    organisms = population_generate(poplength, bitlength)

    if indicator == 'h':
        OF = lambda code: himmelblau((decoder_h(code))[0],(decoder_h(code))[1])

    if indicator == 'r':
        OF = lambda code: rosenbrockvalley(decoder_r(code))

    if indicator == 'd':
        OF = lambda code: dejong(decoder_d(code))

    best = []
    worst = []
    avg = []
    minima = []
    for generation in range(generations):

        
        if generation != 0 and choice != 1:
            organisms.sort(key= lambda x: x.fitness)
            best.append((organisms[0],generation))
            #worst.append(organisms[len(organisms)-1].fitness)
            #avg.append(organisms[int(len(organisms)/2)].fitness)
            #best_fit = organisms.pop(0)
            #print(str(best_fit))
        elif generation != 0:
            organisms.sort(key= lambda x: x.fitness)
            best.append((organisms[0],generation))
            #worst.append(organisms[len(organisms)-1].fitness)
            #avg.append(organisms[int(len(organisms)/2)].fitness)

        print('Generation: ' + str(generation)) 
        organisms = reproduction(organisms, OF, generation)
        organisms = complete_crossover(organisms, crossover_rate, OF)
        organisms = population_mutation(organisms, mutation_rate, OF)
        
        """ 
        if generation != 0 and choice != 1:
            organisms.append(best_fit)
            """

    print("-------------------------------------")

    for i in best:
        if(len(minima) == 0):
            minima.append(i)
        elif(i[0].fitness < minima[0][0].fitness):
            minima = []
            minima.append(i)
        elif(i[0].fitness == minima[0][0].fitness):
            minima.append(i)
    #plot_gen_diagram(best, worst, avg, generation)
    for i in minima:
        print("Organism: {}   Fitness: {}  Minimum Point: {} Generation: {}".format(i[0].code,i[0].fitness,i[0].decoded,i[1]))
    new_plot(best,minima)



ga()