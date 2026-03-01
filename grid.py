import random

class Grid:

    def __init__(self,rows,cols):

        self.rows=rows
        self.cols=cols

        self.cells=[[0]*cols for _ in range(rows)]

        self.start=(0,0)
        self.goal=(rows-1,cols-1)


    def random_maze(self,density):

        for r in range(self.rows):
            for c in range(self.cols):

                if (r,c)!=self.start and (r,c)!=self.goal:

                    if random.random()<density:
                        self.cells[r][c]=1
                    else:
                        self.cells[r][c]=0