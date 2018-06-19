import pygame, random, time
from math import sin, cos

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
vector = pygame.math.Vector2

sprites = []

def get_int(vect):
    return (int(vect.x), int(vect.y))

def explosion(pos):
    for i in range(20):
        particle(pos, (random.randint(-5, 5) / 4, random.randint(-5, 5) / 4), 1)

def intro():
    screen.fill((0, 0, 0))
    time.sleep(1)
    p_lists = [
        [(0, 0), (15, 0), (20, 5), (20, 15), (15, 20), (0, 20)],
        [(20, 0), (35, 0), (40, 5), (40, 20), (25, 20), (20, 15)],
        [(40, 0), (48, 0), (48, 2), (50, 0), (60, 0), (60, 5), (55, 10), (60, 15), (60, 20), (50, 20), (48, 18), (48, 20), (40, 20)],
        [(60, 0), (60, 20), (80, 20), (80, 10), (75, 10), (80, 10), (80, 5), (75, 5), (80, 5), (80, 0)],
        [(80, 0), (95, 0), (100, 5), (100, 20), (90, 20), (90, 7), (90, 20), (80, 20)],
        [(105, 0), (120, 0), (120, 10), (110, 10), (110, 13), (110, 10), (120, 10), (120, 15), (115, 20), (100, 20), (100, 5)],
        [(120, 0), (130, 0), (130, 10), (130, 0), (140, 0), (140, 15), (135, 20), (125, 20), (120, 15)],
        [(140, 0), (150, 0), (150, 5), (150, 0), (160, 0), (160, 10), (155, 15), (155, 20), (145, 20), (145, 15), (140, 10)]]
    for i in p_lists:
        pygame.draw.lines(screen, WHITE, True, [vector(x) + (160, 150) for x in i])
    pygame.display.flip()
    time.sleep(1)


class ship:

    def __init__(self, pos):
        self.pos = vector(pos)
        self.model = [
            [(-15, 0), (8, 13), (10, 0), (8, -13)],
            [(0, 1), (1, 2), (2, 3), (3, 0)]]
        self.dir = vector(0, 1)
        self.vel = vector(0, 0)
        self.health = 255

    def draw(self):
        global mouse_pos
        for i in range(round(self.pos.distance_to(mouse_pos) / 5)):
            pygame.draw.circle(screen, RED, get_int(self.pos - (5 * (self.dir * 6 - self.vel / 3).normalize()) * i), 0)
            pygame.draw.circle(screen, WHITE, get_int(self.pos - 5 * (self.dir).normalize() * i), 0)
        for l in self.model[1]:
            v = vector(self.model[0][l[0]]); z = vector(self.model[0][l[1]])
            pygame.draw.line(screen, (255, self.health, round(self.health / 16, 1)**2),
                             (v.x * self.dir.x - v.y * self.dir.y + self.pos.x, v.y * self.dir.x + v.x * self.dir.y + self.pos.y),
                             (z.x * self.dir.x - z.y * self.dir.y + self.pos.x, z.y * self.dir.x + z.x * self.dir.y + self.pos.y))

    def update(self):
        global mouse_buttons, mouse_pos, global_counter
        if mouse_buttons[2]:
            self.vel -= self.dir / 5
            if global_counter % 6 == 0:
                particle(self.pos + (random.randint(-10, 10), random.randint(-5, 5)) + 15 * self.dir, self.dir + self.vel)
        if mouse_buttons[1]:
            self.vel /= 1.1
        t.dir = vector(t.pos - mouse_pos).normalize()
        self.pos += self.vel
        if not screen.get_rect().collidepoint(self.pos):
            temp = self.pos
            temp -= (240, 160)
            temp = temp * -.98
            temp += (240, 160)
            self.pos = temp

class enemy:

    def __init__(self, pos):
        self.pos = vector(pos)
        self.model = [
            [(0, 0), (-16, 5), (15, 16), (15, -16), (-16, -5)],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]]
        self.dir = vector(0, 1)
        self.vel = vector(0, 0)
        sprites.append(self)

    def draw(self):
        self.dir = (self.pos - t.pos).normalize()
        self.vel = -self.dir
        self.pos += self.vel
        for s in sprites:
            if type(s) == projectile and self.pos.distance_to(s.pos) <= 20:
                explosion(self.pos)
                sprites.remove(self)
                sprites.remove(s)
                for i in range(5):
                    coin(self.pos)
        for l in self.model[1]:
            v = vector(self.model[0][l[0]]); z = vector(self.model[0][l[1]])
            pygame.draw.line(screen, WHITE,
                             (v.x * self.dir.x - v.y * self.dir.y + self.pos.x, v.y * self.dir.x + v.x * self.dir.y + self.pos.y),
                             (z.x * self.dir.x - z.y * self.dir.y + self.pos.x, z.y * self.dir.x + z.x * self.dir.y + self.pos.y))


