import pygame
import random
import math

#----------------------------------------------------------------------------- setting up pygame display
bg = (255, 255, 255)
(width, height) =  (800, 800)
screen = pygame.display.set_mode((width, height))
screen.fill(bg)


#---------------------------------------------------- vectors and gravity

def addVectors(angle1, length1, angle2, length2):

    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = math.pi / 2 - math.atan2(y, x)

    return (angle, length)

gravity = 0.02
gravity_angle = math.pi
elasticity = 0.999


#---------------------------------------------------- mouse interactions

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None

#---------------------------------------------------- collisions

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    if math.hypot(dx, dy) < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass
        dist = math.hypot(dx, dy)

        a1 = p1.angle
        a2 = angle
        a3 = p2.angle
        a4 = angle + math.pi

        l1 = p1.speed * (p1.mass-p2.mass)/total_mass
        l2 = 2 * p2.speed * p2.mass/total_mass
        l3 = p2.speed * (p2.mass-p1.mass)/total_mass
        l4 = 2 * p1.speed*p1.mass/total_mass

        p1.angle, p1.speed = addVectors(a1, l1, a2, l2)
        p2.angle, p2.speed = addVectors(a3, l3, a4, l4 )

        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - dist + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap



#----------------------------------------------------------------------------- creating a particle class

class Particle():
    def __init__(self, x, y, size, mass = 1):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

#---------------------------------------------------- movement and collisions
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

        self.angle, self.speed = addVectors(self.angle, self.speed, gravity_angle, gravity)

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle

        self.speed *= elasticity

#----------------------------------------------------------------------------- placing random particles

number_of_particles = 5

my_particles = []


for n in range(number_of_particles):
    size = random.randint(10, 20)
    density = random.randint(1, 20)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)

    particle = Particle(x, y, size, density * size ** 2)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

#-----------------------------------------------------------------------------
selected_particle = None



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(bg)

    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i + 1:]:
            collide(particle, particle2)
        particle.display()
    pygame.display.flip()
