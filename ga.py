import random
from rosen import rosenbrockvalley

population = 20
generations = 10000

class Agent:

    def __init__(self, length):

        self.binary = (random.choice(dnageneration) for _ in range(length))
        self.fitness = 0

    def __str__(self):

        return 'String: ' + str(self.binary) + ' Fitness: ' + str(self.fitness)
    
    
def dnageneration():

    codes = []
    for num in range (0, generations):
        codes.append(str(bin(num))[2:])

    return codes


def ga():

    agents = init_agents(population)

    for generation in range(generations):
        print('Generation: ' + str(generation)) 

        agents = fitness(agents)

        if any(agent.fitness >= maximum for agent in agents):

            print('Function has reached its maximum/minimum value.')
            exit(0)


def init_agents(population, length):


    return [Agent(length) for x in range(population)]


def fitness(agents):

    for agent in agents:

        agent.fitness = rosenbrockvalley(i,j)
 
ga()
