import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
width,height=500,800
#button_controls
stop=False
gameover=False
class Diamond:
    def __init__(self):
        self.x=random.randint(-220,220)
        self.y=340
        #cng
        self.color = [random.uniform(0.5, 1.0),random.uniform(0.5, 1.0),random.uniform(0.5, 1.0)]
        self.iterate=0
    def restart(self):
        self.x = random.randint(-180, 180)
        self.y = 340
        # cng
        self.color = [random.uniform(0.5, 1.0) for _ in range(3)]
class Diamond_catcher:
    def __init__(self):
        self.x=0
        self.color=[1,1,1]

#mid_point

#zone_convertion
def point(x,y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glFlush()
def zone_converter_to_zero(x,y,z):
    if z == 0:
        return (x, y)
    elif z == 1:
        return (y, x)
    elif z == 2:
        return (y, -x)
    elif z == 3:
        return (-x, y)
    elif z == 4:
        return (-x, -y)
    elif z == 5:
        return (-y, -x)
    elif z == 6:
        return (-y, x)
    elif z == 7:
        return (x, -y)
def zone_converter_from_zero(x,y,z):
    if z == 0:
        return (x, y)
    elif z == 1:
        return (y, x)
    elif z == 2:
        return (-y, x)
    elif z == 3:
        return (-x, y)
    elif z == 4:
        return (-x, -y)
    elif z == 5:
        return (-y, -x)
    elif z == 6:
        return (y, -x)
    elif z == 7:
        return (x, -y)
    
#main_algo
def midpoint_line_algo(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    zone=0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6
    if zone!=0:
        x1,y1=zone_converter_to_zero(x1,y1,zone)
        x2,y2=zone_converter_to_zero(x2,y2,zone)
    dx = x2 - x1
    dy = y2 - y1
    #decesion_perameter
    d = 2 * dy - dx
    Eincrease=2*dy
    NEincrease=2*(dy-dx)
    x,y=x1,y1
    x0,y0=zone_converter_from_zero(x,y,zone)
    point(x0,y0)
    #iterate through the whole points
    while x < x2:
        if d <= 0:
            d += Eincrease
            x += 1
        else:
            d += NEincrease
            x += 1
            y += 1
        # Convert back from zone 0
        x0, y0 = zone_converter_from_zero(x,y,zone)
        point(x0, y0)
diamond=Diamond()
diamond_catcher=Diamond_catcher()

def diamond_drawing():
    global diamond
    glPointSize(2)

    glColor3f(diamond.color[0], diamond.color[1], diamond.color[2])
    midpoint_line_algo(diamond.x + 10, diamond.y, diamond.x, diamond.y + 18)
    midpoint_line_algo(diamond.x + 10, diamond.y, diamond.x, diamond.y - 18)
    midpoint_line_algo(diamond.x - 10, diamond.y, diamond.x, diamond.y + 18)
    midpoint_line_algo(diamond.x - 10, diamond.y, diamond.x, diamond.y - 18)
def draw_left_button():
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line_algo(-210, 350, -160, 350)
    glPointSize(3)
    midpoint_line_algo(-212, 350, -190, 370)
    midpoint_line_algo(-212, 350, -190, 330)
def draw_cross_button():
    glPointSize(3)
    glColor3f(0.9, 0, 0)
    midpoint_line_algo(200, 365, 170, 335)
    midpoint_line_algo(200, 335, 170, 365)
def draw_pause_button():
    glPointSize(4)
    glColor3f(1, .5, 0)
    if stop:
        midpoint_line_algo(-15, 370, -15, 330)
        midpoint_line_algo(-15, 370, 15, 350)
        midpoint_line_algo(-15, 330, 15, 350)
    else:
        midpoint_line_algo(-10, 370, -10, 330)
        midpoint_line_algo(10, 370, 10, 330)
def ui_drawing():
    global diamond_catcher
    glPointSize(2)
    glColor3f(diamond_catcher.color[0], diamond_catcher.color[1], diamond_catcher.color[2])
    midpoint_line_algo(diamond_catcher.x + 70, -365, diamond_catcher.x - 70, -365)
    midpoint_line_algo(diamond_catcher.x + 60, -385, diamond_catcher.x + 70, -365)
    midpoint_line_algo(diamond_catcher.x + 60, -385, diamond_catcher.x - 60, -385)
    midpoint_line_algo(diamond_catcher.x - 60, -385, diamond_catcher.x - 70, -365)
    draw_left_button()
    draw_cross_button()
    draw_pause_button()
def coordinate_converter(x,y):
    global width, height
    x1 = x - (width / 2)
    y1 = (height / 2) - y
    return x1, y1
def keyboardListener(key, x, y):
    global  stop
    if key == b' ':
        stop = not stop
    glutPostRedisplay()
def specialKeyListener(key, x, y):
    global diamond_catcher, stop
    if key== GLUT_KEY_RIGHT:
        if diamond_catcher.x<180 and not stop:
            diamond_catcher.x += 10
    if key== GLUT_KEY_LEFT:
        if diamond_catcher.x>-180 and not stop:
            diamond_catcher.x -= 10
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global stop, diamond, gameover, diamond_catcher
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = coordinate_converter(x, y)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = coordinate_converter(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            print('Starting Over')
            diamond_catcher.color = (1, 1, 1)
            diamond.restart()
            gameover = False
            stop = False
            diamond.iteration = 0

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', diamond.iterate)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            stop = not stop

    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        pass

    glutPostRedisplay()


def display():
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 314, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    ui_drawing()
    diamond_drawing()
    glutSwapBuffers()

def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global stop, diamond, diamond_catcher, gameover
    if not stop and not gameover:
        diamond.y-= (100 + diamond.iterate*20)* delta_time
        if diamond.y<=-365 and  diamond_catcher.x-75 <= diamond.x <= diamond_catcher.x+75:
            diamond.restart()
            diamond.iterate+=1
            print("Score:", diamond.iterate)
        if diamond.y<-400:
            diamond.restart()
            diamond_catcher.color=(1,0,0)
            print("Game Over! Your Final Score is :", diamond.iterate)
            diamond.iterate=0
            stop=not stop
            gameover = True
    time.sleep(1/60)
    glutPostRedisplay()

def init():

    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(104, (500/800), 1, 1000.0)


glutInit()
glutInitWindowSize(width,height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)



wind = glutCreateWindow(b"Diamonds Game!")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()