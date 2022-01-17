from PIL import Image
from PIL import EpsImagePlugin
import cv2 as cv
from turtle import *
from random import *
from math import sin, cos, tan, pi, radians, sqrt, ceil
from random import randint, uniform
from time import time

BRANCH_NUM_SETTING = 11
LENGTH_SETTING = 110
ANG_SPREAD = 30
ANG_OFFSET = 10
LENGTH_SPREAD = 0.6
LENGTH_MIN = 0.5
RED_LEAF_RANGE = 0.9
GREEN_LEAF_RANGE = 0.9
BLUE_LEAF_RANGE = 0.9
RED_LEAF_RGB = 0.1
GREEN_LEAF_RGB = 0.1
BLUE_LEAF_RGB = 0.1
LEAF_ANGLE_RANGE = 90
MAX_BRANCH_NUM = 3
FAST_FORWARD_BRANCH_END_NUM = 1
LEAF_SIZE_MIN = 20
LEAF_SIZE_SPREAD = 20
PEN_THICKNESS_RESOLUTION_NUM = 10

LEFT_TO_RIGHT_LIGHT_DIFF = 0.5
WIDTH, HEIGHT = 1080, 1080

GRASS_HEIGHT_MIN = 10
GRASS_HEIGHT_SPREAD = 50
GRASS_THICK_MIN = 1
GRASS_THICK_SPREAD = 3
RED_GRASS_RANGE = 0.3
GREEN_GRASS_RANGE = 0.3
BLUE_GRASS_RANGE = 0.1
RED_GRASS_RGB = 0.5
GREEN_GRASS_RGB = 0.6
BLUE_GRASS_RGB = 0.1
GRASS_NUM = 4000
GRASS_ANG_SPREAD = 40
GRASS_ANG_OFFSET = 0

SAVEDIR = "Images/"
NUM_IMG = 1000
SAVENAME = ""

n = 500 # number of points on each ellipse
# X,Y is the center of ellipse, a is radius on x-axis, b is radius on y-axis
# ts is the starting angle of the ellipse, te is the ending angle of the ellipse
# P is the list of coordinates of the points on the ellipse

def grass():
    drawed = 0;
    while(drawed < GRASS_NUM):
        posx = random() * WIDTH - WIDTH / 2
        posy = random() * HEIGHT - HEIGHT / 2
        if(posy < -470  + 100 * sin((posx + WIDTH/2)/(WIDTH*4)*2*pi+pi/4)):
            pencolor(RED_GRASS_RGB + random() * RED_GRASS_RANGE, \
            GREEN_GRASS_RGB + random() * GREEN_GRASS_RANGE, \
            BLUE_GRASS_RGB + random() * BLUE_GRASS_RANGE)
            pu()
            setpos((posx, posy))
            pd()
            pensize(GRASS_THICK_MIN + random() * GRASS_THICK_SPREAD)
            ang = GRASS_ANG_SPREAD * random() - GRASS_ANG_SPREAD/2
            right(ang)
            fd(GRASS_HEIGHT_MIN + random() * GRASS_HEIGHT_SPREAD)
            left(ang)
            drawed = drawed + 1
    pu()

def tree(n, l, last_color):
    pd()
    t = cos(radians(heading() + 45)) / 8 + 0.25
    pencolor(t, t, t)

    #pensize(n**3 / 50)
    #forward(l)

    t_diff = (t - last_color) / PEN_THICKNESS_RESOLUTION_NUM
    for i in range(PEN_THICKNESS_RESOLUTION_NUM):
        pencolor(last_color + t_diff * i, last_color + t_diff * i, last_color + t_diff * i)
        pensize(int((n - (i/(PEN_THICKNESS_RESOLUTION_NUM)))**2 / 3))
        forward(int(l / PEN_THICKNESS_RESOLUTION_NUM))

    if n > 0:
        branch_num = int(random() * MAX_BRANCH_NUM) + 1
        for i in range(branch_num):
            spread_ang = (0.5 - random()) * ANG_SPREAD
            b = spread_ang + spread_ang/abs(spread_ang) * ANG_OFFSET
            d = l * (random() * LENGTH_SPREAD + LENGTH_MIN)
            right(b)

            branch_remaining = n - 1 - int(FAST_FORWARD_BRANCH_END_NUM * random())
            if(branch_remaining < 1):
                branch_remaining = 0
            
            posx, posy = pos()
            if posx  > WIDTH/2 - (LENGTH_MIN + LENGTH_SPREAD)*l*2 or \
               posx  < -WIDTH/2 + (LENGTH_MIN + LENGTH_SPREAD)*l*2 or \
               posy  > HEIGHT/2 - (LENGTH_MIN + LENGTH_SPREAD)*l*2 or \
               posy  < -HEIGHT/2 + (LENGTH_MIN + LENGTH_SPREAD)*l*2:
               branch_remaining = 0

            tree(branch_remaining, d, t)
            left(b)
    else:
        position = pos()
        angle = heading()
        pu()
        right(random() * LEAF_ANGLE_RANGE - LEAF_ANGLE_RANGE/2)
        fillcolor(RED_LEAF_RGB + random() * RED_LEAF_RANGE, \
            GREEN_LEAF_RGB + random() * GREEN_LEAF_RANGE, \
            BLUE_LEAF_RGB + random() * BLUE_LEAF_RANGE)
        begin_fill()

        spread_leaf = int(random() * LEAF_SIZE_SPREAD)
        circle(LEAF_SIZE_MIN + spread_leaf,70)
        left(110)
        circle(LEAF_SIZE_MIN + spread_leaf,70)
        end_fill()
        setpos(position)
        setheading(angle)
    pu()

    for i in range(PEN_THICKNESS_RESOLUTION_NUM):
        backward(int(l / PEN_THICKNESS_RESOLUTION_NUM))

