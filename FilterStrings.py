# -----------------------------------------
# These are threat attack patterns which are used to calculate heuristic values
# o (alphabet o) means attacker's stone
# - (dash) means empty space
# x (alphabet x) means attacker's opponent's stone
# each pattern must be 6 characters long
# -----------------------------------------
# Open3 is a threat in which all the ends of 3 repetitive stones are open
# The third and fourth are also counted as Open3
Open3 = [
    "-ooo--",
    "--ooo-",
    "-o-oo-",
    "-oo-o-"
]
# -----------------------------------------
# Open4 is a threat in which all the ends of 4 repetitive stones are open
# If the attacker does not have an Closed4 or Open4 to make into 5, Attacker is guarenteed to win next turn
Open4 = [
    "-oooo-"
]
# -----------------------------------------
# Closed4 is a threat in which one of the ends of 4 repetitive stones are open
# If the defender does not block the other, end, Attacker is guarenteed to win next turn.
Closed4 = [
    "xoooo-"
    "-oooox"
]
# -----------------------------------------
# (Reference)
# I have also added Open2 for heuristics calculation.
# However, they pose of low value, but, multiple Open2s can turn into a Open3xOpen3.
Open2 = [
    "-oo---",
    "--oo--",
    "---oo-",
    "-o-o--",
    "--o-o-",
    "--o-o-"
]