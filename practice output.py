import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500

points = []  
speed = 0.001
ball_size = 4
freeze = False

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dark = [0,0,0]
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw_points(x, y, s, color):
    glColor3f(color[0], color[1], color[2])
    glPointSize(s) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
    
def generate_movable_point(x, y):
    global points
    color = [random.random(), random.random(), random.random()]
    points.append(Point(x, y, color))


def draw_list_points():
    global points
    for point in points:
        draw_points(point.x, point.y, ball_size, point.color)

def keyboardListener(key, x, y):
    global ball_size, speed, freeze
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    elif key == b's':
        ball_size -= 1
        print("Size Decreased")
    elif key == b' ':
        freeze = not freeze
        if freeze:
            print("Freeze")
        else:
            print("Unfreeze")

    glutPostRedisplay()

# def specialKeyListener(key, x, y):
#     global speed
#     if key == GLUT_KEY_UP:
#         if speed<0.25:
#             speed *= 2
#             print("Speed Increased")
#     elif key == GLUT_KEY_DOWN:
#         speed /= 2
#         print("Speed Decreased")
#     glutPostRedisplay()

def mouseListener(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        for i in range(-50,50,10):
            if random.random()>0.75:
                generate_movable_point(c_x+i, c_y+i)
            elif random.random()>0.55:
                generate_movable_point(c_x+i, c_y)
            elif random.random()>0.25:
                generate_movable_point(c_x, c_y-i)
            else:
                generate_movable_point(c_x+i, c_y-i)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in points:
            point.color, point.dark =  point.dark, point.color
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        time.sleep(1)
        for point in points:
            point.color, point.dark =  point.dark, point.color

    glutPostRedisplay()

def display():
     #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    draw_list_points()
    glutSwapBuffers()

def animate():
    global points, freeze
    if not freeze:
        for point in points:
            point.x += speed * point.direction[0]
            point.y += speed * point.direction[1]

            if abs(point.x) > W_Width/2:
                point.direction[0] *= -1
            if abs(point.y) > W_Height/2:
                point.direction[1] *= -1
    glutPostRedisplay()

def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color


# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"CSE423 Assignment 1 Task 2")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL
