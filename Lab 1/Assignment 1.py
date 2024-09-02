from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
angle=0
W_Width, W_Height = 500,500
bg_color= (1.0, 1.0, 1.0,1.0)

arr=[]
for i in range(100):
    x=random.uniform(1,500)
    y=random.uniform(1,500)
    arr.append((x,y))
def raindrops(x,y):
    glColor3f(0,0,1.0)
    glPointSize(1)
    glBegin(GL_LINES)
    glVertex2f(x,y)
    glVertex2f(x, y +10)
    glEnd()


def mul_raindrops():
    for i in range(len(arr)):
        x,y=arr[i]
        y-=1
        x+=angle
        if y < 0:
            y = W_Height
        elif y<300:
            y=random.uniform(300,500)
            x=random.uniform(1,500)
        # x=x%
        arr[i]=(x,y)

def animation(value) :
    mul_raindrops()
    glutPostRedisplay()
    glutTimerFunc(1, animation,0)
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
def house():
    glColor3f(0.0, 0.0, 1.0)
    glPointSize(5)
    glLineWidth(5)
    glColor3f(0.7, 1.0, 0.0)
    glBegin(GL_LINES)

    # roof
    glVertex2f(450, 300)
    glVertex2f(100, 300)
    glVertex2f(450, 300)
    glVertex2f(400, 350)
    glVertex2f(100, 300)
    glVertex2f(150, 350)
    glVertex2f(150, 350)
    glVertex2f(400, 350)


    # body
    glVertex2f(430, 300)
    glVertex2f(430, 100)
    glVertex2f(120, 300)
    glVertex2f(120, 100)
    glVertex2f(120, 100)
    glVertex2f(430, 100)
    glEnd()

    glPointSize(5)
    glLineWidth(4)
    glColor3f(0.7, 0.7, 0.7)

    glBegin(GL_LINES)

    # door
    glVertex2f(150, 100)
    glVertex2f(150, 200)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(150, 200)
    glVertex2f(200, 200)

    # window
    glVertex2f(350, 200)
    glVertex2f(350, 250)
    glVertex2f(300, 200)
    glVertex2f(300, 250)
    glVertex2f(350, 250)
    glVertex2f(300, 250)
    glVertex2f(350, 200)
    glVertex2f(300, 200)
    glVertex2f(300, 225)
    glVertex2f(350, 225)
    glVertex2f(325, 250)
    glVertex2f(325, 200)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    # door lock
    glVertex2f(190, 120)
    glEnd()


def showScreen():
    # Set the background color
    glClearColor(*bg_color)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    house()

    # call the raindrop function
    for i in arr:
        raindrops(i[0], i[1])
    glutSwapBuffers()
def specialKeyListener(key,x,y):
    global angle
    if key==GLUT_KEY_RIGHT:
        angle+=0.5
    elif key==GLUT_KEY_LEFT:
        angle-=0.5
    glutPostRedisplay()
def mouseListener(button, state, x, y):
    global bg_color
    if button == GLUT_LEFT_BUTTON:
        if (state == GLUT_DOWN):
            bg_color = (0, 0, 0, 0)

    if button == GLUT_RIGHT_BUTTON:
        # if state == GLUT_DOWN:
            bg_color = (1.0, 1.0, 1.0, 1.0)
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Lab 1 task 1")
# init()

glutDisplayFunc(showScreen)	#display callback function
glutIdleFunc(animation(0))	#what you want to do in the idle time (when no drawing is occuring)

# glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL