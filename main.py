import pygame, math, random, operator
from pygame.locals import (
    K_ESCAPE,
    K_SPACE,
    K_q,
    K_w,
    K_e,
    K_a,
    K_s,
    K_d,
    K_f,
    K_g,
    K_c,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_k,
    K_l,
    K_p,
    K_o,
    K_x,
    K_COMMA,
    K_PERIOD,
    K_EQUALS,
    K_MINUS,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_PAGEUP,
    K_PAGEDOWN,
    KEYDOWN,
    QUIT
)
from operator import attrgetter

# initial window information and constants
# width height and center values
WIDTH = 2000
HEIGHT = 1200
ORIGINX = WIDTH / 2
ORIGINY = HEIGHT / 2

# camera distance from screen
FOCALLENGTH = 1200

# pi used in rotation and sphere calculations
PI = math.pi


# returns a random number between -a and a, used to make random coordinates
def randInt(a):
    return random.randint(-a, a)


# returns a cube wireframe with side lengths of dist, whose center point is given by center [x,y,z]
def cubePoints(dist, center):
    # define vertices/points
    a = Point(-dist / 2 + center.x, -dist / 2 + center.y, -dist / 2 + center.z)
    b = Point(dist / 2 + center.x, -dist / 2 + center.y, -dist / 2 + center.z)
    c = Point(-dist / 2 + center.x, dist / 2 + center.y, -dist / 2 + center.z)
    d = Point(-dist / 2 + center.x, -dist / 2 + center.y, dist / 2 + center.z)
    e = Point(dist / 2 + center.x, dist / 2 + center.y, -dist / 2 + center.z)
    f = Point(dist / 2 + center.x, -dist / 2 + center.y, dist / 2 + center.z)
    g = Point(-dist / 2 + center.x, dist / 2 + center.y, dist / 2 + center.z)
    h = Point(dist / 2 + center.x, dist / 2 + center.y, dist / 2 + center.z)
    points = [a, b, c, d, e, f, g, h]

    # define edges/lines
    ab = Line(points[0], points[1])
    ac = Line(points[0], points[2])
    ad = Line(points[0], points[3])
    be = Line(points[1], points[4])
    bf = Line(points[1], points[5])
    ce = Line(points[2], points[4])
    cg = Line(points[2], points[6])
    df = Line(points[3], points[5])
    dg = Line(points[3], points[6])
    eh = Line(points[4], points[7])
    fh = Line(points[5], points[7])
    gh = Line(points[6], points[7])
    lines = [ab, ac, ad, be, bf, ce, cg, df, dg, eh, fh, gh]

    return Shape(lines, center=center)


# returns an equilateral tetrahedron with height of dist, whose center point is given by center [x,y,z]
def tetraPoints(dist, center):
    # define vertices/points
    a = Point(dist / 2 + center.x, dist / 2 + center.y, dist / 2 + center.z)
    b = Point(dist / 2 + center.x, -dist / 2 + center.y, -dist / 2 + center.z)
    c = Point(-dist / 2 + center.x, dist / 2 + center.y, -dist / 2 + center.z)
    d = Point(-dist / 2 + center.x, -dist / 2 + center.y, dist / 2 + center.z)
    points = [a, b, c, d]

    # define edges/lines
    ab = Line(points[0], points[1])
    ac = Line(points[0], points[2])
    ad = Line(points[0], points[3])
    bc = Line(points[1], points[2])
    bd = Line(points[1], points[3])
    cd = Line(points[2], points[3])
    lines = [ab, ac, ad, bc, bd, cd]
    return Shape(lines, center=center)


