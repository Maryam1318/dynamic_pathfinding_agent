import tkinter as tk
import time
import random

from algorithms import astar, greedy
from hueristics import manhattan, euclidean
from grid import Grid

CELL_SIZE = 25

class PathfindingGUI:

    def __init__(self, root):

        self.root = root
        root.title("Dynamic Pathfinding Agent")
        root.configure(bg="#2b2b2b")

        # Visualization sets
        self.frontier=set()
        self.visited=set()
        self.path=set()

        # Variables
        self.rows=tk.IntVar(value=20)
        self.cols=tk.IntVar(value=20)

        self.algorithm=tk.StringVar(value="A*")
        self.heuristic=tk.StringVar(value="Manhattan")
        self.dynamic=tk.BooleanVar()

        # LEFT PANEL
        left=tk.Frame(root,bg="#3a3a3a",padx=10,pady=10)
        left.pack(side="left",fill="y")

        tk.Label(left,text="PATHFINDING AGENT",
                 font=("Arial",14,"bold"),
                 bg="#3a3a3a",
                 fg="white").pack(pady=10)

        tk.Label(left,text="Grid Size",
                 bg="#3a3a3a",
                 fg="white").pack()

        tk.Entry(left,textvariable=self.rows,width=8).pack(pady=3)
        tk.Entry(left,textvariable=self.cols,width=8).pack(pady=3)

        tk.Label(left,text="Algorithm",
                 bg="#3a3a3a",
                 fg="white").pack(pady=5)

        tk.OptionMenu(left,self.algorithm,"A*","Greedy").pack()

        tk.Label(left,text="Heuristic",
                 bg="#3a3a3a",
                 fg="white").pack(pady=5)

        tk.OptionMenu(left,self.heuristic,"Manhattan","Euclidean").pack()

        tk.Checkbutton(left,
                       text="Dynamic Mode",
                       variable=self.dynamic,
                       bg="#3a3a3a",
                       fg="white",
                       selectcolor="#3a3a3a").pack(pady=10)

        tk.Button(left,
                  text="Generate Maze",
                  width=18,
                  bg="#4CAF50",
                  fg="white",
                  command=self.generate_maze).pack(pady=5)

        tk.Button(left,
                  text="Start Search",
                  width=18,
                  bg="#2196F3",
                  fg="white",
                  command=self.start_search).pack(pady=5)

        tk.Button(left,
                  text="Reset Grid",
                  width=18,
                  bg="#f44336",
                  fg="white",
                  command=self.reset).pack(pady=5)

        # METRICS PANEL

        tk.Label(left,text="METRICS",
                 font=("Arial",12,"bold"),
                 bg="#3a3a3a",
                 fg="white").pack(pady=10)

        self.nodes_label=tk.Label(left,
                                  text="Nodes Visited: 0",
                                  bg="#3a3a3a",
                                  fg="white")

        self.nodes_label.pack()

        self.cost_label=tk.Label(left,
                                 text="Path Cost: 0",
                                 bg="#3a3a3a",
                                 fg="white")

        self.cost_label.pack()

        self.time_label=tk.Label(left,
                                 text="Time(ms): 0",
                                 bg="#3a3a3a",
                                 fg="white")

        self.time_label.pack()


        # RIGHT PANEL (GRID)

        self.canvas=tk.Canvas(root,
                              bg="white",
                              highlightthickness=0)

        self.canvas.pack(side="right")

        self.frontier=set()
        self.visited=set()
        self.path=set()


        self.reset()


    def reset(self):

        self.grid=Grid(self.rows.get(),self.cols.get())

        w=self.cols.get()*CELL_SIZE
        h=self.rows.get()*CELL_SIZE

        self.canvas.config(width=w,height=h)

        self.frontier=set()
        self.visited=set()
        self.path=set()

        self.draw()


    def generate_maze(self):

        self.grid.random_maze(0.3)
        self.draw()


    def draw(self):

        self.canvas.delete("all")

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):

                x1=c*CELL_SIZE
                y1=r*CELL_SIZE

                x2=x1+CELL_SIZE
                y2=y1+CELL_SIZE

                color="#ffffff"

                if (r,c)==self.grid.start:
                    color="#00bcd4"

                elif (r,c)==self.grid.goal:
                    color="#9c27b0"

                elif self.grid.cells[r][c]==1:
                    color="#222222"

                elif (r,c) in self.frontier:
                    color="#FFD54F"

                elif (r,c) in self.visited:
                    color="#EF5350"

                elif (r,c) in self.path:
                    color="#66BB6A"

                self.canvas.create_rectangle(
                    x1,y1,x2,y2,
                    fill=color,
                    outline="#cccccc")

        self.canvas.bind("<Button-1>",self.click)


    def click(self,event):

        r=event.y//CELL_SIZE
        c=event.x//CELL_SIZE

        if (r,c)!=self.grid.start and (r,c)!=self.grid.goal:

            self.grid.cells[r][c]^=1

        self.draw()


    def get_heuristic(self):

        if self.heuristic.get()=="Manhattan":
            return manhattan
        return euclidean


    def search_once(self,start):

        h=self.get_heuristic()

        t1=time.time()

        if self.algorithm.get()=="A*":
            path,visited,frontier=astar(self.grid,start,h)
        else:
            path,visited,frontier=greedy(self.grid,start,h)

        t2=time.time()

        self.nodes_label.config(text=f"Nodes Visited: {len(visited)}")
        self.cost_label.config(text=f"Path Cost: {len(path)}")
        self.time_label.config(text=f"Time(ms): {(t2-t1)*1000:.2f}")

        return path,visited,frontier


    def dynamic_step(self,pos):

        if random.random()<0.05:

            r=random.randint(0,self.grid.rows-1)
            c=random.randint(0,self.grid.cols-1)

            if (r,c)!=self.grid.goal and (r,c)!=pos:

                self.grid.cells[r][c]=1
                return (r,c)

        return None


    def start_search(self):

        pos=self.grid.start

        while pos!=self.grid.goal:

            path,visited,frontier=self.search_once(pos)

            if not path:
                print("No Path")
                return

            self.path=set(path)
            self.visited=set(visited)
            self.frontier=set(frontier)

            self.draw()
            self.root.update()

            for step in path[1:]:

                pos=step

                new_obstacle=None

                if self.dynamic.get():
                    new_obstacle=self.dynamic_step(pos)

                if new_obstacle and new_obstacle in path:
                    break

                self.draw()
                self.root.update()

                time.sleep(0.05)



root=tk.Tk()
PathfindingGUI(root)
root.mainloop()