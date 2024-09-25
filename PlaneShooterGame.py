import os.path
import sys

import pygame, random
# Let's import the Car Class
import pygame

WHITE = (255, 255, 255)

enemies = []
goodItems = []
enemy_obs_width  = 50
enemy_obs_height = 100
goodItem_obs_width = 40
goodItem_obs_height = 40
#--------------------------------------------  LOAD IMAGE -----------------------------------------------------------
red_rocket = pygame.image.load(os.path.join('image','rocketEnemy.png'))
blue_rocket = pygame.image.load(os.path.join('image','rocketPlayer.png'))
F4Phantom = pygame.image.load(os.path.join('image','enemyPlane-F-4Phantom.png'))
F4Phantom = pygame.transform.scale(F4Phantom, (enemy_obs_width, enemy_obs_height))
Sukhoi47 = pygame.image.load(os.path.join('image','enemyPlane-Sukhoi47.png'))
Sukhoi47 = pygame.transform.scale(Sukhoi47, (enemy_obs_width, enemy_obs_height))
F22Raptor = pygame.image.load(os.path.join('image','enemyPlane-F-22Raptor.png'))
F22Raptor = pygame.transform.scale(F22Raptor, (enemy_obs_width, enemy_obs_height))
diaomond =  pygame.image.load(os.path.join('image','diamond.jfif'))
diaomond = pygame.transform.scale(diaomond, (enemy_obs_width, enemy_obs_height))
fuelIcon =  pygame.image.load(os.path.join('image','fuelIcon.png'))
fuelIcon = pygame.transform.scale(fuelIcon, (goodItem_obs_width, goodItem_obs_height))
repairIcon =  pygame.image.load(os.path.join('image','repairIcon.png'))
repairIcon = pygame.transform.scale(repairIcon, (goodItem_obs_width, goodItem_obs_height))

#create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y, type):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        if type == "player":
            for num in range(1,23):
                img = pygame.image.load(f"image/playerExp{num}.png")
                img = pygame.transform.scale(img,(100,100))
                self.images.append(img)
        else:
            for num in range(1,23):
                img = pygame.image.load(f"image/enemyExp{num}.png")
                img = pygame.transform.scale(img,(100,100))
                self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

#       if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

class Rocket:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, screen_height):
        return not(self.y <= screen_height and self.y >= 0)

    def collision(self, obj):
        return  collide(self, obj)




class Car(pygame.sprite.Sprite):
    coolDown = 30
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self ,x,y,width, height, health = 100, fuel = 500):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.x = x
        self.y = y
        self.health = health
        self.fuel = fuel
        self.width = width
        self.height = height
        self.car_img = None
        self.rocket_img = None
        self.rockets = []
        self.cooldown_counter = 0

    def draw(self,screen):
        screen.blit(self.car_img, (self.x,self.y))
        for rocekt in self.rockets:
            rocekt.draw(screen)

    def move_rockets(self, vel, obj):
        self.cooldown()
        for rocket in self.rockets:
            rocket.move(vel)
            if rocket.off_screen(screen_height):
                self.rockets.remove(rocket)
            elif rocket.collision(obj):
                obj.health -= 10
                explosion_enemy = Explosion(obj.x + enemy_obs_width / 2, obj.y + enemy_obs_height / 2, "enemy")
                explosion_group.add(explosion_enemy)
                self.rockets.remove(rocket)


    def cooldown(self):
        if self.cooldown_counter >= self.coolDown:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1


    def shoot(self):
        if self.cooldown_counter == 0:
            rocket = Rocket(self.x, self.y, self.rocket_img)
            self.rockets.append(rocket)
            self.cooldown_counter = 1

