import pygame, random, math, threading, numpy as np

pygame.init()

# Best score: 67? (yes)
#             3  47

class Player():
    def __init__(self, x, y, vel, velIncrease, levelAmount, color):
        self.pos = np.array([x, y])
        self.dir = np.array([0, 0])
        self.vel = vel
        self.color = color
        self.velIncrease = velIncrease
        self.levelAmount = levelAmount
        self.pointAdder = 1

        self.snake = []
        self.length = 0
        self.newLengthAmount = 1

        self.lvl = 0
        self.score = 0                  


    def lose(self):
        print(self.lvl)
        print(self.score)
        game.gameOver = True


    def point(self, pos):
        game.map[pos[1]][pos[0]] = None
        for apple in game.apples:
            # print(pos); print(game.apples)
            if pos[0] == apple[0] and pos[1] == apple[1]:
                game.apples.remove(apple)
        game.new_apple(1)

        self.score += self.pointAdder
        self.length += 1 / self.newLengthAmount
        if self.score % self.levelAmount == 0 and self.score > 0: 
            self.lvl += 1
            self.vel -= self.velIncrease*0.01*self.vel
        


    def collision(self, pos):
        # print(self.pos)
        if -1 < pos[0] < game.size[0] and -1 < pos[1] < game.size[1]:
            if game.map[pos[1]][pos[0]] == None:
                return True
            # elif game.map[pos[1]][pos[0]] == "SNAKE":
            #     return "SNAKE"
            elif game.map[pos[1]][pos[0]] == "APPLE":
                return "APPLE"
        return False


    def changeDir(self, key):
        if key[pygame.K_w] and self.dir[1] != 1:
            self.dir = np.array([0, -1])  
        if key[pygame.K_a] and self.dir[0] != 1:
            self.dir = np.array([-1, 0])  
        if key[pygame.K_s] and self.dir[1] != -1:
            self.dir = np.array([0, 1])  
        if key[pygame.K_d] and self.dir[0] != -1:
            self.dir = np.array([1, 0])  

    
    def move(self):
        collision = self.collision(self.pos + self.dir)
        if collision:
            if collision == "APPLE": self.point(self.pos + self.dir)
            self.snake.append([self.pos[0], self.pos[1], math.floor(self.length)])
            # print(self.snake)
            game.map[self.pos[1]][self.pos[0]] = "SNAKE"
            self.pos += self.dir
            game.map[self.pos[1]][self.pos[0]] = "HEAD"
            for i in self.snake:
                i[2] -= 1
                if i[2] < 1:
                    print(game.map[i[1]][i[0]])
                    game.map[i[1]][i[0]] = None
                    self.snake.remove(i)
        else:
            self.lose()


    def draw(self, screen):
        for i in self.snake:
            x = i[0]; y = i[1]
            pygame.draw.rect(screen, self.color,
            (x*game.dist+cx-game.dist//2*game.size[0], y*game.dist+cy-game.dist//2*game.size[1], game.dist, game.dist))
        x = self.pos[0]; y = self.pos[1] 
        pygame.draw.rect(screen, self.color,
            (x*game.dist+cx-game.dist//2*game.size[0], y*game.dist+cy-game.dist//2*game.size[1], game.dist, game.dist))


class Game():
    def __init__(self):
        self.size = [0, 0]
        self.dist = 30
        self.colors = [(0, 100, 0), (0, 150, 0)]
        self.map = []
        self.apples = []
        self.borderSize = 40
        self.gameOver = False
        self.fade = [0, 0]
        # self.i = 0


    def new_map(self, x, y):
        self.size = [x, y]
        for i in range(0, y):
            self.map.append([])                
            for _ in range(0, x):
                self.map[i].append(None)


    def new_apple(self, num):
        print("NOOOOOOOO")
        for i in range(0, num):
            while True:
                x = random.randint(0, game.size[0]-1); y = random.randint(0, game.size[1]-1)
                # if self.i > 2: 
                #     x = player.pos[0]; y = player.pos[1]
                # else:
                #     x = random.randint(0, game.size[0]-1); y = random.randint(0, game.size[1]-1)
                # self.i += 1
                if player.collision([x, y]) == True:
                    print(player.snake)
                    print([x, y])
                    self.apples.append([x, y])
                    self.map[y][x] = "APPLE"
                    break
                

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200),
        (cx-(self.size[0]*self.dist+self.borderSize)//2, cy-(self.size[1]*self.dist+self.borderSize)//2, 
        self.size[0]*self.dist+self.borderSize, self.size[1]*self.dist+self.borderSize))

        for y in range(0, self.size[1]):
            for x in range(0, self.size[0]):
                color = self.colors[(y*self.size[0]+x)%2]
                pygame.draw.rect(screen, color,
                (x*self.dist+cx-self.dist//2*self.size[0], y*self.dist+cy-self.dist//2*self.size[1], self.dist, self.dist))

        for i in self.apples:
            x = i[0]; y = i[1]
            pygame.draw.rect(screen, (255, 0, 0),
                (x*self.dist+cx-self.dist//2*self.size[0], y*self.dist+cy-self.dist//2*self.size[1], self.dist, self.dist))    


def render(screen):
    screen.fill((0, 0, 0))
    game.draw(screen)
    player.draw(screen)
    if game.gameOver == True:
        if game.fade[0]+1 < 200: game.fade[0] += 20 
        else: game.fade[0] = 200
        s = pygame.Surface((w,h), pygame.SRCALPHA)  
        s.fill((0,0,0,game.fade[0]))                         
        screen.blit(s, (0,0))
        text = font.render("GAME OVER", 1, (255, 0, 0))
        screen.blit(text, (cx-text.get_rect().width//2, cy-text.get_rect().height//2-cy//5*3))    
    pygame.display.update()


w, h = 1500, 800; cx, cy = w//2, h//2
fontSize = 150
font = pygame.font.SysFont("candara", fontSize, 1, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))

game = Game()
moveTick = pygame.time.get_ticks()
delay = pygame.time.get_ticks()
player = None

def play():
    global player, moveTick
    game.new_map(27, 21)
    size = 30
    game.dist = size
    player = Player(x=game.size[0]//2, y=game.size[1]//2, vel=100, velIncrease=20, levelAmount=5, color=[200, 0, 0])

    game.new_apple(20)

    while True:
        clock.tick(60)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event == pygame.QUIT:
                break

        if key[pygame.K_ESCAPE]:
            break 

        if game.gameOver == False:
            player.changeDir(key)
            if pygame.time.get_ticks() - moveTick > player.vel:
                moveTick = pygame.time.get_ticks(); player.move()
                for y in range(0, game.size[1]):
                    row = ""
                    for x in range(0, game.size[0]):
                        if player.pos[0] == x and player.pos[1] == y: row += "X"
                        elif game.map[y][x] == "SNAKE": row += "#"
                        elif game.map[y][x] == None: row += "/"
                        elif game.map[y][x] == "APPLE": row += "O"
                    print(row)
                print(player.vel)

        render(screen)


play()