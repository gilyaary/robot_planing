import numpy as np

class Node:
    children = []
    def __init__(self, parent, location):
        self.parent = parent
        self.location = location
        self.id = str(location)
        self.distance = 0
        if parent != None:
            self.path = parent.path + '.' + self.id
            self.distance = parent.distance + 1
            parent.children.append(self)
        else:
            self.path = self.id

class PathPlanner:
    
    def __init__(self, board, start, goal):
        #print("init")
        self.board = board
        self.start_point = start
        self.goal = goal
        self.root = Node(None, (0,0))
        
    def find_best_path(self):
        #print('find best path')
        current_leaves = []
        all_nodes = {}
        current_leaves.append(self.root)
        all_nodes[self.root.id] = self.root
        self._find_best_path(current_leaves, all_nodes)
    
    def _find_best_path(self, current_leaves, all_nodes):
        next_level_leaves = []
        for node in current_leaves:
            #check for empty cells
            #create a node if not occupied
            #check for short circuit
            #check for shorter path
            if node.location == self.goal:
                print('reached goal: ' + node.path)
                continue

            neighbors = self.get_neighbors(node)
            for n in neighbors:
                x,y = n
                #print(x,y)
                if self.board[x,y] != 1:
                    child = Node(node, (x,y))
                    if child.id in all_nodes:
                        #trim one of the trees
                        current_distance = child.distance
                        other_distance = all_nodes[child.id].distance
                        #this will not be true here because shorter paths are encountered earlier
                        if current_distance < other_distance:
                            print('short circuit')
                    else:
                        #print('adding child at ', child.location)
                        all_nodes[child.id] = child
                        next_level_leaves.append(child)
                        #print(child.path)
                
        if len(next_level_leaves) > 0 :
            self._find_best_path(next_level_leaves, all_nodes)

    def get_neighbors(self, node):
        x,y = node.location
        neighbors = []
        xx = []
        yy = []
        xx.append(x)
        yy.append(y)
        if x > 0:
            xx.append(x - 1)
        if y > 0:
            yy.append(y - 1)
        if x < len(self.board) - 1:
            xx.append(x + 1)
        if y < len(self.board) - 1:
            yy.append(y + 1)
        for i in xx:
            for j in yy:
                neighbors.append((i,j))
        #print(neighbors)
        return neighbors

# def __main_():
#     board = np.zeros((1000,1000))
#     board[400:600,400:600] = 1
#     board[100:200,100:200] = 1
#     board[800:900,800:900] = 1
#     board[100:200,800:900] = 1
#     board[800:900,100:200] = 1
#     start = (0,0)
#     goal = (999,999)
#     pp = PathPlanner(board, start, goal)
#     #pp.set_obstacle()
#     pp.find_best_path()

# def __main_():
#     board = np.zeros((10,10))
#     board[3:7,3:7] = 1
#     board[1:2,1:2] = 1
#     board[8:9,8:9] = 1
#     board[1:2,8:9] = 1
#     board[8:9,1:2] = 1
#     start = (0,0)
#     goal = (9,9)
#     pp = PathPlanner(board, start, goal)
#     #pp.set_obstacle()
#     pp.find_best_path()

def __main_():
    board = np.zeros((100,100))
    board[30:70,30:70] = 1
    board[10:20,10:20] = 1
    board[80:90,80:90] = 1
    board[10:20,80:90] = 1
    board[80:90,10:20] = 1
    start = (0,0)
    goal = (99,99)
    pp = PathPlanner(board, start, goal)
    #pp.set_obstacle()
    pp.find_best_path()


__main_()
    
