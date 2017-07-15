from main import GameBoard
import time,random,timeit
import cProfile

def random_number():
    return random.randint(1,99999)
def random_matrix(board):

    randoms = []
    for x in range(0,board.size[0]):
        randoms.append([])
        for y in range(0,board.size[1]):

            rarr = [random_number(),random_number(),random_number()]
            randoms[x].append(rarr)
    randoms.insert(len(randoms),[random_number(),random_number()])
    return randoms
def Zobrist_Hash(board,matrix):
    board_hash = 0
    for x in range(1,board.size[0]+1):
        for y in range(1,board.size[1]+1):
            if (x,y) in board.BlackStones:
                piece = 1
            elif (x,y) in board.WhiteStones:
                piece = 2
            else:
                piece = 0
            board_hash ^= matrix[x-1][y-1][piece]

    if board.turn == "black":
        board_hash ^= matrix[len(matrix)-1][0]
    elif board.turn == "white":
        board_hash ^= matrix[len(matrix)-1][1]
    return board_hash

if __name__ == "__main__":
    #from Tester import RandomPopulate


    board = GameBoard(2,2)


    board.AddStone("black", (6, 6))
    board.AddStone("black", (6, 7))




    #RandomPopulate(board)
    print("Black:", board.BlackStones)
    print("White:", board.WhiteStones)
    random_matrix = random_matrix(board)
    #heuristics = Analyzer(board,debug=True)
    starttime = time.time()
    print(Zobrist_Hash(board,random_matrix))
    print(Zobrist_Hash(board, random_matrix))
    #refree = WinChecker(board)
    #print(refree.CheckBoth())
    endtime = time.time()
    board = GameBoard(2,2)
    board.AddStone("white",(6,6))
    board.AddStone("white",(6,6))
    print(Zobrist_Hash(board, random_matrix))
    print("Total calculation time:", endtime-starttime if not endtime-starttime == 0.0 else "0.0 (<0.0001 seconds)")
    print(starttime,endtime)