class Player(Car):
    def __init__(self,x,y,width, height, health = 100, fuel = 500):
        super().__init__(x, y, width, height, health, fuel)
        self.car_img = playerCarImage1
        self.rocket_img = blue_rocket
        self.mask = pygame.mask.from_surface(self.car_img)
        self.max_health = health
        self.max_fuel = fuel
        self.kills = 0
        self.cash = 0

    def move_rockets(self, vel, objs):
        self.cooldown()
        for rocket in self.rockets:
            rocket.move(vel)
            if rocket.off_screen(screen_height):
                self.rockets.remove(rocket)
            else:
                for obj in objs:
                    if rocket.collision(obj):
                        playerCar1.kills += 1
                        explosion_player = Explosion(obj.x + enemy_obs_width/2, obj.y + enemy_obs_height/2, "player")
                        explosion_group.add(explosion_player)
                        objs.remove(obj)
                        if obj.car_img == F22Raptor:
                            playerCar1.cash += 50
                        if obj.car_img == Sukhoi47:
                            playerCar1.cash += 40
                        if obj.car_img == F4Phantom:
                            playerCar1.cash += 20

                        if rocket in self.rockets:
                            self.rockets.remove(rocket)

    def draw(self, screen):
        super().draw(screen)
        self.healthbar(screen)
        self.fuelbar(screen)

    def healthbar(self, screen):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y + self.height + 10, self.width, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + self.height + 10, self.width * (self.health/self.max_health), 10))

    def fuelbar(self, screen):
        pygame.draw.rect(screen, (0, 102, 255), ( 10, 10, self.width, 10))
        pygame.draw.rect(screen, (0, 204, 255), (10, 10, self.width * (self.fuel/self.max_fuel), 10))
        draw_text(screen,"FUEL", 14, 23,11)


class Enemy(Car):
    TYPE_MAP = {
                "F-4Phantom": (F4Phantom,red_rocket),
                "F-22Raptor": (F22Raptor, red_rocket),
                "Sukhoi-47": (Sukhoi47, red_rocket),

    }
    def __init__(self,x,y,width, height, type_img,health = 100, fuel = 500):
        super().__init__(x, y, width, height, health, fuel)
        self.car_img, self.rocket_img = self.TYPE_MAP[type_img]
        self.mask = pygame.mask.from_surface(self.car_img)

    def move(self,vel):
        self.y += vel

    def shoot(self):
        if self.cooldown_counter == 0:
            rocket = Rocket(self.x + 10, self.y + 10, self.rocket_img)
            self.rockets.append(rocket)
            self.cooldown_counter = 1


class GoodItem(Car):
    TYPE_MAP_ICON = {
                "fuel": fuelIcon,
                "repair": repairIcon,
    }
    def __init__(self,x,y,width, height, type_img,health = 100, fuel = 500):
        super().__init__(x, y, width, height, health, fuel)
        self.car_img = self.TYPE_MAP_ICON[type_img]
        self.mask = pygame.mask.from_surface(self.car_img)

    def move(self,vel):
        self.y += vel


pygame.init()

screen_width = 600
screen_height = 600

size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Car Racing")

background = pygame.image.load(os.path.join('image','roadImage.jpg'))

global playerCarImage1, leftPlaneImg, rightPlaneImg

playerCarImage1 = pygame.image.load(os.path.join('image','samolet1.png'))
leftPlaneImg = pygame.image.load(os.path.join('image','leftPlaneImg.png'))
rightPlaneImg = pygame.image.load(os.path.join('image','rightPlaneImg.png'))
playerCar1X = 200
playerCar1Y = 320
playerCarImage1_width = 50
playerCarImage1_height = 100
playerCarImage1 = pygame.transform.scale(playerCarImage1, (playerCarImage1_width, playerCarImage1_height))
leftPlaneImg = pygame.transform.scale(leftPlaneImg, (playerCarImage1_width, playerCarImage1_height))
rightPlaneImg = pygame.transform.scale(rightPlaneImg, (playerCarImage1_width, playerCarImage1_height))
playerCar1 = Player(playerCar1X,playerCar1Y,playerCarImage1_width, playerCarImage1_height)

#playerCar1.rect.x = 200
#playerCar1.rect.y = 300
playerCar1_velocity = 5

playerCarImage2 = pygame.image.load(os.path.join('image','car_1.jpg'))

#playerCar2 = Car(300, 200)
#playerCar2.rect.x = 400
#playerCar2.rect.y = 400
font_name = pygame.font.match_font("arial")

explosion_group = pygame.sprite.Group()

