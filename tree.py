from turtle import *
from random import *
from math import sin, cos, tan, pi, radians, sqrt

ANG_SPREAD = 30
ANG_OFFSET = 10
LENGTH_SPREAD = 0.6
LENGTH_MIN = 0.5
RED_LEAF_RANGE = 0.4
GREEN_LEAF_RANGE = 0.4
BLUE_LEAF_RANGE = 0.4
RED_LEAF_RGB = 0.4
GREEN_LEAF_RGB = 0.4
BLUE_LEAF_RGB = 0.0
LEAF_ANGLE_RANGE = 90
MAX_BRANCH_NUM = 3
FAST_FORWARD_BRANCH_END_NUM = 1
LEAF_SIZE_MIN = 20
LEAF_SIZE_SPREAD = 20
PEN_THICKNESS_RESOLUTION_NUM = 10

LEFT_TO_RIGHT_LIGHT_DIFF = 0.5
WIDTH, HEIGHT = 1080, 1080

GRASS_HEIGHT_MIN = 10
GRASS_HEIGHT_SPREAD = 40
GRASS_THICK_MIN = 1
GRASS_THICK_SPREAD = 5
RED_GRASS_RANGE = 0.4
GREEN_GRASS_RANGE = 0.4
BLUE_GRASS_RANGE = 0.1
RED_GRASS_RGB = 0.4
GREEN_GRASS_RGB = 0.6
BLUE_GRASS_RGB = 0.05
GRASS_NUM = 10000

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
            pensize = GRASS_THICK_MIN + random() * GRASS_THICK_SPREAD
            fd(GRASS_HEIGHT_MIN + random() * GRASS_HEIGHT_SPREAD)
            drawed = drawed + 1
    pu()

def tree(n, l):
    pd()
    t = cos(radians(heading() + 45)) / 8 + 0.25
    pencolor(t, t, t)

    #pensize(n**3 / 50)
    #forward(l)

    for i in range(PEN_THICKNESS_RESOLUTION_NUM):
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

            tree(branch_remaining, d)
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




if __name__ == '__main__':
    #Screen size
    screen = Screen()
    screen.setup(WIDTH + 4, HEIGHT + 8)  # fudge factors due to window borders & title bar
    #screen.setworldcoordinates(WIDTH/2, HEIGHT/2, WIDTH*2, HEIGHT*2)
    speed(0)
    pu()
    ht()
    setpos((0,-100))    
    pd()

    #Hill drawing
    pu()
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
    bgcolor(0.8, 0.8, 1)
    ht()
    speed(0)
    tracer(0, 0)
    left(90)
    pu()
    backward(300)
    tree(10, 100)

    #Grass
    grass()

    # Save vector image
    getcanvas().postscript(file="test.ps")
    exitonclick()
    done()