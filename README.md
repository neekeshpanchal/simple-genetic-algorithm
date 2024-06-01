# simple-genetic-algorithm
# Project Report: Implementation of a Simple Genetic Algorithm

### Objectives
The primary goal of this project was to successfully create and implement a simple genetic algorithm to efficiently optimize the benchmark objective functions (OFs) provided. The three benchmark OFs included are:

- De Jong Sphere Function
- Rosenbrock's Valley
- Himmelblau's Function

### Introduction
A Simple Genetic Algorithm (GA) follows the steps of selection, crossover, and mutation to simulate Darwin's Theory of Evolution. This algorithm evaluates the fitness of each member of a population and assigns a specific probability to determine whether or not a member will influence the genetic code of the next generation.

### Benchmark Objective Functions
- **De Jong Sphere Function (Easy)**
- **Himmelblau's Function (Medium)**
- **Rosenbrock's Valley (Hard)**

### Procedure
We implemented three chronological phases of the Simple Genetic Algorithm:

1. **Selection (or Reproduction):** This step takes the previous population of organisms and produces a new population genetically influenced by the previous generation through a biased roulette.
2. **Crossover:** The output of the selection step is combined based on chance, creating new organisms in the population (Crossover Rate, CR=0.45). This step is also referred to as the 'breeding' step.
3. **Mutation:** The final step takes the output of the crossover phase and introduces minimal genetic alterations based on a declared mutation rate (Mutation Rate, MR=0.045).

### Optimizations
To efficiently reach optimal solutions, we applied two methods of optimization:

- **Natural Selection:** Assigns a probability to each organism based on its fitness.
- **Elitism:** Similar to natural selection but guarantees the highest fitness member will influence the next generation.

### Objective Function Formulae

#### De Jong Sphere Function
\[ f(x) = \sum_{i=1}^n x_i^2 \]

#### Himmelblau's Function
\[ f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2 \]

#### Rosenbrock's Valley
\[ f(x, y) = (a - x)^2 + b(y - x^2)^2 \]

### Results
The three-dimensional visualizations of each function depict the minimal points, implying that our simple genetic algorithm efficiently reached optimal points within the confines of this demonstration.

---


Physics and Computer Science Department, Wilfrid Laurier University, Fall 2022 Term

### DNA and Fitness Examples
| Function       | DNA Sequence                   | Fitness      |
|----------------|--------------------------------|--------------|
| De Jong Sphere | 001001001001000000000000       | 0.0015999... |
| Himmelblau's   | 111000000101101111110110       | 0.0061543... |
| Rosenbrock's   | 110010100010110011101011       | 0.0018550... |