def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(str(text), True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
    #pygame.display.update()

def redraw_screen(j,ticks, enemies, goodItems,lives, levels):
    screen.fill((0, 0, 0))
    screen.blit(background, (0, j))
    screen.blit(background, (0, j - screen_height))

    for enemy in enemies:
        enemy.draw(screen)

    for goodItem in goodItems:
        goodItem.draw(screen)

    playerCar1.draw(screen)

    draw_text(screen, "Time:", 24, screen_width - 170, screen_height - 550)
    draw_text(screen, str(ticks), 24, screen_width - 130, screen_height - 550)
    draw_text(screen, "Lives:", 24, screen_width - 550, screen_height - 530)
    draw_text(screen, str(lives), 24, screen_width - 500, screen_height - 530)
    draw_text(screen, "Levels:", 24, screen_width - 550, screen_height - 570)
    draw_text(screen, str(levels), 24, screen_width - 500, screen_height - 570)
    draw_text(screen, "Kills:", 24, screen_width - 550, screen_height - 500)
    draw_text(screen, str(playerCar1.kills), 24, screen_width - 500, screen_height - 500)
    draw_text(screen, "Cash:", 24, screen_width - 550, screen_height - 470)
    draw_text(screen, str(playerCar1.cash) + "$", 24, screen_width - 500, screen_height - 470)

def game_over(lost,lost_counter,FPS,running):
    delay = 2
    draw_text(screen, "YOU LOST!", 24, screen_width / 2 , screen_height - 300)
    if lost:
        if lost_counter >= FPS*3:
            pygame.time.delay( delay * 1000)
            sys.exit()

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return  obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main(playerCarImage1):
    running = True
    clock = pygame.time.Clock()
    FPS = 60
    j = int(0)
    lives = 5
    levels = 1
    lost = False
    lost_counter = 0

    wave_length = 1
    goodItem_wave_length = 2
    enemy_vel = 1
    boost_player = 0.5
    goodItem_vel = 1
    rocket_vel = 4
    spawn_interval_enemy = 30
    spawn_interval_goodItem = 50
    start_ticks_enemy = round(pygame.time.get_ticks()/100)
    start_ticks_goodItem = round(pygame.time.get_ticks() / 100)





    while running:
        ticks = round(pygame.time.get_ticks() / 100)
        clock.tick(FPS)
        redraw_screen(j, ticks,enemies, goodItems ,lives,levels)

        explosion_group.draw(screen)
        explosion_group.update()

        if playerCar1.health < 0:
            lives -= 1
            playerCar1.health = 100
            playerCar1.x = playerCar1X
            playerCar1.y = playerCar1Y

#        if playerCar1.fuel < 0:
#            lost = True
#            lost_counter += 1
#            game_over(lost, lost_counter, FPS, running)

        if pygame.time.get_ticks() % 30 == 0:
            playerCar1.fuel -= 2

        if lives <= 0:
            lost = True
            lost_counter += 1
            game_over(lost,lost_counter,FPS,running)


#        if len(enemies) == 0:
#            levels += 1
#            wave_length += 5
        if ticks - start_ticks_enemy > spawn_interval_enemy:
            newElementEnemy = Enemy(random.randint(50, screen_width - 50),  -50, enemy_obs_width, enemy_obs_height, random.choice(["F-4Phantom", "F-22Raptor", "Sukhoi-47"]))

#			Обхожда всички обекти, за да провери дали новосъздадения няма да се удари с някой от съществуващите
            newElementFalsePosition = True
            if len(enemies) == 0:
                enemies.append(newElementEnemy)
            else:
                while newElementFalsePosition:

                    hasCollide = False
                    lengthOfEnemies = len(enemies)

                    for i in range(lengthOfEnemies):
                        existElement = enemies[i]
                        if collide(existElement,newElementEnemy):
                            hasCollide = True
                            break

                    if hasCollide == False:
                        enemies.append(newElementEnemy)
                        newElementFalsePosition = False
                    else:
                        newElementEnemy = Enemy(random.randint(50, screen_width - 50), -50, enemy_obs_width,enemy_obs_height, random.choice(["F-4Phantom", "F-22Raptor", "Sukhoi-47"]))

            start_ticks_enemy = ticks

        if ticks - start_ticks_goodItem > spawn_interval_goodItem:
            newElementGoodItem = GoodItem(random.randint(50, screen_width - 50), random.randint(-500, -50), goodItem_obs_width, goodItem_obs_height, random.choice(["fuel", "repair"]))
#             Обхожда всички обекти, за да провери дали новосъздадения няма да се удари с някой от съществуващите
            newElementFalsePosition = True
            if len(goodItems) == 0:
                goodItems.append(newElementGoodItem)
            else:
                while newElementFalsePosition:
                    print("---------------------------")
                    print("len(goodItems)=", len(goodItems))

                    hasCollide = False
                    lengthOfGoodItems = len(goodItems)

                    print("PREDI FOR CIKYL")

                    for i in range(lengthOfGoodItems):
                        #                        print("lengthOfEnemies=",lengthOfEnemies)
                        print("i=", i)
                        existElement = goodItems[i]
                        if collide(existElement, newElementGoodItem):
                            print("SBLUSUK s element", i)
                            hasCollide = True
                            break

                    if hasCollide == False:
                        #                goodItems.append(goodItem)
                        print("DOBAVQ ELEMENT")
                        newElementFalsePosition = False
                    else:
                        newElementGoodItem = GoodItem(random.randint(50, screen_width - 50), random.randint(-1500, -50), goodItem_obs_width, goodItem_obs_height, random.choice(["fuel", "repair"]))
                        print("Generira nov goodItem")

            start_ticks_goodItem = ticks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if j == screen_width:
            screen.blit(background, (0, j - screen_height))
            j = 0
        j += 2

        key = pygame.key.get_pressed()
        playerCar1.car_img = playerCarImage1
        # player 1 key move
        if key[pygame.K_a] and playerCar1.x > 0:
            playerCarImage1 = pygame.transform.scale(playerCarImage1, (playerCarImage1_width, playerCarImage1_height))
            playerCar1.x -= playerCar1_velocity
            playerCar1.car_img = leftPlaneImg
        if key[pygame.K_d] and playerCar1.x < screen_width - playerCarImage1_width:
            playerCar1.x += playerCar1_velocity
            playerCar1.car_img = rightPlaneImg
        if key[pygame.K_w] and playerCar1.y > 0:
            playerCar1.y -= playerCar1_velocity
        if key[pygame.K_s] and playerCar1.y < screen_height - playerCarImage1_height - 15:
            playerCar1.y += playerCar1_velocity
        if key[pygame.K_SPACE]:
            playerCar1.shoot()
        if key[pygame.K_x] and key[pygame.K_s]:
            playerCar1.y += playerCar1_velocity + boost_player
        if key[pygame.K_x] and key[pygame.K_w]:
            playerCar1.y -= playerCar1_velocity + boost_player


        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_rockets(rocket_vel, playerCar1)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            if collide(enemy, playerCar1):
                playerCar1.health -= 10
                enemies.remove(enemy)
            elif enemy.y > screen_height:
                lives -= 1
                enemies.remove(enemy)

        for goodItem in goodItems:
            goodItem.move(goodItem_vel)

            if collide(goodItem, playerCar1):
                if goodItem.car_img == repairIcon:
                    if playerCar1.health < 100:
                        playerCar1.health += 20

                if goodItem.car_img == fuelIcon:
                    if playerCar1.fuel < 500:
                        playerCar1.fuel += 30

                goodItems.remove(goodItem)

            elif goodItem.y > screen_height:
                goodItems.remove(goodItem)


        playerCar1.move_rockets(-rocket_vel, enemies)

        pygame.display.update()

def main_menu(playerCarImage1):
    run = True
    while run:
        screen.blit(background, (0,0))
        draw_text(screen, "Press mouse to begin...", 70, screen_width / 2 + 10, 270)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main(playerCarImage1)

    pygame.quit()

main_menu(playerCarImage1)
"""

player_1 = pygame.image.load("image/car_1.jpg").convert_alpha()
width_player_1_car = 40
height_player_1_car = 100
player_1 = pygame.transform.scale(player_1, (width_player_1_car, height_player_1_car))
pygame.draw.rect(player_1, pygame.rect(0, 0, width_player_1_car, height_player_1_car))
player_1.rect = player_1.image.get_rect()

player_2 = pygame.image.load("image/car_7.png").convert_alpha()
width_player_2_car = 40
height_player_2_car = 100
player_2 = pygame.transform.scale(player_2, (width_player_2_car, height_player_2_car))
pygame.draw.rect(player_2, pygame.Rect(0, 0, width_player_2_car, height_player_2_car))
player_2.rect = player_2.image.get_rect()

obs_pic = ""
font_name = pygame.font.match_font("arial")

FPS = 60
player_vel_1 = 10
clock = pygame.time.Clock()
x_pl_1 = 200
y_pl_1 = 400

player_vel_2 = 10
x_pl_2 = 400
y_pl_2 = 400

obs_speed = 3
obs_width = 40
obs_height = 100

max_index_obs = int(20)
obs_x = [0]*max_index_obs
obs_y = [0]*max_index_obs
obs_visible = []
obs_fileName = ["","","","",""]
obs_type = [0,0,0,0,0,0,0]


background_speed = int(2.5)
current_score_pl_1 = int(0)
current_score_pl_2 = int(0)
high_score_pl_1 = int(7)
high_score_pl_2 = int(8)
index_of_array = int(0)

game_over_player_1 = False
game_over_player_2 = False

mixer.music.load('music/backgroundMusic.mp3')

def redraw_window(j,x_pl_1,y_pl_1,x_pl_2,y_pl_2, ticks):
    #screen.fill((0,0,0))
    screen.blit(bg, (0, j))
    screen.blit(bg, (0, j - height_screen ))
    screen.blit(player_1, (x_pl_1, y_pl_1))
    screen.blit(player_2, (x_pl_2, y_pl_2))

    for i in range(0,max_index_obs):
        if obs_visible[i] == True:
            obs_pic = pygame.image.load(obs_fileName[i]).convert_alpha()
            pygame.draw.rect(obs_pic, pygame.Rect(0, 0, obs_width, obs_height))
            obs_pic.rect = obs_pic.image.get_rect()
            #obs_pic = pygame.transform.scale(obs_fileName[i], (obs_width, obs_height))
            obs_pic = pygame.transform.scale(obs_pic , (obs_width, obs_height))
            screen.blit( obs_pic, (obs_x[i], obs_y[i]))
            draw_text(screen, i, 18, obs_x[i]+10, obs_y[i]+10)
            obs_y[i] += obs_speed
            if (obs_y[i] >= height_screen - 0 and obs_y[i] <= (height_screen + 200)):
                obs_visible[i] = False

    draw_text(screen, "Time:", 18, width_screen - 570, height_screen - 300)
    draw_text(screen, round(ticks / 10), 18, width_screen - 540, height_screen - 300)

    draw_text(screen, "Score player 1:", 18, width_screen - 540, height_screen - 580)
    draw_text(screen, str(current_score_pl_1), 18, width_screen - 480, height_screen - 580)

    draw_text(screen, "Score player 2:", 18, width_screen - 80, height_screen - 580)
    draw_text(screen, str(current_score_pl_2), 18, width_screen - 30, height_screen - 580)

    pygame.display.update()

def new_obstacles ():
    # Search for free index
    i = int(0)
    while obs_visible[i] != False and i < max_index_obs:
        i+=1
    first_free_index = i
    index_of_array = i

    print("first_free_index=",first_free_index)
    print("NEW CAR+++++++++++++++++++++++++++++++++++++++++++++++NEW CAR")

    obs_x[first_free_index] = random.randint(0,width_screen - 100)
    obs_y[first_free_index] = -(obs_height)
    obs_visible[first_free_index] = True
    obs_type[first_free_index] = random.randint(1,5)
    obs_type[first_free_index] = random.randint(1,5)

    if obs_type[first_free_index] == 1:
        obs_fileName[first_free_index] = "image/car_1.jpg"
    elif obs_type[first_free_index] == 2:
        obs_fileName[first_free_index] = "image/enemyCar.jfif"
    elif obs_type[first_free_index] == 3:
        obs_fileName[first_free_index] = "image/diamond.jfif"
    elif obs_type[first_free_index] == 4:
        obs_fileName[first_free_index] = "image/diamond_2.jfif"
    elif obs_type[first_free_index] == 5:
        obs_fileName[first_free_index] = "image/lamborghini.png"
    pygame.display.update()

def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(str(text), True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
    #pygame.display.update()


def crash(x_pl_1,y_pl_1,x_pl_2,y_pl_2):
    # check conditions
    global current_score_pl_1,current_score_pl_2
    global game_over_player_1, game_over_player_2

    for i in range(0, max_index_obs):

        if obs_visible[i] == True:

            if (y_pl_1 + height_player_1_car) > obs_y[i] and y_pl_1 < (obs_y[i] + obs_height):
                if ((x_pl_1 > obs_x[i] and x_pl_1 < (obs_x[i] + obs_width)) or ((x_pl_1 + width_player_1_car) > obs_x[i]  and (x_pl_1 + width_player_1_car) < (obs_x[i] + obs_width))):

                    if obs_type[i] == 1:   # crash with enemy
                        game_over_player_1 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 2:  # crash with enemy
                        game_over_player_1 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 3: # get diamond
                        current_score_pl_1 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 4:  # get diamond 2
                        current_score_pl_1 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 5:  # crash with enemy
                        game_over_player_1 = True
                        game_over(game_over_player_1, game_over_player_2)
                        
            if (y_pl_2 + height_player_2_car) > obs_y[i] and y_pl_2 < (obs_y[i] + obs_height):

                if ((x_pl_2 > obs_x[i] and x_pl_2 < (obs_x[i] + obs_width)) or ((x_pl_2 + width_player_2_car) > obs_x[i]  and (x_pl_2 + width_player_2_car) < (obs_x[i] + obs_width))):

                    if obs_type[i] == 1:   # crash with enemy
                        game_over_player_2 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 2:  # crash with enemy
                        game_over_player_2 = True
                        game_over(game_over_player_1, game_over_player_2)
                    elif obs_type[i] == 3: # get diamond
                        current_score_pl_2 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 4:  # get diamond
                        current_score_pl_2 += 1
                        obs_visible[i] = False
                    elif obs_type[i] == 5:  # crash with enemy
                        game_over_player_2 = True
                        game_over(game_over_player_1, game_over_player_2)
                    if pygame.sprite.spritecollideany(player_1, obs_pic):
                        print("Udar pri PL1")


def show_go_screen():
    with open("score.txt", "r") as file:
        global high_score_pl_1
        global high_score_pl_2
        content = file.readlines()
        high_score_pl_1 = int(content[5])
        high_score_pl_2 = int(content[7])

    for i in range(0, max_index_obs):
        obs_visible.append(False)

    draw_text(screen, "Play survival cars!", 68, width_screen / 2, height_screen / 6)
    draw_text(screen, "Press any key to begin again", 24, width_screen / 2, height_screen - 100)

    mainScreenImage = pygame.image.load("image/mainScreenImage.jpg")
    mainScreenImage = pygame.transform.scale(mainScreenImage, (200, 200))
    screen.blit(mainScreenImage, (width_screen-400, height_screen-400))
    pygame.display.flip()
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                 waiting = False
                 mixer.music.play(-1)

def game_over(game_over_player_1, game_over_player_2):
    mixer.music.stop()

    screen.fill((0, 0,0))

    winImage = pygame.image.load("image/winImage.jpg")
    winImage = pygame.transform.scale(winImage, (200, 200))

    loseImage = pygame.image.load("image/loseImage.jpg")
    loseImage = pygame.transform.scale(loseImage, (200, 200))
    if game_over_player_1 == True:
        draw_text(screen, "Player 1 LOST", 30, width_screen - 440, height_screen - 500)
        screen.blit(loseImage, (width_screen - 550, height_screen - 400))
    else:
        draw_text(screen, "Player 1 WIN", 30, width_screen - 440, height_screen - 500)
        screen.blit(winImage, (width_screen - 550, height_screen - 400))

    if  game_over_player_2 == True:
        draw_text(screen, "Player 2 LOST", 30, width_screen - 180, height_screen - 500)
        screen.blit(loseImage, (width_screen - 250, height_screen - 400))
    else:
        draw_text(screen, "Player 2 WIN", 30, width_screen - 180, height_screen - 500)
        screen.blit(winImage, (width_screen - 250, height_screen - 400))

    draw_text(screen, "Press any key to exit", 24, width_screen / 2, height_screen - 100)

    pygame.display.flip()
    pygame.display.update()

    with open("score.txt", "w") as file:
        file.write("Current score player 1:" + "\n" + str(current_score_pl_1) + "\n")
        file.write("Current score player 2:" + "\n" + str(current_score_pl_2) + "\n")
        if int(high_score_pl_1) < current_score_pl_1:
            file.write("High score player 1:" + "\n" + str(current_score_pl_1) + "\n")
        else:
            file.write("High score player 1:" + "\n" + str(high_score_pl_1) + "\n")
        if int(high_score_pl_2) < current_score_pl_2:
            file.write("High score player 2:" + "\n" + str(current_score_pl_2) + "\n")
        else:
            file.write("High score player 2:" + "\n" + str(high_score_pl_2) + "\n")

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
                sys.exit()

def main(x_pl_1,y_pl_1,x_pl_2,y_pl_2,game_over_player_1,game_over_player_2):

    j = int(0)

# start of init
    show_go_screen()
# end of init
    running = True
    spawn_interval  = 30
    start_ticks = round(pygame.time.get_ticks()/100)
    while running:

        ticks = round(pygame.time.get_ticks()/100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        redraw_window(j,x_pl_1,y_pl_1,x_pl_2,y_pl_2,ticks)

        if ticks-start_ticks > spawn_interval:
            new_obstacles()
            start_ticks = ticks

        if y_pl_1 > height_screen:
            game_over_player_1 = True
            game_over(game_over_player_1, game_over_player_2)
        if y_pl_2 > height_screen:
            game_over_player_2 = True
            game_over(game_over_player_1, game_over_player_2)



        if j == width_screen:
            screen.blit(bg, (0, j - height_screen ))

            j = 0
        j += 2
        y_pl_1 += background_speed
        y_pl_2 += background_speed
        clock.tick(FPS)

        key = pygame.key.get_pressed()

        #player 1 key move
        if key[pygame.K_a] and x_pl_1 > 0:
            x_pl_1 -= player_vel_1
        if key[pygame.K_d] and x_pl_1 < width_screen - width_player_1_car:
            x_pl_1 += player_vel_1
        if key[pygame.K_w] and y_pl_1 > 0:
            y_pl_1 -= player_vel_1
        if key[pygame.K_s] and y_pl_1  < height_screen:
            y_pl_1 += player_vel_1

        # player 2 key move
        if key[pygame.K_LEFT] and x_pl_2 > 0:
            x_pl_2 -= player_vel_2
        if key[pygame.K_RIGHT] and x_pl_2 + width_player_2_car < width_screen:
            x_pl_2 += player_vel_2
        if key[pygame.K_UP] and y_pl_2 > 0:
            y_pl_2 -= player_vel_2
        if key[pygame.K_DOWN] and y_pl_2:
            y_pl_2 += player_vel_2

        crash(x_pl_1,y_pl_1, x_pl_2,y_pl_2)

        if (current_score_pl_1+current_score_pl_2) <= 4:
            spawn_interval = 30
        elif (current_score_pl_1 + current_score_pl_2) <= 6:
            spawn_interval = 25
        elif (current_score_pl_1 + current_score_pl_2) <= 8:
            spawn_interval = 18
        elif (current_score_pl_1 + current_score_pl_2) <= 10:
            spawn_interval = 12
        else:
            spawn_interval = 8



    pygame.quit()

main(x_pl_1,y_pl_1,x_pl_2,y_pl_2,game_over_player_1,game_over_player_2)
"""