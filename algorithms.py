import heapq

def neighbors(grid,node):

    r,c=node

    dirs=[(1,0),(-1,0),(0,1),(0,-1)]

    result=[]

    for dr,dc in dirs:

        nr=r+dr
        nc=c+dc

        if 0<=nr<grid.rows and 0<=nc<grid.cols:

            if grid.cells[nr][nc]==0:
                result.append((nr,nc))

    return result


def reconstruct(parent,node):

    path=[node]

    while node in parent:
        node=parent[node]
        path.append(node)

    path.reverse()
    return path


def astar(grid,start,h):

    goal=grid.goal

    openlist=[]
    heapq.heappush(openlist,(0,start))

    g={start:0}

    parent={}

    visited=set()

    frontier=set([start])

    while openlist:

        f,node=heapq.heappop(openlist)

        frontier.discard(node)

        if node==goal:

            return reconstruct(parent,node),visited,frontier

        visited.add(node)

        for nb in neighbors(grid,node):

            cost=g[node]+1

            if nb not in g or cost<g[nb]:

                g[nb]=cost

                parent[nb]=node

                f=cost+h(nb,goal)

                heapq.heappush(openlist,(f,nb))

                frontier.add(nb)

    return [],visited,frontier


def greedy(grid,start,h):

    goal=grid.goal

    openlist=[]
    heapq.heappush(openlist,(0,start))

    parent={}

    visited=set()

    frontier=set([start])

    while openlist:

        f,node=heapq.heappop(openlist)

        frontier.discard(node)

        if node==goal:

            return reconstruct(parent,node),visited,frontier

        visited.add(node)

        for nb in neighbors(grid,node):

            if nb not in visited:

                parent[nb]=node

                f=h(nb,goal)

                heapq.heappush(openlist,(f,nb))

                frontier.add(nb)

    return [],visited,frontier