# returns an equilateral octahedron with height of dist, whose center point is given by center [x,y,z]
def octagPoints(dist, center):
    # define vertices/points
    a = Point(center.x, dist / 2 + center.y, center.z)
    b = Point(center.x, -dist / 2 + center.y, center.z)
    c = Point(dist / 2 + center.x, center.y, center.z)
    d = Point(-dist / 2 + center.x, center.y, center.z)
    e = Point(center.x, center.y, dist / 2 + center.z)
    f = Point(center.x, center.y, -dist / 2 + center.z)

    points = [a, b, c, d, e, f]

    # define edges/lines
    ac = Line(points[0], points[2])
    ad = Line(points[0], points[3])
    ae = Line(points[0], points[4])
    af = Line(points[0], points[5])
    bc = Line(points[1], points[2])
    bd = Line(points[1], points[3])
    be = Line(points[1], points[4])
    bf = Line(points[1], points[5])
    ce = Line(points[2], points[4])
    cf = Line(points[2], points[5])
    de = Line(points[3], points[4])
    df = Line(points[3], points[5])
    lines = [ac, ad, ae, af, bc, bd, be, bf, cf, ce, de, df]
    return Shape(lines, center=center)


# returns a sphere wireframe, defined by two angles tta and phi. sphere is made of horizontal and vertical lines like a globe, whose center point is given by center [x,y,z]
def spherePoints(dist, center, tta, phi):  # makes tta (minimum 2) rings of 2x phi (minimum 1) points
    pp = []  # list of point rings
    lines = []  # list of all lines

    # ring points loop
    an1 = 0
    while an1 <= PI:
        points = []
        # horizontal ring loop
        an2 = 0
        while an2 <= 2 * PI:
            # sphere point calculation
            x = center.x + dist / 2 * math.sin(an1) * math.cos(an2)
            y = center.y + dist / 2 * math.sin(an1) * math.sin(an2)
            z = center.z + dist / 2 * math.cos(an1)
            points.append(Point(x, y, z))
            an2 += PI / phi

        # connect horizontal points with lines
        j = 0
        lines.append(Line(points[0], points[-1]))
        while j + 1 < points.__len__():
            lines.append(Line(points[j], points[j + 1]))
            j += 1
        pp.append(points)
        an1 += PI / (tta - 1)

    # connect rings vertically
    i = 0
    while i + 1 < pp.__len__():
        j = 0
        while j < pp[i].__len__():
            lines.append(Line(pp[i][j], pp[i + 1][j]))
            j += 1
        i += 1

    # make shape object in case extra of translation
    shape = Shape(lines, center=center)

    # rotate default sphere for visual aid
    shape.rotate(ax='y', theta=PI / 6)
    shape.rotate(ax='z', theta=PI / 6)

    return shape

# returns a complex shape, specifically a 3x3x3 of cubes, centered by the given center point
def cubix(dist, center):
    shapes = []

    # loop to create 27 cubes in a 3x3x3 grid
    j = 0
    while j < 27:
        jx = j % 3 - 1
        jy = int((j % 9) / 3) - 1
        jz = int(j / 9) - 1
        j += 1
        if abs(jx) + abs(jy) + abs(jz) >= 2:
            shapes.append(cubePoints(dist, Point(jx * dist, jy * dist, jz * dist)))

    # remove redundant lines from the collective of cubes
    ls = []
    for shape in shapes:
        for line in shape.lines:
            if not ls.__contains__(line):
                ls.append(line)

    # create a single shape with the same vertices and edges as the 27 base shapes
    shapes = [Shape(ls, center=center)]
    return shapes


