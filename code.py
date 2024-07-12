

#'1' is solid coin '0' is transparent coin

import random
SIDE = 8  #size of the grid
ACTIONS = ["up", "down", "left", "right"]
from copy import deepcopy
class State:
    def __init__(self):
        self.grid = [[None for _ in range(SIDE)] for _ in range(SIDE)]
        self.A = 'A' #player A
        self.B = 'B' #player B
        self.countA = 0 #score of A
        self.countB = 0 #score of B
        self.posA = 0 #position of A
        self.posB = 0 #position of B
        self.streakA = 0 #streak of A (consecutive coin)
        self.streakB = 0 #streak of B (consecutive coin)
        self.old_coinA = -1 #old coin where A passed
        self.og_posA = -1 #position where A moved from
        self.old_coinB = -1 #old coin where B passed
        self.og_posB = -1 #position where B moved from
    def start(self):
        #set starting position for each player
        self.grid[0][0] = self.A  
        self.grid[SIDE - 1][SIDE - 1] = self.B  
        self.posA = (0, 0)
        self.posB = (SIDE - 1, SIDE - 1)
        for i in range(SIDE):
            for j in range(SIDE):
                if (i, j) != self.posA and (i, j) != self.posB:  #exclude positions of A and B
                    if random.randint(0, 1) == 1:
                        self.grid[i][j] = '1'  #place solid coin randomly

    def update_map(self, p): 
        if p == "a":
            if self.og_posA != -1 or self.old_coinA != -1:
                self.grid[self.og_posA[0]][self.og_posA[1]] = self.old_coinA
                if self.old_coinA == '1':
                    self.grid[self.og_posA[0]][self.og_posA[1]] = None
                elif self.old_coinA == 'A':
                    self.grid[self.og_posA[0]][self.og_posA[1]] = None
                else:
                    self.grid[self.og_posA[0]][self.og_posA[1]] = self.old_coinA
        elif p == "b":
            if self.og_posB != -1 or self.old_coinB != -1:
                self.grid[self.og_posB[0]][self.og_posB[1]] = self.old_coinB
                if self.old_coinB == '1':
                    self.grid[self.og_posB[0]][self.og_posB[1]] = None
                elif self.old_coinB == 'B':
                    self.grid[self.og_posA[0]][self.og_posA[1]] = None
                else:
                    self.grid[self.og_posB[0]][self.og_posB[1]] = self.old_coinB

    def show_state(self):
        #state print
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if (i, j) == self.posA:
                    print('A', end=' ')
                elif (i, j) == self.posB:
                    print('B', end=' ')
                elif cell:
                    print(cell, end=' ')
                else:
                    print('-', end=' ')
            print()
        print("Score of Player A:", self.countA)
        print("Streak of Player A:", self.streakA)
        print("Score of Player B:", self.countB)
        print("Streak of Player B:", self.streakB)
        print()


    def move(self, player, direction):
        self.grid[0][0] = None
        self.grid[SIDE - 1][SIDE - 1] = None
        #check player
        if player == self.A:
            pos = self.posA
            player_streak = self.streakA
        elif player == self.B:
            pos = self.posB
            player_streak = self.streakB
        else:
            return "Invalid player"
        #setting newpos according to direction
        if direction == "up":
            newpos = (pos[0] - 1, pos[1])
        elif direction == "down":
            newpos = (pos[0] + 1, pos[1])
        elif direction == "left":
            newpos = (pos[0], pos[1] - 1)
        elif direction == "right":
            newpos = (pos[0], pos[1] + 1)
        else:
            return "Invalid direction"
        #check if newpos stills on the board
        if 0 <= newpos[0] < SIDE and 0 <= newpos[1] < SIDE:
            self.update_score(pos,newpos,player)
            #update player's position
            pos = newpos
            
        else:
            return "Invalid: move out of bounds"

        #update player's streak and position
        if player == self.A:
            self.posA = pos
            self.streakA = player_streak
        elif player == self.B:
            self.posB = pos
            self.streakB = player_streak

        return f"Player {player} moved {direction}"
       
    def update_score(self, pos, newpos, player):
        x, y = pos
        newx, newy = newpos
        
        #check if the new position is still on the board
        if 0 <= newx < SIDE and 0 <= newy < SIDE:
            #check if the new position is a solid coin
            if self.grid[newx][newy] == '1':
                #increment the score + remove coin
                if player == self.A:
                    self.countA += 1
                    self.streakA += 1
                    if self.streakA > 1:
                        self.countA += 1
                        print('!!!Bonus Added!!!')
                    print("Score of Player A:", self.countA)
                elif player == self.B:
                    self.countB += 1
                    self.streakB += 1
                    if self.streakB > 1:
                        self.countB += 1
                        print('!!!Bonus Added!!!')
                    print("Score of Player B:", self.countB)
                self.grid[newx][newy] = None  #remove the collected coin 
            coin_update(self)  #update grid
        else:
            print("New position out of grid boundaries.")

