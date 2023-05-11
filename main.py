import pygame
from sys import exit


class Roomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft = (0,0))
        self.speed = 5
        self.angle = 0
        self.direction = 's'
        self.score = 0
        pygame.draw.circle(self.image, (0, 0, 0), self.rect.center, radius)
        pygame.draw.circle(self.image, (255, 255, 255), self.rect.center, 25)
        pygame.draw.circle(self.image, (0, 0, 0), self.rect.center, 15)
        pygame.draw.line(self.image, (0, 0, 0), (self.rect.left + 12, self.rect.bottom - 12), (self.rect.right - 12, self.rect.bottom - 12), 3)
        pygame.draw.circle(self.image, (255, 255, 255), self.rect.center, 5)

    def player_input(self, obstacles):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            #print('w')
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle) & obstacle.rect.collidepoint(self.rect.midtop): return
            self.rect.y -= self.speed
            self.direction = 'w'
        if keys[pygame.K_s]:
            #print('s')
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle) & obstacle.rect.collidepoint(self.rect.midbottom): return
            self.rect.y += self.speed
            self.direction = 's'
        if keys[pygame.K_a]:
            #print('a')
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle) & obstacle.rect.collidepoint(self.rect.midleft): return
            self.rect.x -= self.speed
            self.direction = 'a'
        if keys[pygame.K_d]:
            #print('d')
            for obstacle in obstacles:
                if self.rect.colliderect(obstacle) & obstacle.rect.collidepoint(self.rect.midright): return
            self.rect.x += self.speed
            self.direction = 'd'

    def apply_border(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.right >= width:self.rect.right = width
        if self.rect.bottom >= height: self.rect.bottom = height

    def animate(self):
        if self.direction == 's':
            if self.angle == 0:
                return
            if self.angle == 90:
                self.image = pygame.transform.rotate(self.image, -90)
                self.angle = 0
            if self.angle == 180:
                self.image = pygame.transform.rotate(self.image, -180)
                self.angle = 0
            if self.angle == 270:
                self.image = pygame.transform.rotate(self.image, -270)
                self.angle = 0
        if self.direction == 'w':
            if self.angle == 0:
                self.image = pygame.transform.rotate(self.image, 180)
                self.angle = 180
            if self.angle == 90:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 180
            if self.angle == 180:
                return
            if self.angle == 270:
                self.image = pygame.transform.rotate(self.image, -90)
                self.angle = 180
        if self.direction == 'a':
            if self.angle == 0:
                self.image = pygame.transform.rotate(self.image, 270)
                self.angle = 270
            if self.angle == 90:
                self.image = pygame.transform.rotate(self.image, 180)
                self.angle = 270
            if self.angle == 180:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 270
            if self.angle == 270:
                return
        if self.direction == 'd':
            if self.angle == 0:
                self.image = pygame.transform.rotate(self.image, 90)
                self.angle = 90
            if self.angle == 90:
                return
            if self.angle == 180:
                self.image = pygame.transform.rotate(self.image, -90)
                self.angle = 90
            if self.angle == 270:
                self.image = pygame.transform.rotate(self.image, -180)
                self.angle = 90


    def update(self, obstacles):
        self.player_input(obstacles)
        self.apply_border()
        self.animate()



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect


class Snack(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect

    def destroy(self):
        self.kill()


def collision_snack_sprite():
    for obstacle in obstacles.sprites():
        pygame.sprite.spritecollide(obstacle, snacks, True)


def roomba_eat_snack():
    snack_list = pygame.sprite.spritecollide(roomba.sprite, snacks, False)
    if snack_list:
        for snack in snack_list:
            snack.destroy()
    return len(snack_list)



pygame.init()
width = 800
height = 600
radius = 29
speed = 20
food = []
objects = []
score = 0.0


screen = pygame.display.set_mode((1000, height))
pygame.display.set_caption('Roomba')
clock = pygame.time.Clock()

display_score_surface = pygame.Surface((200, height))
display_score_surface.fill((122, 173, 172))



#font_score_img = font_score_text.render('Score: ' + str(score) + '%', True, (0,0,0))


display_surface = pygame.Surface((width, height))
display_surface.fill((252, 172, 152))

roomba_garage_surface = pygame.Surface((100, 100))
roomba_garage_surface.fill((128, 0, 128))
roomba_garage_rect = roomba_garage_surface.get_rect(topleft = (0,0))
objects.append(roomba_garage_rect)

tv_surface = pygame.Surface((40, 300))
tv_surface.fill((0, 0, 0))
tv_rect = tv_surface.get_rect(midleft = (0, height/2))
objects.append(tv_rect)

couch_surface = pygame.Surface((200,60))
couch_surface.fill((255, 100, 100))
couch_rect = couch_surface.get_rect(midtop = (width /2, 0))
objects.append(couch_rect)

couch_arm_1_surface = pygame.Surface((50,100))
couch_arm_1_surface.fill((255, 100, 100))
couch_arm_1_rect = couch_arm_1_surface.get_rect(topright = (width/2 - 100, 0))
objects.append(couch_arm_1_rect)

couch_arm_2_surface = pygame.Surface((50,100))
couch_arm_2_surface.fill((255, 100, 100))
couch_arm_2_rect = couch_arm_2_surface.get_rect(topleft = (width/2 + 100, 0))
objects.append(couch_arm_2_rect)

table_surface = pygame.Surface((250, 100))
table_surface.fill((165, 42, 42))
table_rect = table_surface.get_rect(center = (width/2, height/2))
objects.append(table_rect)

light_1_surface = pygame.Surface((100, 100))
light_1_surface.fill((165, 42, 42))
light_1_rect = light_1_surface.get_rect(topright = (width, 0))
objects.append(light_1_rect)

light_2_surface = pygame.Surface((100, 100))
light_2_surface.fill((165, 42, 42))
light_2_rect = light_2_surface.get_rect(bottomright = (width, height))
objects.append(light_2_rect)

other_couch_surface = pygame.Surface((200,60))
other_couch_surface.fill((255, 100, 100))
other_couch_rect = other_couch_surface.get_rect(midbottom = (width/2, height))
objects.append(other_couch_rect)

other_couch_arm_1_surface = pygame.Surface((50,100))
other_couch_arm_1_surface.fill((255, 100, 100))
other_couch_arm_1_rect = other_couch_arm_1_surface.get_rect(bottomright = (width/2 -100, height))
objects.append(other_couch_arm_1_rect)

other_couch_arm_2_surface = pygame.Surface((50,100))
other_couch_arm_2_surface.fill((255, 100, 100))
other_couch_arm_2_rect = other_couch_arm_2_surface.get_rect(bottomleft = (width/2 +100, height))
objects.append(other_couch_arm_2_rect)

roomba_surface = pygame.Surface((60, 60))
roomba_surface = roomba_surface.convert_alpha()
roomba_surface.fill((0, 0, 0, 0))


roomba_rectangle = roomba_surface.get_rect(topleft = (10,10))

roomba = pygame.sprite.GroupSingle()
roomba.add(Roomba())

obstacles = pygame.sprite.Group()
obstacles.add(Obstacle(tv_surface, tv_rect))
obstacles.add(Obstacle(couch_surface, couch_rect))
obstacles.add(Obstacle(couch_arm_1_surface, couch_arm_1_rect))
obstacles.add(Obstacle(couch_arm_2_surface, couch_arm_2_rect))
obstacles.add(Obstacle(table_surface, table_rect))
obstacles.add(Obstacle(light_1_surface, light_1_rect))
obstacles.add(Obstacle(light_2_surface, light_2_rect))
obstacles.add(Obstacle(other_couch_surface, other_couch_rect))
obstacles.add(Obstacle(other_couch_arm_1_surface, other_couch_arm_1_rect))
obstacles.add(Obstacle(other_couch_arm_2_surface, other_couch_arm_2_rect))

snacks = pygame.sprite.Group()


def update_score(snacks):
    eaten = 205 - len(snacks)
    score = (eaten / 205) * 100
    print(score)


for i in range(20, width, 40):
    for j in range(20, height, 40):
        snack = (i, j)
        food.append(snack)

for snack in food:
    snack_surface = pygame.Surface((40, 40))
    snack_surface.fill((255, 255, 255))
    snack_rect = snack_surface.get_rect(center = (snack[0], snack[1]))
    snacks.add(Snack(snack_surface, snack_rect))

print(snacks)
print(food)
print(len(food))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # do all the stufs
    font = pygame.font.Font(None, 36)
    screen.blit(display_surface, (0, 0))
    screen.blit(roomba_garage_surface, (0, 0))
    screen.blit(display_score_surface, (width, 0))
    score_text = font.render(f'Score: {score} %', True, (255, 255, 255))
    screen.blit(score_text, (width + 20, 20))

    obstacles.draw(screen)
    obstacles.update()

    snacks.draw(screen)
    snacks.update()

    roomba.draw(screen)
    roomba.update(obstacles)

    collision_snack_sprite()
    roomba_eat_snack()

    update_score(snacks)

    pygame.display.update()
    clock.tick(30)
    #run = False

