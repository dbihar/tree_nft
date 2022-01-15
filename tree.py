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
RED_LEAF_RGB = 0.6
GREEN_LEAF_RGB = 0.6
BLUE_LEAF_RGB = 0.05
LEAF_ANGLE_RANGE = 90
MAX_BRANCH_NUM = 3
FAST_FORWARD_BRANCH_END_NUM = 1

def tree(n, l):
    pd()
    t = cos(radians(heading() + 45)) / 8 + 0.25
    pencolor(t, t, t)
    pensize(n**3 / 50)
    forward(l)
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
        circle(30,70)
        left(110)
        circle(30,70)
        end_fill()
        setpos(position)
        setheading(angle)
    pu()
    backward(l)




if __name__ == '__main__':
	# Starting of tree drawing
	bgcolor(1, 1, 1)
	ht()
	speed(0)
	tracer(0, 0)
	left(90)
	pu()
	backward(300)
	tree(10, 100)
	done()