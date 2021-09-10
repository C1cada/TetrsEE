import pygame
import random
import math
import copy

colors = [
    (0, 0, 0), 
    (2, 252, 252), 
    (49, 252, 3),
    (252, 3, 3),  
    (3, 36, 252), 
    (252, 111, 3), 
    (227, 3, 252), 
    (252, 244, 3), 
]

initialPopulation = 200
mutationRate = 0.2
mutationStep = 0.5

class Figure:

    
    def __init__(self, x, y):
        self.figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
        ]   

        self.x = x
        self.y = y
        self.rand = random.randint(0,  len(self.figures) - 1)
        self.type = self.rand
        self.color = self.rand + 1
        self.rotation = 0
        self.rotations = len(self.figures[self.type])
        

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % self.rotations

class Tetris:
    level = 2
    state = "start"
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.fitness = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.fitness += (lines*4) ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1

        self.freezetest()

    def go_space2(self):
        while not self.intersects():
            self.figure.y += 1
            self.fitness += 1
        self.figure.y -= 1
        
        self.freeze()

    def return_fitness(self):
        return self.fitness

    def go_down(self):
        self.figure.y += 1
        self.fitness += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_downtesting(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freezetesting()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def freezetest(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color

    def freezetesting(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color

        if self.intersects():
            self.state = "test_complete"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

class Organism:

    def __init__(self, genome):
        """
        genome:
            all the weights and genes for the organism
            averageHeight
            relativeHeight
            totalHeight
            flatness
            rowsCleared
            holes
            pits
            holes greater than 2 deep????
        fitness
        """
        # self.fitness = 0
        self.genome = genome
        

    def mutate(self):
        if random.random() < mutationRate:
            self.genome["averageHeight"] += (random.random() * mutationStep * 2) - mutationStep

        if random.random() < mutationRate:
            self.genome["relativeHeight"] += (random.random() * mutationStep * 2) - mutationStep

        if random.random() < mutationRate:
            self.genome["totalHeight"] += (random.random() * mutationStep * 2) - mutationStep

        if random.random() < mutationRate:
            self.genome["flatness"] += (random.random() * mutationStep * 2) - mutationStep

        if random.random() < mutationRate:
            self.genome["rowsCleared"] += (random.random() * mutationStep * 2) - mutationStep

        if random.random() < mutationRate:
            self.genome["holes"] += (random.random() * mutationStep * 2) - mutationStep
            
        if random.random() < mutationRate:
            self.genome["pits"] += (random.random() * mutationStep * 2) - mutationStep


class Controller:

    """
    initialize game
    initialize pop
    fitness eval
    data from game
    breeding
    looping
    any visual things
    """
    def __init__(self):
        self.board = []

    def live(self, initpop, gens, ):
        organisms = self.generateInitPop(initpop)
        for i in range(gens):
            print(i)
            orgfit = {}
            for i in organisms:
                # print(i)
                fitness = self.gameTime(i, False)
                # print(fitness)
                
                orgfit[i] = fitness

            print("highest: " + str(max(orgfit.values())))
            print("average: " + str(sum(orgfit.values())/len(orgfit)))
            elite = list(orgfit.keys())[list(orgfit.values()).index(max(orgfit.values()))]
            elites = sorted(orgfit, key=orgfit.get, reverse=True)[:50]
            organisms = self.breeding(elites, initpop)



        print(elite.genome)
        self.playGame(elite)

    def playGame(self, org):
        pygame.init()

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)

        size = (400, 500)
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Tetris")
        game = Tetris(20, 10)
        speed = 1
        running = True
        counter = 0

        while running:
            
            if not game.figure:
                game.new_figure()

            counter += 1
            
            self.board = list(game.field)
            moves = self.allMoves(org, game.figure)
            # print(moves)
            for rots in range(moves[0]):
                game.rotate()

            counter = 0
            current_moves = 0
            while current_moves != moves[1]:
                if current_moves > moves[1]:
                    old_x = game.figure.x
                    game.figure.x += -1
                    inter = game.intersects()
                    game.figure.x = old_x
                    if inter:
                        game.go_space2()
                        # print("going")
                        # print(current_moves)
                        # print(moves[1])
                        current_moves = moves[1]
                    else:
                        game.go_side(-1)
                        current_moves += -1
                if current_moves < moves[1]:
                    old_x = game.figure.x
                    game.figure.x += 1
                    inter = game.intersects()
                    game.figure.x = old_x
                    if inter:
                        game.go_space2()
                        # print("going")
                        # print(current_moves)
                        # print(moves[1])
                        current_moves = moves[1]
                    else:
                        game.go_side(1)
                        current_moves += 1
               

            if current_moves == moves[1]:
                game.go_space2()
                # print("gone")

            pygame.time.wait(100)
            screen.fill(WHITE)

            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, colors[game.field[i][j]],
                                        [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(screen, colors[game.figure.color],
                                            [game.x + game.zoom * (j + game.figure.x) + 1,
                                            game.y + game.zoom * (i + game.figure.y) + 1,
                                            game.zoom - 2, game.zoom - 2])

            pygame.display.flip()


            if game.state == "gameover":
                running = False

        pygame.quit()
    def gameTime(self, org, visual):
        game = Tetris(20, 10)
        speed = 1
        running = True
        counter = 0

        while running:
            
            if not game.figure:
                game.new_figure()


            
            self.board = list(game.field)
            moves = self.allMoves(org, game.figure)
            # print(moves)
            for rots in range(moves[0]):
                game.rotate()

            current_moves = 0
            while current_moves != moves[1]:
                if current_moves > moves[1]:
                    old_x = game.figure.x
                    game.figure.x += -1
                    inter = game.intersects()
                    game.figure.x = old_x
                    if inter:
                        game.go_space2()
                        # print("going")
                        # print(current_moves)
                        # print(moves[1])
                        counter += 1
                        current_moves = moves[1]
                    else:
                        game.go_side(-1)
                        current_moves += -1
                if current_moves < moves[1]:
                    old_x = game.figure.x
                    game.figure.x += 1
                    inter = game.intersects()
                    game.figure.x = old_x
                    if inter:
                        game.go_space2()
                        # print("going")
                        # print(current_moves)
                        # print(moves[1])
                        current_moves = moves[1]
                        counter += 1
                    else:
                        game.go_side(1)
                        current_moves += 1
               

            if current_moves == moves[1]:
                game.go_space2()
                counter += 1
                # print("gone")

                


            if game.state == "gameover" or counter > 299:
                # print(counter)
                running = False
                if counter > 299:
                    print("it happenedf")
        if visual:
            self.visual(game)
        return game.fitness

    def visual(self, game):
        pygame.init()

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)

        size = (400, 500)
        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Tetris")

        done = False

        pressing_down = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(WHITE)

            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, colors[game.field[i][j]],
                                        [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])



            pygame.display.flip()

        pygame.quit()

    def allMoves(self, org, piece):

        # print("gone?")
        rotations = piece.rotations
        tempGame = Tetris(20, 10)
        scores = {}

        visual = False
        if visual:
            pygame.init()

            BLACK = (0, 0, 0)
            WHITE = (255, 255, 255)
            GRAY = (128, 128, 128)

            size = (400, 500)
            screen = pygame.display.set_mode(size)

            pygame.display.set_caption("Tetris")
        pressing_down = False
        working = True
        tempGame.new_figure()

        tempGame.figure = copy.deepcopy(piece)
        counter = 0
        for rot in range(tempGame.figure.rotations):
            tempGame.field = copy.deepcopy(self.board)
            done = False
            tempGame.state = "start"
            moves = 0
            while not done:
                if visual:

                    # pygame.time.wait(100)
                    screen.fill(WHITE)

                    for i in range(tempGame.height):
                        for j in range(tempGame.width):
                            pygame.draw.rect(screen, GRAY, [tempGame.x + tempGame.zoom * j, tempGame.y + tempGame.zoom * i, tempGame.zoom, tempGame.zoom], 1)
                            if tempGame.field[i][j] > 0:
                                pygame.draw.rect(screen, colors[tempGame.field[i][j]],
                                                [tempGame.x + tempGame.zoom * j + 1, tempGame.y + tempGame.zoom * i + 1, tempGame.zoom - 2, tempGame.zoom - 1])

                    if tempGame.figure is not None:
                        for i in range(4):
                            for j in range(4):
                                p = i * 4 + j
                                if p in tempGame.figure.image():
                                    pygame.draw.rect(screen, colors[tempGame.figure.color],
                                                    [tempGame.x + tempGame.zoom * (j + tempGame.figure.x) + 1,
                                                    tempGame.y + tempGame.zoom * (i + tempGame.figure.y) + 1,
                                                    tempGame.zoom - 2, tempGame.zoom - 2])

                    pygame.display.flip()

                old_x = tempGame.figure.x
                tempGame.figure.x += -1
                inter = tempGame.intersects()
                tempGame.figure.x = old_x
                if inter:
                    tempGame.go_downtesting()
                else:
                    tempGame.go_side(-1)
                    moves += -1

                if tempGame.state == "test_complete":
                    done = True

            space = True
            while space:
                done = False
                tempGame.figure.x = 3
                tempGame.figure.y = 0
                tempGame.field = copy.deepcopy(self.board)
                tempGame.state = "start"
                current_moves = 0
                while not done:
                    if visual:

                        screen.fill(WHITE)

                        for i in range(tempGame.height):
                            for j in range(tempGame.width):
                                pygame.draw.rect(screen, GRAY, [tempGame.x + tempGame.zoom * j, tempGame.y + tempGame.zoom * i, tempGame.zoom, tempGame.zoom], 1)
                                if tempGame.field[i][j] > 0:
                                    pygame.draw.rect(screen, colors[tempGame.field[i][j]],
                                                    [tempGame.x + tempGame.zoom * j + 1, tempGame.y + tempGame.zoom * i + 1, tempGame.zoom - 2, tempGame.zoom - 1])

                        if tempGame.figure is not None:
                            for i in range(4):
                                for j in range(4):
                                    p = i * 4 + j
                                    if p in tempGame.figure.image():
                                        pygame.draw.rect(screen, colors[tempGame.figure.color],
                                                        [tempGame.x + tempGame.zoom * (j + tempGame.figure.x) + 1,
                                                        tempGame.y + tempGame.zoom * (i + tempGame.figure.y) + 1,
                                                        tempGame.zoom - 2, tempGame.zoom - 2])

                        pygame.display.flip()
                    if current_moves != moves:
                        if current_moves > moves:
                            old_x = tempGame.figure.x
                            tempGame.figure.x += -1
                            inter = tempGame.intersects()
                            tempGame.figure.x = old_x
                            if inter:
                                tempGame.go_downtesting()
                            else:
                                tempGame.go_side(-1)
                                current_moves += -1
                        if current_moves < moves:
                            old_x = tempGame.figure.x
                            tempGame.figure.x += 1
                            inter = tempGame.intersects()
                            tempGame.figure.x = old_x
                            if inter:
                                tempGame.go_downtesting()
                            else:
                                tempGame.go_side(1)
                                current_moves += 1
                    elif current_moves == moves:
                        tempGame.go_downtesting()

                    if tempGame.state == "test_complete":
                        score = self.getValues(tempGame.field, org)
                        instructions = [rot, moves]
                        scores[score] = instructions
                        done = True
                moves += 1

                if moves > 8:
                    space = False
            tempGame.figure.x = 3
            tempGame.figure.y = 0
            tempGame.rotate()


                
        if visual:
            pygame.quit()
    
            

            
        return scores[max(scores)]
        
    def averageHeight(self, field):
        heights = 0
        for x in range(10):
            flag = False
            for y in range(20):
                if field[y][x] != 0:
                    flag = True
                if flag:
                    heights += 1
        return heights/10

    def relativeHeight(self, field):
        heights = []
        for x in range(10):
            flag = False
            height = 0
            for y in range(20):
                if field[y][x] != 0:
                    flag = True
                if flag:
                    height += 1
            heights.append(height)
        return max(heights) - min(heights)

    def totalHeight(self, field):
        heights = 0
        for x in range(10):
            flag = False
            for y in range(20):
                if field[y][x] != 0:
                    flag = True
                if flag:
                    heights += 1
                
        return heights

    def flatness(self, field):
        heights = []
        flatness = 0
        for x in range(10):
            flag = False
            height = 0
            for y in range(20):
                if field[y][x] != 0:
                    flag = True
                if flag:
                    height += 1
            heights.append(height)
        for i in range(len(heights)-1):
            flatness += abs(heights[i] - heights[i+1])
        return flatness

    def rowsCleared(self, field):
        rowsCleared = 0
        for i in field:
            flag = True
            for x in i:
                if x == 0:
                    flag = False
            if flag:
                rowsCleared += 1

        return rowsCleared**2

    def holes(self, field):
        holes = 0
        for x in range (10):
            for y in range(19):
                if field[y][x] != 0:
                    i = 1
                    while field[y + i][x] == 0:
                        i += 1
                        holes += 1
                        if (y + i > 19):
                            break
        return holes

    def pits(self, field):
        pits = 0
        for x in range (10):
            for y in range(18):
                if field[y][x] == 0 and ((x + 1 > 9 or field[y][x+1] != 0) and (x - 1 < 0 or field[y][x -1] != 0)):
                    if field[y+1][x] == 0 and field[y+2][x] == 0:
                        pits += 1
                        break
        return pits
        # return 0

    def getValues(self, field, org):
        """
        get the values for each gene based on current board
            averageHeight find height of each collumn then average
            relativeHeight ^
            totalHeight ^
            flatness avg difference in height
            rowsCleared how many full rows
            holes how many empty spaces with block over it
            pits empty spaces with blocks or wall to the side and nothing over > 2 depth
        """
        values = {
            "averageHeight" : self.averageHeight(field),                                                                                               
            "relativeHeight" : self.relativeHeight(field),
            "totalHeight" : self.totalHeight(field),
            "flatness" : self.flatness(field),
            "rowsCleared" : self.rowsCleared(field),
            "holes" : self.holes(field),
            "pits" : self.pits(field)
        }
        score1 = 0
        score1 += values["averageHeight"] * org.genome["averageHeight"]
        score1 += values["relativeHeight"] * org.genome["relativeHeight"]
        score1 += values["totalHeight"] * org.genome["totalHeight"]
        score1 += values["flatness"] * org.genome["flatness"]
        score1 += values["rowsCleared"] * org.genome["rowsCleared"]
        score1 += values["holes"] * org.genome["holes"]
        score1 += values["pits"] * org.genome["pits"]
        return score1

    def generateInitPop(self, popSize):
        organisms = []
        for i in range(popSize):
            genome = {
                "averageHeight" : random.uniform(-1, 1),                                                                                               
                "relativeHeight" : random.uniform(-1, 1),
                "totalHeight" : random.uniform(-1, 1),
                "flatness" : random.uniform(-1, 1),
                "rowsCleared" : random.uniform(-1, 1),
                "holes" : random.uniform(-1, 1),
                "pits" : random.uniform(-1, 1)
            }
            organisms.append(Organism(genome))

        return organisms

    def breeding(self, elites, initial_population):
        new_population = []
        for i in elites:
            new_population.append(i)
        random.shuffle(elites)
        # print(len(elites))
        for i in range(int(len(elites)/2)):
            for x in range(int((initial_population-len(elites))/(len(elites)/2))):
                new_population.append(self.crossover(elites[i], elites[i+1]))


        return new_population

    def crossover(self, parent1, parent2):
        genome = {
            "averageHeight" : random.choice((parent1.genome["averageHeight"], parent2.genome["averageHeight"])),                                                                                               
            "relativeHeight" : random.choice((parent1.genome["relativeHeight"], parent2.genome["relativeHeight"])),
            "totalHeight" : random.choice((parent1.genome["totalHeight"], parent2.genome["totalHeight"])),
            "flatness" : random.choice((parent1.genome["flatness"], parent2.genome["flatness"])),
            "rowsCleared" : random.choice((parent1.genome["rowsCleared"], parent2.genome["rowsCleared"])),
            "holes" : random.choice((parent1.genome["holes"], parent2.genome["holes"])),
            "pits" : random.choice((parent1.genome["pits"], parent2.genome["pits"]))
        }
        org = Organism(genome)
        org.mutate()
        return org

control = Controller() 
control.live(initialPopulation, 70)
