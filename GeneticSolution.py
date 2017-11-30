import numpy, os
from Analyzer import WinChecker
from main import GameBoard
from GeneticAlphaBeta import AlphaBeta
from GeneticAnalyzerOptimized import Analyzer
# Genetic Algorithm Approach to adjust weights in FilterStrings.py for Analyzer function
# Refer to FilterStrings.py for more info on weights.
template = [5, 40000, 10000000, 50000]
#          [open2, open3, open4, closed4]

mutation_rate = 0.1
starting_population = 16
default_generation_deviation = 20

game_searchrange = 1
game_playdepth = 2

def generate_random_chromosomes():
    g1 = numpy.random.normal(0.0, default_generation_deviation, 4)
    return g1.tolist()

def generate_random_gene():
    return numpy.random.normal(0.0, default_generation_deviation)

start_chromosomes = []
for x in range(starting_population):
    start_chromosomes.append(generate_random_chromosomes())


def play_game(c1, c2):
    board = GameBoard(10,10)
    refree = WinChecker(board)

    ai1 = AlphaBeta(board,"black",game_playdepth, game_searchrange,c1)
    ai2 = AlphaBeta(board, "white", game_playdepth,game_searchrange,c2)
    board.AddStone("black",(5,5))
    while True:
        if not len(ai2.GetOpenMoves(board)) == 0:
            ai2.AddAIStone(ai2.ChooseMove()[1])
            if refree.Check("white"):
                print("game finished")
                return c2
            else:
                if not len(ai1.GetOpenMoves(board)) == 0:
                    ai1.AddAIStone(ai1.ChooseMove()[1])
                    if refree.Check("black"):
                        print("game finished")
                        return c1
                else:
                    print("tie")
                    return play_game(c1, c2)
        else:
            print("tie")
            return play_game(c1, c2)

logfile = open("GA results.txt","a")
logfile.write("NEW INIT ------------------\n")
def multiinput(msg):
    print(msg)
    logfile.write(str(msg)+"\n")
    logfile.flush()
generation = 1
multiinput("START GENES:")
multiinput(start_chromosomes)

while True:
    multiinput("****************")
    multiinput("GENERATION "+str(generation))
    evaluated_chromosomes = []
    for x in range(0, int(starting_population/2)):
        first_chromosome = start_chromosomes[x*2]
        second_chromosome = start_chromosomes[x*2+1]
        result = play_game(first_chromosome,second_chromosome)
        evaluated_chromosomes.append(result)
        multiinput("%d of %d sets done simulationg"%(x+1, int(starting_population/2)))
    for x in range(0, int(len(evaluated_chromosomes)/2)):
        first_chromosome = evaluated_chromosomes[x * 2]
        second_chromosome = evaluated_chromosomes[x * 2 + 1]
        crossover_policy = []
        for x in range(4):
            crossover_policy.append(numpy.random.choice([0,1]))

        new_chromosome = []
        gene_index = 0
        for item in crossover_policy:
            mrate = numpy.random.randint(1,mutation_rate+1)
            if mrate == 5:
                new_chromosome.append(generate_random_gene())
            else:
                if item == 0:
                    new_chromosome.append(first_chromosome[gene_index])
                elif item == 1:
                    new_chromosome.append(second_chromosome[gene_index])
                gene_index += 1
        evaluated_chromosomes.append(new_chromosome)
        start_chromosomes = evaluated_chromosomes
        generation += 1





