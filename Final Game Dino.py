import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 850
SCREEN_WIDTH = 1600

font = pygame.font.Font('freesansbold.ttf', 20)

LEADERBOARDENTRIES = 10
leaderboard = open("leaderboard.txt", "r")
leaderboardValues = []

leaderboardScores = []
leaderboardNames = []


leaderboard = open("leaderboard.txt", "r")
leaderboardValues = []
for i in range(LEADERBOARDENTRIES*2):
    leaderboardValues.insert(100000000, leaderboard.readline())
for i in range(LEADERBOARDENTRIES):
    leaderboardScores.insert(1000000000000, int(leaderboardValues[2*i+1][:-1:]))
for i in range(LEADERBOARDENTRIES):
    leaderboardNames.insert(1000000000000, leaderboardValues[2*i][:-1:])
print(leaderboardNames)



def displayLBText():
    leaderboard = open("leaderboard.txt", "r")
    leaderboardValues = []
    for i in range(LEADERBOARDENTRIES*2):
        leaderboardValues.insert(100000000, leaderboard.readline())
    i = -1
    for j in range(LEADERBOARDENTRIES):
        text = ""
        i+=1
        text += leaderboardValues[i][:-1:]
        i+=1
        text += " " + leaderboardValues[i][:-1:]
        text = font.render(text, True, (0, 0, 0))
        score = font.render("Your Score: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200 + j * 30)
        SCREEN.blit(text, textRect)
    return text

def insertNewScoreIntoLB(name, score):
    if score > leaderboardScores[-1]:
        i=0
        while score < leaderboardScores[i]:
            i+=1
        leaderboardNames.insert(i, name)
        del leaderboardNames[-1]
        leaderboardScores.insert(i, score)
        del leaderboardScores[-1]
        leaderboardText = ""
        for i in range(LEADERBOARDENTRIES):
            leaderboardText += leaderboardNames[i] + "\n"
            leaderboardText += str(leaderboardScores[i]) + "\n"
        leaderboardText += " \n"
        f = open("leaderboard.txt", "w")
        f.write(leaderboardText)
        print(leaderboardText)


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Dino", "Robot.png")),
           pygame.image.load(os.path.join("Dino", "Robot.png"))]
JUMPING = pygame.image.load(os.path.join("Dino", "Robot.png"))
DUCKING = [pygame.image.load(os.path.join("Dino", "Robot.png")),
           pygame.image.load(os.path.join("Dino", "Robot.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.timeSinceJump = 0

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump and self.timeSinceJump > 10:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


clock = pygame.time.Clock()
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    player = Dinosaur()
    player.timeSinceJump+=1
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        clock.tick(300)
        player.timeSinceJump+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    user_name = ""
    global points
    run = True
    while run:
        clock.tick(30)
        
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 400))
            text = font.render("Press enter to Start", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
        elif death_count > 0:
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 440))
            displayLBText()
            score = font.render("Your Score: " + str(points) + ". Press Enter to restart.", True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
            SCREEN.blit(score, scoreRect)
            name = font.render("Your name: " + user_name, True, (0, 0, 0))
            nameRect = score.get_rect()
            nameRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(name, nameRect)

        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN and death_count > 0 and points > leaderboardScores[-1]:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER:
                    user_name += event.unicode
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and death_count != 0:
                    insertNewScoreIntoLB(user_name, points)
                    main()
                elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    main()


menu(death_count=0)