class particle:

    def __init__(self, pos, vel, auto=0):
        self.pos = vector(pos)
        self.vel = vector(vel)
        self.counter = 0
        if not auto:
            self.r = random.randint(0, 1)
        else:
            self.r = auto - 1
        sprites.append(self)

    def draw(self):
        self.pos += self.vel
        self.counter += 1
        if self.counter >= random.randint(20, 30):
            sprites.remove(self)
        if self.r:
            pygame.draw.rect(screen, WHITE, (self.pos, (3, 3)), 1)
        else:
            screen.set_at(get_int(self.pos), WHITE)

class projectile:

    def __init__(self, pos, vel):
        self.pos = vector(pos)
        self.vel = vector(vel)
        self.pos += self.vel
        self.dir = self.vel.normalize()
        self.model = [
            [(-20, 0), (0, 1), (1, 0), (0, -1)],
            [(0, 1), (1, 2), (2, 3), (3, 0)]]
        sprites.append(self)

    def draw(self):
        self.pos += self.vel
        if not screen.get_rect().collidepoint(self.pos):
            sprites.remove(self)
        for i in [b for b in sprites if type(b) == box]:
            if i.rect.collidepoint(self.pos):
                sprites.remove(self)
                if i.dest:
                    sprites.remove(i)
                    explosion(i.rect.center)
        for l in self.model[1]:
            v = vector(self.model[0][l[0]]); z = vector(self.model[0][l[1]])
            pygame.draw.line(screen, WHITE,
                             (v.x * self.dir.x - v.y * self.dir.y + self.pos.x, v.y * self.dir.x + v.x * self.dir.y + self.pos.y),
                             (z.x * self.dir.x - z.y * self.dir.y + self.pos.x, z.y * self.dir.x + z.x * self.dir.y + self.pos.y))

class coin:

    def __init__(self, pos):
        self.pos = vector(pos) + (random.randint(-20, 20), random.randint(-20, 20))
        self.vel = vector(0, 0)
        sprites.append(self)

    def draw(self):
        self.vel = 100 * (t.pos - self.pos).normalize() / self.pos.distance_squared_to(t.pos)
        self.pos += self.vel
        if self.pos.distance_to(t.pos) < 15:
            sprites.remove(self)
            t.health += 5
            if t.health > 255:
                t.health = 255
        pygame.draw.circle(screen, GREEN, get_int(self.pos), 2)

class box:

    def __init__(self, rect, destructible=False):
        self.rect = pygame.Rect(rect)
        sprites.append(self)
        self.dest = destructible

    def draw(self):
        if self.dest:
            pygame.draw.line(screen, WHITE, self.rect.topleft, self.rect.bottomright - vector(1, 1))
            pygame.draw.line(screen, WHITE, self.rect.topright - vector(1, 0), self.rect.bottomleft - vector(0, 1))
        pygame.draw.rect(screen, WHITE, self.rect, 1)

        
screen1 = [
    "0 112 32 1110 1",
    "              3",
    "1            3 ",
    "o             1",
    "o  o        2 1",
    "o        x   0 ",
    "o              ",
    "1             1",
    "0     1       3",
    "  14  2 112 11 ",]

for y in range(10):
    for x in range(15):
        if screen1[y][x] == '0':
            box((x * 32, y * 32, 64, 64))
        if screen1[y][x] == '1':
            box((x * 32, y * 32, 32, 32))
        if screen1[y][x] == '2':
            box((x * 32, y * 32, 64, 32))
        if screen1[y][x] == '3':
            box((x * 32, y * 32, 32, 64))
        if screen1[y][x] == '4':
            box((x * 32, y * 32, 96, 32))
        if screen1[y][x] == 'o':
            box((x * 32, y * 32, 32, 32), True)
        if screen1[y][x] == 'x':
            enemy((x * 32, y * 32))



pygame.init()

size = (480, 320)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("vector")

intro()

t = ship((100, 100))

done = False
clock = pygame.time.Clock()
global_counter = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                projectile(t.pos, t.vel / 3 + t.dir * -8)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                explosion(t.pos)
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill(BLACK)

    t.update()
    t.draw()

    for s in sprites:
        s.draw()
    print(len(sprites))
    
    pygame.display.flip()
    clock.tick(60)
    global_counter += 1
pygame.quit()