def ellipse(X,Y,a,b,ts,te,P):
    t = ts
    for i in range(n):
        x = a*cos(t)
        y = b*sin(t)
        P.append((x+X,y+Y))
        t += (te-ts)/(n-1)

# computes Euclidean distance between p1 and p2
def dist(p1,p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

# draws an arc from p1 to p2 with extent value ext
def draw_arc(p1,p2,ext):
    up()
    goto(p1)
    seth(towards(p2))
    a = heading() 
    b = 360-ext 
    c = (180-b)/2
    d = a-c
    e = d-90
    r = dist(p1,p2)/2/sin(radians(b/2)) # r is the radius of the arc
    seth(e) # e is initial heading of the circle
    down()
    circle(r,ext,100)
    return (xcor(),ycor()) # returns the landing position of the circle
                                         # this position should be extremely close to p2 but may not be exactly the same
                                         # return this for continuous drawing to the next point


def cloud(P):
    step = n//10 # draw about 10 arcs on top and bottom part of cloud
    a = 0 # a is index of first point
    b = a + randint(step//2,step*2) # b is index of second point
    p1 = P[a] # p1 is the position of the first point
    p2 = P[b] # p2 is the position of the second point
    fillcolor('white')
    begin_fill()
    p3 = draw_arc(p1,p2,uniform(70,180)) # draws the arc with random extention
    while b < len(P)-1:
        p1 = p3 # start from the end of the last arc 
        if b < len(P)/2: # first half is top, more ragged
            ext = uniform(70,180)
            b += randint(step//2,step*2)
        else: # second half is bottom, more smooth
            ext = uniform(30,70)
            b += randint(step,step*2)
        b = min(b,len(P)-1) # make sure to not skip past the last point
        p2 = P[b] # second point
        p3 = draw_arc(p1,p2,ext) # draws an arc and return the end position
    end_fill()
    pu()
    

def draw_save_process(iter):
    n = 500
    #Screen size
    screen = Screen()
    screen.setup(WIDTH + 4, HEIGHT + 8)  # fudge factors due to window borders & title bar
    #screen.setworldcoordinates(WIDTH/2, HEIGHT/2, WIDTH*2, HEIGHT*2)
    speed(0)
    pu()
    ht()
    setpos((0,-100))    

    # Drawing Clouds
    speed(0)
    hideturtle()
    fillcolor(0.8, 0.8, 1.0)
    pu()
    setpos(-WIDTH/2, -HEIGHT/2)
    begin_fill()
    setpos(-WIDTH/2, HEIGHT/2)
    setpos(WIDTH/2, HEIGHT/2)
    setpos(WIDTH/2, -HEIGHT/2)
    end_fill()
    setpos(0,0)
    pu()
    pencolor('white')
    pensize(2)

    P = [] # starting from empty list
    ellipse(0,0,300,200,0,pi,P) # taller top half
    ellipse(0,0,300,50,pi,pi*2,P) # shorter bottom half
    cloud(P)

    #Hill drawing
    pu()
    setheading(0)
    setpos((0,-470))  
    pensize(1)
    fillcolor(0.1, 0.7, 0.1)
    pu()
    setpos((-WIDTH/2,-470  + 100 * sin(0/(WIDTH*4)*2*pi+pi/4)))
    begin_fill()
    for i in range(0, WIDTH + 30, 20):
        setpos((i-WIDTH/2,-470  + 100 * sin(i/(WIDTH*4)*2*pi+pi/4)))
    
    setpos(WIDTH/2, -HEIGHT/2)
    setpos(-WIDTH/2, -HEIGHT/2)
    end_fill()
    pu()

	# Starting of tree drawing
    setpos((0,-100))  
    ht()
    pu()
    speed(0)
    tracer(0, 0)
    left(90)
    backward(300)
    t = cos(radians(heading() + 45)) / 8 + 0.25
    tree(BRANCH_NUM_SETTING, LENGTH_SETTING, t)

    #Grass
    grass()

    # Save vector image
    getcanvas().postscript(file="test.eps")
    getcanvas().postscript(file=(SAVEDIR + "eps/" +  SAVENAME + str(iter) + ".eps"))

    dpi = 600.
    img = Image.open("test.eps")
    original = [float(d) for d in img.size]
    # scale = width / original[0] # calculated wrong height
    scale = dpi/72.0            # this fixed it
    if dpi is not 0:
        img.load(scale = ceil(scale))
    if scale != 1:
        img.thumbnail([round(scale * d) for d in original], Image.ANTIALIAS)

    #psimage=Image.open('test.eps')
    img.save('test.png', dpi=(600, 600))
    img.save((SAVEDIR + "png/" +  SAVENAME + str(iter) + ".png"), dpi=(600, 600))
    # Blurring
    img = cv.imread('test.png')
    blur = cv.bilateralFilter(img,9,75,75)
    cv.imwrite("blur.png", blur)
    cv.imwrite((SAVEDIR + "blur/" +  SAVENAME + str(iter) + ".png"), blur)
    clear()
    clearscreen()

if __name__ == '__main__':
    draw_save_process(0)
    draw_save_process(1)
    for i in range(NUM_IMG):
        draw_save_process(i)