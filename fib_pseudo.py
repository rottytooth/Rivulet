lists = [] 

def glyph1():
    global lists
    lists = [
    [0,  # fibonacci number
    1,   # number in waiting
    0,   # how many we've calculated
    10  # how many we'll calcuate
    ],[] # stack 1: output
    ,[0]  # stack 2: another temporary storage
]

def glyph2():
    global lists

    while(True):

        stack_bckup = lists.copy()

        lists[2][0] = lists[0][0]
        lists[0][0] += lists[0][1]
        lists[0][1] = lists[2][0]
        lists[0][2] += 1
        lists[1].append(lists[0][0])

        lists[2][1] = lists[0][3]
        lists[2][1] -= lists[0][2]
        # this is the revert
        if lists[2][1] <= 0:
            # set lists back to their previous condition
            lists = stack_bckup
            return

def glyph3():
    global lists
    print(lists[1])

glyph1()
glyph2()
glyph3()