def fitness(state, path, pos):
    #check player
    if pos == state.posA:
        score = state.countA
        streak = state.streakA
        
    else:
        score = state.countB
        streak = state.streakB
    
    initial_streak = streak
    #assigned newpos according to direction
    x, y = pos
    for direction in path:
        if direction == "up":
            newpos = (pos[0] - 1, pos[1])
        elif direction == "down":
            newpos = (pos[0] + 1, pos[1])
        elif direction == "left":
            newpos = (pos[0], pos[1] - 1)
        elif direction == "right":
            newpos = (pos[0], pos[1] + 1)
        else:
            return "Invalid direction"

        if state.grid[x][y] in ['1', '0']:
            #find the possible outcomes of picking up a coin
            score_without_pickup = score 
            score_with_pickup = score + 10
            streak_with_pickup = streak + 1

            #calculate the chance of coin status changing
            if state.grid[x][y] == '1':
                chance_of_change = 0.5  #50% chance of changing
            else:
                chance_of_change = 0.5  #50% chance for changing

            #update the score considering the chance
            score = score_without_pickup * (1 - chance_of_change) + score_with_pickup * chance_of_change
            streak = streak_with_pickup if score_with_pickup > score_without_pickup else 0
        else:
            score_without_pickup = score
            score_with_pickup = score
            streak_with_pickup = 0

            score = score_with_pickup
            streak = streak_with_pickup
        #check if move is valid
        if 0 <= newpos[0] < SIDE and 0 <= newpos[1] < SIDE:
            x, y = newpos
        else:
            return 0  #retrurn 0 for invalid move 
    

    return score


def is_goal_reached(state):
    for row in state.grid:
        for cell in row:
            if cell == '1' or cell == '0':  #'1' is solid coin '0' is transparent coin
                return False  #if any coin remains on the grid, the goal is not reached
    return True  #no coin remains on the grid, the goal is reached

def ga(state, player, pop_size=20, gen=30, moves_per_path=10):
    #check player
    if player == state.A:
        player_pos = state.posA
    else:
        player_pos = state.posB
    #random population 
    def random_population(state, player_pos, pop_size, moves_per_path):
        population = []

        for _ in range(pop_size):
            path = []
            pos = player_pos
            for _ in range(moves_per_path):
                #check potential moves
                potential_moves = []
                for direction in ['up', 'down', 'left', 'right']:
                    newpos = pos
                    if direction == "up":
                        newpos = (pos[0] - 1, pos[1])
                    elif direction == "down":
                        newpos = (pos[0] + 1, pos[1])
                    elif direction == "left":
                        newpos = (pos[0], pos[1] - 1)
                    elif direction == "right":
                        newpos = (pos[0], pos[1] + 1)

                    if 0 <= newpos[0] < len(state.grid) and 0 <= newpos[1] < len(state.grid[0]):
                        potential_moves.append((direction, newpos))  #verify that potential move is still on grid/board

                #choose move that can go to solid coin
                if potential_moves:
                    coin_moves = [move[0] for move in potential_moves if state.grid[move[1][0]][move[1][1]] == '1']
                    if coin_moves:
                        move, newpos = random.choice(potential_moves)  #else choose randomly
                        path.append(move)
                        pos = newpos
                    else:
                        move, newpos = random.choice(potential_moves)  #else choose randomly from all potential moves
                        path.append(move)
                        pos = newpos
                else:
                    break  #no valid move case
            population.append(path)
        return population


    def select_population(population): #plugs paths in fitness to find paths with best score
        fitnesses = [fitness(state, path, player_pos) for path in population] 
        return sorted(population, key=lambda path: fitness(state, path, player_pos), reverse=True)[:pop_size]

    def crossover(path1, path2): #crossover paths at raondom point
        crossover_point = random.randint(1, min(len(path1), len(path2)) - 1)
        child = path1[:crossover_point] + path2[crossover_point:]
        return child

    def mutate(path, mutation_rate=0.01): #mutate paths 
        mutated_path = []
        for move in path:
            if random.random() < mutation_rate:
                mutated_path.append(random.choice(['up', 'down', 'left', 'right']))
            else:
                mutated_path.append(move)
        return mutated_path

    population = random_population(state,player_pos,20,10)

    for _ in range(gen):
        population = select_population(population)
        new_population = []
        while len(new_population) < pop_size:
            path1, path2 = random.sample(population, 2)
            child = crossover(path1, path2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
        #from all child gen and population, select paths giving best fitness score

    best_path = max(population, key=lambda x: fitness(state, x, player_pos))
    return best_path

def coin_update(state): #random coin
    for i in range(SIDE):
        for j in range(SIDE):
            if state.grid[i][j] == '1':  #solid can change to transparent with 50% chance
                if random.randint(0, 1) == 1:
                    state.grid[i][j] = '0'
            elif state.grid[i][j] == '0': #transparent can change to solid with 50% chance
                if random.randint(0, 1) == 1:
                    state.grid[i][j] = '1'

    
    return state

state = State()
state.start()
state.show_state()

while not is_goal_reached(state):
# for _ in range(20):
    print("Player A's turn")
    pathA = ga(state, state.A)  #find the best path for A
    result = state.move(state.A, pathA[0])  #move A according to the pathA
    print(result)
    state.update_map("a")
    state.show_state()  #show the updated state 
    if is_goal_reached(state): #check if wins
        print("Player A wins!")
        break

    print("Player B's turn")
    pathB = ga(state, state.B)  #find best path for B
    print("Player B's path:", pathB)
    result = state.move(state.B, pathB[0])  #move B according to pathB
    print(result)
    state.update_map("b")
    state.show_state()  #show the updated state 
    if is_goal_reached(state):
        print("Player B wins!")  #check if wins
        break
