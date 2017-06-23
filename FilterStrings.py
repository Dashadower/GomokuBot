# -----------------------------------------
# These are threat attack patterns which are used to calculate heuristic values
# o (alphabet o) means attacker's stone
# - (dash) means empty space
# x (alphabet x) means attacker's opponent's stone
# each pattern must be 6 characters long
# -----------------------------------------
# (Reference)
# I have also added Open2 for heuristics calculation.
# They pose of low value, but, multiple Open2s can turn into a Open3xOpen3.
# Also, Open2s can make better decisions in the opening, where making as many threats as possible is good.
Open2 = [
    "-oo---",
    "--oo--",
    "---oo-",
    "-o-o--",
    "--o-o-",
    "--o-o-"
]
Open2Val = 5
# -----------------------------------------
# Open3 is a threat in which all the ends of 3 repetitive stones are open
# The third and fourth are also counted as Open3
Open3 = [
    "-ooo--",
    "--ooo-",
    "-o-oo-",
    "-oo-o-",
    "x-ooo-"
]
Open3Val = 5000
# -----------------------------------------
# Open4 is a threat in which all the ends of 4 repetitive stones are open
# If the attacker does not have an Closed4 or Open4 to make into 5 immediately, Attacker is guarenteed to win next turn
Open4 = [
    "-oooo-"
]
Open4Val = 90000000
# -----------------------------------------
# Open5 is a win condition.
Open5 = [
    "xooooo",
    #"ooooox", # the algorithm will not count this as a 5 win , because it is not possible
    "-ooooo",
    #"ooooo-", # same as above
]
Open5Val = 100000000
# -----------------------------------------
# Closed4 is a threat in which one of the ends of 4 repetitive stones are open
# If the defender does not block the other end, Attacker is guaranteed to win next turn.
Closed4 = [
    "xoooo-",
    "-oooox",
    "xoo-oo",
]
Closed4Val = 5000