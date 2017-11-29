# Genetic Algorithm Approach to adjust weights in FilterStrings.py for Analyzer function
# Refer to FilterStrings.py for more info on weights.
template = [5, 40000, 10000000, 50000]
#          [open2, open3, open4, closed4]
import numpy
mutation_rate = 0.1
starting_population = 16


def generate_random_genes():
    g1 = numpy.random.normal(0.0, 1.0, 4)
    print(g1)


start_genes = []
for x in range(starting_population):
    start_genes.append(generate_random_genes())

print(start_genes)

