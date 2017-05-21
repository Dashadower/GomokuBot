size = 5
#2o`clock diagnol search from 1,1 to 13,13 in coordinate plane
"""for x in range(1, size + 1):
    for y in range(0, x):
        print(x - y, y + 1)

for y in range(2, size + 1):
    for x in range(size, y - 1, -1):
        print(x, y + (size - x))"""
# 5o`clock diagnol search from 1,13 to 13,1 in coordinate plane
for x in range(1,size+1):
    for y in range(5,size-x,-1):
        print(x-size+y,y)
        pass
    print("-----")
for y in range(1,size):
    for x in range(size,y,-1):
        #print(x,x-y)
        pass
    #print("-----")