# Classes
# Point defined by a x,y,z coordinates, a dot size, and a color. inherits the sprite class to be displayed on the screen
class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, z, width=10, color=(255, 255, 255)):
        super(Point, self).__init__()
        self.color = color
        self.width = width
        self.surf = pygame.Surface((self.width, self.width), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        pygame.draw.circle(self.surf, self.color, (self.width / 2, self.width / 2), self.width / 2)
        self.x = x
        self.y = y
        self.z = z
        self.dx = self.x * FOCALLENGTH / (self.z + FOCALLENGTH)
        self.dy = self.y * FOCALLENGTH / (self.z + FOCALLENGTH)
        self.rect = self.surf.get_rect(center=((ORIGINX + self.dx), (ORIGINY - self.dy)))

    # moves the sprite rect to the new location (described as a coordinate with respect to the center of the screen, with 0,0 as the center)
    def relocate(self):
        self.rect = self.surf.get_rect(center=((ORIGINX + self.dx), (ORIGINY - self.dy)))

    # adds two points' values (vector addition)
    def add(self, point):
        self.move(Point(self.x + point.x, self.y + point.y, self.z + point.z))

    # subtracts two points' values (vector addition)
    def subtract(self, point):
        self.move(Point(self.x - point.x, self.y - point.y, self.z - point.z))

    def xy(self):
        return [self.x, self.y]

    def xyz(self):
        return [self.x, self.y, self.z]

    # changes the color of the point
    def colorize(self, color):
        self.color = color
        pygame.draw.circle(self.surf, self.color, (self.width / 2, self.width / 2), self.width / 2)

    # moves the point to a new point's location, re-altering scale for depth
    def move(self, point):
        self.x = point.x
        self.y = point.y
        self.z = point.z
        self.dx = self.x * FOCALLENGTH / (self.z + FOCALLENGTH)
        self.dy = self.y * FOCALLENGTH / (self.z + FOCALLENGTH)
        self.relocate()

    # rotates a point with respect to a given axis. 'x' = x axis, 'u' = reverse on x axis, 'y','v' = y and reverse, 'z','w' = z axis and reverse. rotated by an angle (default is pi/1000)
    def rotate(self, ax="y", theta=PI / 1000):
        # r is 3x3 matrix, defined for the specific type of rotation
        if ax == "x":
            r = [1, 0, 0,
                 0, math.cos(theta), math.sin(theta),
                 0, -math.sin(theta), math.cos(theta)]
        elif ax == "y":
            r = [math.cos(theta), 0, -math.sin(theta),
                 0, 1, 0,
                 math.sin(theta), 0, math.cos(theta)]
        elif ax == "z":
            r = [math.cos(theta), -math.sin(theta), 0,
                 math.sin(theta), math.cos(theta), 0,
                 0, 0, 1]
        elif ax == "u":
            r = [1, 0, 0,
                 0, math.cos(theta), -math.sin(theta),
                 0, math.sin(theta), math.cos(theta)]
        elif ax == "v":
            r = [math.cos(theta), 0, math.sin(theta),
                 0, 1, 0,
                 -math.sin(theta), 0, math.cos(theta)]
        elif ax == "w":
            r = [math.cos(theta), math.sin(theta), 0,
                 -math.sin(theta), math.cos(theta), 0,
                 0, 0, 1]
        else:
            r = [1, 0, 0,
                 0, 1, 0,
                 0, 0, 1]

        # multiply matrices
        xyz = [self.x, self.y, self.z]
        x = xyz[0] * r[0] + xyz[1] * r[1] + xyz[2] * r[2]
        y = xyz[0] * r[3] + xyz[1] * r[4] + xyz[2] * r[5]
        z = xyz[0] * r[6] + xyz[1] * r[7] + xyz[2] * r[8]
        nPoint = Point(x, y, z)
        self.move(nPoint)
        return nPoint

    # rotates a point around a point that is not the origin (same as rotate otherwise)
    def rotateInPlace(self, place, ax="y", theta=PI / 1000):
        if ax == "x":
            r = [1, 0, 0,
                 0, math.cos(theta), math.sin(theta),
                 0, -math.sin(theta), math.cos(theta)]
        elif ax == "y":
            r = [math.cos(theta), 0, -math.sin(theta),
                 0, 1, 0,
                 math.sin(theta), 0, math.cos(theta)]
        elif ax == "z":
            r = [math.cos(theta), -math.sin(theta), 0,
                 math.sin(theta), math.cos(theta), 0,
                 0, 0, 1]
        elif ax == "u":
            r = [1, 0, 0,
                 0, math.cos(theta), -math.sin(theta),
                 0, math.sin(theta), math.cos(theta)]
        elif ax == "v":
            r = [math.cos(theta), 0, math.sin(theta),
                 0, 1, 0,
                 -math.sin(theta), 0, math.cos(theta)]
        elif ax == "w":
            r = [math.cos(theta), math.sin(theta), 0,
                 -math.sin(theta), math.cos(theta), 0,
                 0, 0, 1]
        else:
            r = [1, 0, 0,
                 0, 1, 0,
                 0, 0, 1]

        # point is shifted to origin, rotated, and then shifted back
        xyz = [self.x - place.x, self.y - place.y, self.z - place.z]
        x = xyz[0] * r[0] + xyz[1] * r[1] + xyz[2] * r[2]
        y = xyz[0] * r[3] + xyz[1] * r[4] + xyz[2] * r[5]
        z = xyz[0] * r[6] + xyz[1] * r[7] + xyz[2] * r[8]
        x = x + place.x
        y = y + place.y
        z = z + place.z
        nPoint = Point(x, y, z)
        self.move(nPoint)
        return nPoint

    # scales a point's coordinates by a given number, point is scaled with respect to another given point
    def scalePoint(self, scale, place):
        r = [scale, 0, 0,
             0, scale, 0,
             0, 0, scale]

        # matrix multiplication
        xyz = [self.x - place.x, self.y - place.y, self.z - place.z]
        x = xyz[0] * r[0] + xyz[1] * r[1] + xyz[2] * r[2]
        y = xyz[0] * r[3] + xyz[1] * r[4] + xyz[2] * r[5]
        z = xyz[0] * r[6] + xyz[1] * r[7] + xyz[2] * r[8]
        x = x + place.x
        y = y + place.y
        z = z + place.z
        nPoint = Point(x, y, z)
        self.move(nPoint)
        return nPoint

# two points, and a length value
class Line:
    def __init__(self, p1, p2):
        self.point1 = p1
        self.point2 = p2
        self.length = self.length()

    def p1(self):
        return self.point1

    def p2(self):
        return self.point2

    # used to determine and get the segment length
    def length(self):
        x = self.p1().x - self.p2().x
        y = self.p1().y - self.p2().y
        z = self.p1().z - self.p2().z
        xy = math.sqrt(x * x + y * y)
        xyz = math.sqrt(xy * xy + z * z)
        return xyz

# a collection of lines, a center point, and a color define a shape, the vertices are gathered from the lines and saved.
class Shape(pygame.sprite.Sprite):
    def __init__(self, lines, center, color=(255, 255, 255)):
        super(Shape, self).__init__()
        self.color = color
        self.center = center
        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
        self.surf.fill((0, 0, 0))
        self.surf = self.surf.convert_alpha()
        self.lines = lines
        self.points = self.listPoints()
        self.rect = self.surf.get_rect(center=(ORIGINX, ORIGINY))
        self.redraw()

    # creates the initial list of vertex points contained in the shape, removing duplicates
    def listPoints(self):
        points = []
        for line in self.lines:
            if not points.__contains__(line.point1):
                points.append(line.point1)
            if not points.__contains__(line.point2):
                points.append(line.point2)
        return points

    # changes color of shape
    def colorize(self, color):
        for point in self.points:
            point.colorize(color)
        self.color = color

    # redraws a shape on the screen (refreshing the screen)
    def redraw(self):
        self.surf = self.surf.convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        for point in self.points:
            point.relocate()
        for line in self.lines:
            pygame.draw.line(self.surf, self.color, [ORIGINX + line.point1.dx, ORIGINY - line.point1.dy],
                             [ORIGINX + line.point2.dx, ORIGINY - line.point2.dy])

    # redraws a shape on the screen (without refreshing the screen, causing a smearing effect)
    def redraw2(self):
        for point in self.points:
            point.relocate()
        for line in self.lines:
            pygame.draw.line(self.surf, self.color, [ORIGINX + line.point1.dx, ORIGINY - line.point1.dy],
                             [ORIGINX + line.point2.dx, ORIGINY - line.point2.dy])

    # rotates a shape around the center of the screen by rotating each of its points and redefining the lines (see Point.rotate)
    def rotate(self, ax="y", theta=PI / 1000):
        self.center.rotate(ax, theta)
        for point in self.points:
            point.rotate(ax, theta)

    # rotates a shape around its center by rotating each of its points with respect to the center coordinate and redefining the lines (see Point.rotateInPlace)
    def rotateInPlace(self, ax="y", theta=PI / 1000):
        for point in self.points:
            point.rotateInPlace(place=self.center, ax=ax, theta=theta)

    # shifts a shape by a shift value [xShift, yShift, zShift] (using vector addition)
    def shift(self, shift):
        self.center.add(Point(shift[0], shift[1], shift[2]))
        for point in self.points:
            point.add(Point(shift[0], shift[1], shift[2]))

    # scales a shape by a scale factor with respect to the shape's center (see point.scale)
    def scale(self, scale):
        self.center.scalePoint(scale, self.center)
        for point in self.points:
            point.scalePoint(scale, place=self.center)


# Main Code
pygame.init()

# pygame screen definition
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((0, 0, 0))

# contains all sprites being drawn
all_sprites = pygame.sprite.Group()

# main loop variables
loop = True # determine when to stop
shapes = [] # all shapes being drawn (usually just one)

# keyboard input variables
q1 = False # is 'w' -z axis rotation
w1 = False # is 'x' axis rotation
e1 = False # is 'z' axis rotation
a1 = False # is 'v' -y axis rotation
s1 = False # is 'u' -x axis rotation
d1 = False # is 'y' axis rotation
q2 = False # in place q1 rotation
w2 = False # in place w1 rotation
e2 = False # in place e1 rotation
a2 = False # in place a1 rotation
s2 = False # in place s1 rotation
d2 = False # in place d1 rotation

p = True # show all points
o = True # redraw by refreshing
x = True # used to alter between 1 and 2 rotation, and speeds

speed = 1 # speed of axis rotation
speed2 = 1 # speed of in place rotation
theta = PI / 1000 # rotation based on speed
theta2 = PI / 1000 # in place rotation based on speed2

color = False # color cycling
cR = 1 # color r
cG = 1 # color b
cB = 1 # color g

# sphere generation vars
tta = 10
phi = 16

center = [0, 0, 0] # starting center value
dist = 200 # default size of shape

# screen drawing loop
while loop:
    # reinitialize surfaces
    screen.fill((0, 0, 0))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # get event data
    pressed_keys = pygame.key.get_pressed()

    # check event data
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                loop = False
            if event.key == K_SPACE:  # refresh conditions
                speed = 1
                speed2 = 1
                theta = PI / 1000
                theta2 = PI / 1000
                q1 = False
                w1 = False
                e1 = False
                a1 = False
                s1 = False
                d1 = False
                q2 = False
                w2 = False
                e2 = False
                a2 = False
                s2 = False
                d2 = False
                o = True
                x = True
                color = False
                center = [0, 0, 0]
                all_sprites.empty()
                nshape = cubePoints(dist, center=Point(center[0], center[1], center[2]))
                shapes = [Shape(nshape.lines, nshape.center)]
                shapes[0].colorize((255, 255, 255))
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()

            if event.key == K_1: # make cube
                all_sprites.empty()
                nshape = cubePoints(dist, Point(center[0], center[1], center[2]))
                shapes = [Shape(nshape.lines, nshape.center)]
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()
            if event.key == K_2: # make tetrahedron
                all_sprites.empty()
                nshape = tetraPoints(dist, Point(center[0], center[1], center[2]))
                shapes = [Shape(nshape.lines, nshape.center)]
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()
            if event.key == K_3: # make octahedron
                all_sprites.empty()
                nshape = octagPoints(dist, Point(center[0], center[1], center[2]))
                shapes = [Shape(nshape.lines, nshape.center)]
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()
            if event.key == K_4: # make cube grid
                all_sprites.empty()
                shapes = cubix(dist, Point(center[0], center[1], center[2]))
                for shape in shapes:
                    if p:
                        all_sprites.add(shape, shape.points)
                    else:
                        all_sprites.add(shape)
            if event.key == K_5: # make sphere based on tta and phi
                all_sprites.empty()
                nshape = spherePoints(dist, center=Point(center[0], center[1], center[2]), tta=tta, phi=phi)
                shapes = [Shape(nshape.lines, nshape.center)]
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()
            if event.key == K_6: # make random shape by moving points randomly, keeping line relations
                for shape in shapes:
                    for point in shape.points:
                        point.move(Point(randInt(2 * dist), randInt(2 * dist), randInt(2 * dist)))
                shapes[0].redraw()

            if event.key == K_x: # input mode change, True is axis rotation, False is in place rotation
                x = not x
            # see variables before loop
            if x:
                if event.key == K_d:
                    d1 = not d1
                    a1 = False
                if event.key == K_a:
                    a1 = not a1
                    d1 = False
                if event.key == K_s:
                    s1 = not s1
                    w1 = False
                if event.key == K_w:
                    w1 = not w1
                    s1 = False
                if event.key == K_q:
                    q1 = not q1
                    e1 = False
                if event.key == K_e:
                    e1 = not e1
                    q1 = False
                if event.key == K_f:
                    speed += .5
                    theta = PI / 1000 * speed
                if event.key == K_g:
                    speed -= .5
                    theta = PI / 1000 * speed
            else:
                if event.key == K_d:
                    d2 = not d2
                    a2 = False
                if event.key == K_a:
                    a2 = not a2
                    d2 = False
                if event.key == K_s:
                    s2 = not s2
                    w2 = False
                if event.key == K_w:
                    w2 = not w2
                    s2 = False
                if event.key == K_q:
                    q2 = not q2
                    e2 = False
                if event.key == K_e:
                    e2 = not e2
                    q2 = False
                if event.key == K_f:
                    speed2 += .5
                    theta2 = PI / 1000 * speed2
                if event.key == K_g:
                    speed2 -= .5
                    theta2 = PI / 1000 * speed2

            # start/stop color cycling
            if event.key == K_c:
                color = not color

            # alter shape size
            if event.key == K_EQUALS: # increase
                odist = dist
                dist += 50
                scale = dist / odist
                for shape in shapes:
                    shape.scale(scale)
            if event.key == K_MINUS and dist > 50: # decrease ( > 50 to avoid div by 0)
                odist = dist
                dist -= 50
                scale = dist / odist
                for shape in shapes:
                    shape.scale(scale)

            # shift shape, by respective arrow direction, pageup is further away (increase z), pagedown is closer (decrease z)
            if event.key == K_UP:
                center[1] += 50
                for shape in shapes:
                    shape.shift([0, 50, 0])
            if event.key == K_DOWN:
                center[1] -= 50
                for shape in shapes:
                    shape.shift([0, -50, 0])
            if event.key == K_RIGHT:
                center[0] += 50
                for shape in shapes:
                    shape.shift([50, 0, 0])
            if event.key == K_LEFT:
                center[0] -= 50
                for shape in shapes:
                    shape.shift([-50, 0, 0])
            if event.key == K_PAGEUP:
                center[2] += 50
                for shape in shapes:
                    shape.shift([0, 0, 50])
            if event.key == K_PAGEDOWN:
                center[2] -= 50
                for shape in shapes:
                    shape.shift([0, 0, -50])

            # change values for sphere generation
            if event.key == K_COMMA: # increase tta
                tta += 1
                all_sprites.empty()
                nshape = spherePoints(dist, center=Point(center[0], center[1], center[2]), tta=tta, phi=phi)
                shapes = [Shape(nshape.lines, nshape.center)]
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()
            if event.key == K_PERIOD: # decrease tta, no lower than 2
                if tta > 2:
                    tta -= 1
                    all_sprites.empty()
                    nshape = spherePoints(dist, center=Point(center[0], center[1], center[2]), tta=tta, phi=phi)
                    shapes = [Shape(nshape.lines, nshape.center)]
                    if p:
                        all_sprites.add(shapes[0], shapes[0].points)
                    else:
                        all_sprites.add(shapes[0])
                    i = 0
                    for point in shapes[0].points:
                        point.move(nshape.points[i])
                        i += 1
                    shapes[0].redraw()
            if event.key == K_k: # increase phi
                phi += 1
                all_sprites.empty()
                nshape = spherePoints(dist, center=Point(center[0], center[1], center[2]), tta=tta, phi=phi)
                shapes = [Shape(nshape.lines, nshape.center)]
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
                i = 0
                for point in shapes[0].points:
                    point.move(nshape.points[i])
                    i += 1
                shapes[0].redraw()
            if event.key == K_l: # decrease phi, no lower than 1
                if phi > 1:
                    phi -= 1
                    all_sprites.empty()
                    nshape = spherePoints(dist, center=Point(center[0], center[1], center[2]), tta=tta, phi=phi)
                    shapes = [Shape(nshape.lines, nshape.center)]
                    if p:
                        all_sprites.add(shapes[0], shapes[0].points)
                    else:
                        all_sprites.add(shapes[0])
                    i = 0
                    for point in shapes[0].points:
                        point.move(nshape.points[i])
                        i += 1
                    shapes[0].redraw()

            # screen drawing options
            if event.key == K_p: # show / hide points
                p = not p
                all_sprites.empty()
                if p:
                    all_sprites.add(shapes[0], shapes[0].points)
                else:
                    all_sprites.add(shapes[0])
            if event.key == K_o: # determines shape redraw or redraw2
                o = not o

    # update the shapes according to keyboard input variables
    for shape in shapes:

        if color: # color change loop
            shape.colorize((cR, cG, cB))
            if cR < 255 and cG < 255 and cB == 1:
                cR += 1
            elif cR == 255 and cG < 255 and cB == 1:
                cG += 1
            elif cG == 255 and cR > 1 and cB == 1:
                cR -= 1
            elif cR == 1 and cB < 255 and cG == 255:
                cB += 1
            elif cB == 255 and cR == 1 and cG > 1:
                cG -= 1
            elif cG == 1 and cR < 255 and cB == 255:
                cR += 1
            elif cR == 255 and cG == 1 and cB > 1:
                cB -= 1

        # determine axis rotations
        if d1:
            shape.rotate("y", theta)
        if a1:
            shape.rotate("v", theta)
        if s1:
            shape.rotate("x", theta)
        if w1:
            shape.rotate("u", theta)
        if q1:
            shape.rotate("z", theta)
        if e1:
            shape.rotate("w", theta)

        # determine in place rotation
        if d2:
            shape.rotateInPlace("y", theta2)
        if a2:
            shape.rotateInPlace("v", theta2)
        if s2:
            shape.rotateInPlace("x", theta2)
        if w2:
            shape.rotateInPlace("u", theta2)
        if q2:
            shape.rotateInPlace("z", theta2)
        if e2:
            shape.rotateInPlace("w", theta2)

        # redraw shape accordingly
        if o:
            shape.redraw()
        else:
            shape.redraw2()

    # apply screen changes
    pygame.display.flip()

pygame.quit()
