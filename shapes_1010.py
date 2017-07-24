class Shape:
    #A shape has a set of 2 tuples that indicate
    #where the other blocks in that shape are on the grid, relative to
    #the (0,0) rootblock (top left corner of that shape's area
    def __init__(self):
        self.blocks = []
        self.namestring = ""
    def append(self, point):
        self.blocks.append(point)
    def __str__(self):
        return self.namestring
    def __repr__(self):
        return self.__str__()
    def multistr(self):
        min_row = min(self.blocks, key = lambda x: x[0])[0]
        max_row = max(self.blocks, key = lambda x: x[0])[0]
        min_col = min(self.blocks, key = lambda x: x[1])[1]
        max_col = max(self.blocks, key = lambda x: x[1])[1]
        row_mod = 2 - ((min_row + max_row) // 2)
        col_mod = 2 - ((min_col + max_col) // 2)
        returnlist = []
        for x in range(5):
            returnlist.append([" "]*5)
        for block in self.blocks:
            row = block[0] + row_mod
            col = block[1] + col_mod
            returnlist[row][col] = "#"
        for x in range(len(returnlist)):
            returnlist[x] = "".join(returnlist[x])
        return returnlist

def print_round(shapes):
    printlist = ["   "]*5
    for shape in shapes:
        multi = shape.multistr()
        for row in range(len(multi)):
            printlist[row] = printlist[row] + multi[row] + " "
    for line in printlist:
        print(line)
    return

tall_5  = Shape()
tall_5.append((0,0))
tall_5.append((1,0))
tall_5.append((2,0))
tall_5.append((3,0))
tall_5.append((4,0))
tall_5.namestring="Tall 5"

wide_5  = Shape()
wide_5.append((0,0))
wide_5.append((0,1))
wide_5.append((0,2))
wide_5.append((0,3))
wide_5.append((0,4))
wide_5.namestring="Wide 5"

tall_4  = Shape()
tall_4.append((0,0))
tall_4.append((1,0))
tall_4.append((2,0))
tall_4.append((3,0))
tall_4.namestring="Tall 4"

wide_4  = Shape()
wide_4.append((0,0))
wide_4.append((0,1))
wide_4.append((0,2))
wide_4.append((0,3))
wide_4.namestring="Wide 4"

tall_3  = Shape()
tall_3.append((0,0))
tall_3.append((1,0))
tall_3.append((2,0))
tall_3.namestring="Tall 3"

wide_3  = Shape()
wide_3.append((0,0))
wide_3.append((0,1))
wide_3.append((0,2))
wide_3.namestring="Wide 3"

tall_2  = Shape()
tall_2.append((0,0))
tall_2.append((1,0))
tall_2.namestring="Tall 2"

wide_2  = Shape()
wide_2.append((0,0))
wide_2.append((0,1))
wide_2.namestring="Wide 2"

square1 = Shape()
square1.append((0,0))
square1.namestring="1x1 Square"

square2 = Shape()
square2.append((0,0))
square2.append((0,1))
square2.append((1,0))
square2.append((1,1))
square2.namestring="2x2 Square"

square3 = Shape()
square3.append((0,0))
square3.append((0,1))
square3.append((1,0))
square3.append((1,1))
square3.append((0,2))
square3.append((1,2))
square3.append((2,2))
square3.append((2,1))
square3.append((2,0))
square3.namestring="3x3 Square"

L_UL_2  = Shape()
L_UL_2.append((0,0))
L_UL_2.append((0,1))
L_UL_2.append((1,0))
L_UL_2.namestring="2x2 L (UL Corner)"

L_DL_2  = Shape()
L_DL_2.append((0,0))
L_DL_2.append((1,1))
L_DL_2.append((1,0))
L_DL_2.namestring="2x2 L (DL Corner)"

L_UR_2  = Shape()
L_UR_2.append((0,0))
L_UR_2.append((1,1))
L_UR_2.append((0,1))
L_UR_2.namestring="2x2 L (UR Corner)"

L_DR_2  = Shape()
L_DR_2.append((0,0))
L_DR_2.append((0,1))
L_DR_2.append((-1,1))
L_DR_2.namestring="2x2 L (DR Corner)"

L_UL_3  = Shape()
L_UL_3.append((0,0))
L_UL_3.append((0,1))
L_UL_3.append((0,2))
L_UL_3.append((1,0))
L_UL_3.append((2,0))
L_UL_3.namestring="3x3 L (UL Corner)"

L_DL_3  = Shape()
L_DL_3.append((0,0))
L_DL_3.append((2,1))
L_DL_3.append((2,2))
L_DL_3.append((1,0))
L_DL_3.append((2,0))
L_DL_3.namestring="3x3 L (DL Corner)"

L_UR_3  = Shape()
L_UR_3.append((0,0))
L_UR_3.append((0,1))
L_UR_3.append((0,2))
L_UR_3.append((1,2))
L_UR_3.append((2,2))
L_UR_3.namestring="3x3 L (UR Corner)"

L_DR_3  = Shape()
L_DR_3.append((0,0))
L_DR_3.append((0,1))
L_DR_3.append((0,2))
L_DR_3.append((-1,2))
L_DR_3.append((-2,2))
L_DR_3.namestring="3x3 L (DR Corner)"

SHAPES  = [
        tall_5,
        wide_5,
        tall_4,
        wide_4,
        tall_3,
        wide_3,
        tall_2,
        wide_2,
        square1,
        square2,
        square3,
        L_UL_2,
        L_DL_2,
        L_UR_2,
        L_DR_2,
        L_UL_3,
        L_DL_3,
        L_UR_3,
        L_DR_3]

if __name__ == "__main__":
    print_round(tall_5, wide_5, square3, L_DR_3)
