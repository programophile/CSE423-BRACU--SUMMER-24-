from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
Windows_Width, Windows_Height= 500, 500
point_arr=[]
game_freeze_falg=False
speed=0.005
size=4

def convert_coordinate(x,y):
    global Windows_Width, Windows_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a,b
class point:
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.direc=[random.choice([-1,1]),random.choice([-1,1])]
        self.dark_color=[0,0,0]
def points_draw(x,y,color,s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(x, y)
    glEnd()
def point_move(x,y):
    global point_arr
    color=[random.random(),random.random(),random.random()]
    # point_arr.append([random.choice([-1,1]),random.choice([-1,1]),color])
    # for i in point_arr:
    #     points_draw(i[0],i[1],i[2])
    point_arr.append(point(x,y,color))
def draw_mul_point():
    global point_arr,size
    for i in point_arr:
        points_draw(i.x,i.y,i.color,size)

def animate():
    global point_arr
    if game_freeze_falg==False:
        for i in point_arr:
            # print(i[0],i[1])
            i.x+=i.direc[0]*speed
            i.y+=i.direc[1]*speed
            if abs(i.x) > Windows_Width / 2:
                i.direc[0] *= -1
            if abs(i.y) > Windows_Height / 2:
                i.direc[1] *= -1
    glutPostRedisplay()

def mouseListener(button,state,x,y):
    global dark_color
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        x, y = convert_coordinate(x, y)
        for i in range(-100, 100, 20):
            # point_move(random.random()+random.choice([40,38,-229292]),random.random()+random.choice([40,38,-229292]))
            if random.random() > 0.75:
                point_move(x + i, y+i)
            elif random.random() > 0.55:
                point_move(x + i, y)
            elif random.random() > 0.25:
                point_move(x, y - i)
            # # elif random.random()>0.85:
            #
            else:
            #     point_move(x * random.uniform(1, 10), y * random.uniform(5, 16))
                point_move(x + i, y - i)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in point_arr:
            point.color, point.dark_color = point.dark_color, point.color

    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        time.sleep(1)
        for point in point_arr:
            point.color, point.dark_color = point.dark_color, point.color

    glutPostRedisplay()
def keyboardListener(key,x,y):
    global speed,game_freeze_falg,size
    if key==b'w':
        size+=1
    elif key==b's':
        size-=1
    elif key==b" ":
        freeze= not freeze
    if size>80:
        size=2
    elif size<3:
        size=80
def specialKeyListener(key,x,y):
    global speed
    if key== GLUT_KEY_UP:
        speed*=1.5
    elif key==GLUT_KEY_DOWN:
        speed/=2
def display():
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0) # //color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # //load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # //initialize the matrix
    glLoadIdentity()
    # //now give three info
    # //1. where is the camera (viewer)?
    # //2. where is the camera looking?
    # //3. Which direction is the camera's UP direction?
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    draw_mul_point()
    glutSwapBuffers()

glutInit()
glutInitWindowSize(Windows_Width, Windows_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"OpenGL Coding Practice")
# init()
# //clear the screen
glClearColor(0, 0, 0, 0)
# //load the PROJECTION matrix
glMatrixMode(GL_PROJECTION)
# //initialize the matrix
glLoadIdentity()
# //give PERSPECTIVE parameters
gluPerspective(104, 1, 1, 1000.0)
# **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
# //near distance
# //far distance

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL