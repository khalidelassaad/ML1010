class Board:
    #WHEN REFERENCING GRID:
    #grid[x][y] (x is row, y is column). (0,0) is top left)
    colormode = True #SET THIS TO FALSE IF WINDOWS USER
    def __init__(self):
        self.grid = []
        for x in range(10):
            self.grid.append([0]*10)

    def fill_count(self):
        c = 0
        for x in range(10):
            for y in range(10):
                c += self.grid[x][y]
        return c

    def copy(self, source):
        for x in range(10):
            for y in range(10):
                self.grid[x][y] = source.grid[x][y]

    def check_place(self, point, shape):
        for block in shape.blocks:
            row = point[0]+block[0]
            col = point[1]+block[1]
            if (
                    row > 9 or
                    col > 9 or
                    row < 0 or
                    col < 0 or
                    self.grid[row][col]
                    ):
                return False
        return True
                

    def place(self, point, shape):
        if not self.check_place(point,shape):
            raise Exception("Tried to place in an invalid location") 
        for block in shape.blocks:
            self.grid[point[0]+block[0]][point[1]+block[1]] = 1

    def make_move(self, move):
        self.place((move.row,move.col),move.shape)

    def is_color(self, move, x, y):
        if not move:
            return False
        return ((x - move.row),(y - move.col)) in move.shape.blocks


    def draw(self, move = None):
        clearcolor = "\033[92m"
        maincolor = "\033[91m"
        endcolor = "\033[0m"
        print("  0 1 2 3 4 5 6 7 8 9")
        for x in range(10):
            print(x, end=" ")
            for y in range(10):
                if self.grid[x][y] and self.is_color(move, x, y) and Board.colormode:
                    print(maincolor+"#"+endcolor, end = " ")
                elif self.grid[x][y]:
                    print("#",end=" ")
                elif not self.grid[x][y] and self.is_color(move, x, y) and Board.colormode:
                    print(clearcolor+"o"+endcolor, end = " ")
                else:
                    print(".",end=" ")
            print()
    
    def clear(self):
        self.grid = []
        self.__init__()

    def clear10(self):
        rows = []
        cols = []
        clears = 0
        for x in range(10):
            if self.grid[x] == [1]*10:
                rows.append(x)
            colsum = 0
            for y in range(10):
                colsum += self.grid[y][x]
            if colsum ==10:
                cols.append(x)
        for x in range(len(rows)+len(cols)):
            clears+=(x+1)*10
        for row in rows:
            for x in range(10):
                if self.grid[row][x]:
                    self.grid[row][x] = 0
        for col in cols:
            for x in range(10):
                if self.grid[x][col]:
                    self.grid[x][col] = 0
        return clears