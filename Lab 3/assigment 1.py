import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

Windows_Width, Windows_Height = 500, 800

bubble_bullet = []
score = 0
bullets_missed = 0
game_freeze_falg = False
gameover = 0
boundary_passed=0


class Bubble:
    def __init__(self):
        self.x = random.randint(-220, 220)
        self.y = 330
        self.r = random.randint(10, 20)
        self.color = [random.uniform(0.3, 1.0) for _ in range(3)]


class Catcher:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]


# ---------------------------------------------- Mid-Point Line Drawing Algorithm
def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glFlush()


def zone_converter_to_zero(x, y, pointer_zone):
    if pointer_zone == 0:
        return (x, y)
    elif pointer_zone == 1:
        return (y, x)
    elif pointer_zone == 2:
        return (y, -x)
    elif pointer_zone == 3:
        return (-x, y)
    elif pointer_zone == 4:
        return (-x, -y)
    elif pointer_zone == 5:
        return (-y, -x)
    elif pointer_zone == 6:
        return (-y, x)
    elif pointer_zone == 7:
        return (x, -y)


def zone_converter_from_zero(x, y, pointer_zone):
    if pointer_zone == 0:
        return (x, y)
    elif pointer_zone == 1:
        return (y, x)
    elif pointer_zone == 2:
        return (-y, x)
    elif pointer_zone == 3:
        return (-x, y)
    elif pointer_zone == 4:
        return (-x, -y)
    elif pointer_zone == 5:
        return (-y, -x)
    elif pointer_zone == 6:
        return (y, -x)
    elif pointer_zone == 7:
        return (x, -y)


def midpoint_circle_algo(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    # Determine the pointer_zone
    zone = 0
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

    # Convert to pointer_zone 0
    x1, y1 = zone_converter_to_zero(x1, y1, zone)
    x2, y2 = zone_converter_to_zero(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    # calculate initial decision parameter
    d = 2 * dy - dx
    E_increment = 2 * dy
    NE_increment = 2 * (dy - dx)

    # plot initial point
    x, y = x1, y1
    x0, y0 = zone_converter_from_zero(x, y, zone)
    plot_point(x0, y0)

    # iterate over x coordinates
    while x < x2:
        if d <= 0:
            d += E_increment
            x += 1
        else:
            d += NE_increment
            x += 1
            y += 1
        # Convert back from pointer_zone 0
        x0, y0 = zone_converter_from_zero(x, y, zone)
        plot_point(x0, y0)


# ------------------------------------------------------------------Mid-Point Circle Drawing Algorithm


def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()


# -----------------------------------------------------------------------------------
bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubble.sort(key=lambda b: b.x)
catcher = Catcher()


def draw_bullet():
    global bubble_bullet
    glPointSize(2)
    glColor3f(.8, .4, 0)
    for i in bubble_bullet:
        midpointcircle(5, i[0], i[1])


def bubble_drwaing():
    global bubble
    glPointSize(2)

    for i in range(len(bubble)):
        if i == 0:
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)
        elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)


def draw_ui():
    global catcher

    # catcher
    glPointSize(2)
    glColor3f(catcher.color[0], catcher.color[1], catcher.color[2])
    midpointcircle(15, centerX=catcher.x, centerY=-365)

    # Left button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_circle_algo(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_circle_algo(-210, 350, -190, 370)
    midpoint_circle_algo(-210, 350, -190, 330)

    # Right Cross Button
    glPointSize(3)
    glColor3f(0.9, 0, 0)
    midpoint_circle_algo(210, 365, 180, 335)
    midpoint_circle_algo(210, 335, 180, 365)

    # Middle Pause Button
    glPointSize(4)
    glColor3f(1, .5, 0)
    if game_freeze_falg:
        midpoint_circle_algo(-15, 370, -15, 330)
        midpoint_circle_algo(-15, 370, 15, 350)
        midpoint_circle_algo(-15, 330, 15, 350)
    else:
        midpoint_circle_algo(-10, 370, -10, 330)
        midpoint_circle_algo(10, 370, 10, 330)


def coordite_converter(x, y):
    global Windows_Width, Windows_Height
    a = x - (Windows_Width / 2)
    b = (Windows_Height / 2) - y
    return a, b


def keyboardListener(key, x, y):
    global bubble_bullet, game_freeze_falg, gameover
    if key == b' ':
        if not game_freeze_falg and gameover < 5:
            bubble_bullet.append([catcher.x, -365])
    if key == b'd':
        if catcher.x < 230 and not game_freeze_falg:
            catcher.x += 10
    if key == b'a':
        if catcher.x > -230 and not game_freeze_falg:
            catcher.x -= 10
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global catcher, game_freeze_falg
    if key == GLUT_KEY_RIGHT:
        if catcher.x < 230 and not game_freeze_falg:
            catcher.x += 10
    if key == GLUT_KEY_LEFT:
        if catcher.x > -230 and not game_freeze_falg:
            catcher.x -= 10
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global game_freeze_falg, gameover, catcher, score, bubble, bubble_bullet, bullets_missed
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = coordite_converter(x, y)
        print(c_x, c_y)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = coordite_converter(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            game_freeze_falg = False
            print('Starting Over')
            bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
            bubble.sort(key=lambda b: b.x)
            score = 0
            gameover = 0
            bullets_missed = 0
            bubble_bullet = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', score)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            game_freeze_falg = not game_freeze_falg

    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        pass

    glutPostRedisplay()


def display():
    # //clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0);  # //color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # //load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    # //initialize the matrix
    glLoadIdentity()
    gluLookAt(0, 0, 314, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    draw_ui()
    draw_bullet()
    bubble_drwaing()
    glutSwapBuffers()


def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global game_freeze_falg, bubble, catcher, gameover, score, bubble_bullet, bullets_missed ,boundary_passed
    if not game_freeze_falg and gameover < 3 and bullets_missed < 3:
        delidx = []
        for i in range(len(bubble_bullet)):
            if bubble_bullet[i][1] < 385:
                bubble_bullet[i][1] += 10
            else:
                delidx.append(i)
                bullets_missed += 1
        try:
            for j in delidx:
                del bubble_bullet[j]
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                    #boundary_passed+=1
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble())
                    bubble.sort(key=lambda b: b.y)
        try:
            for i in range(len(bubble)):
                if abs(bubble[i].y - -365) < (bubble[i].r) and abs(bubble[i].x - catcher.x) < (bubble[i].r + 15):
                    gameover += 5
                for j in range(len(bubble_bullet)):
                    if abs(bubble[i].y - bubble_bullet[j][1]) < (bubble[i].r + 5 + 3) and abs(bubble[i].x - bubble_bullet[j][0]) < (
                            bubble[i].r + 5 + 3):
                        score += 1
                        print("Score:", score)
                        del bubble[i]
                        del bubble_bullet[j]
                        bubble.append(Bubble())
        except:
            pass


    elif (gameover >= 5 or bullets_missed >= 3) and not game_freeze_falg:
        print("Game Over! Score:", score)
        game_freeze_falg = True

    time.sleep(1 / 60)
    glutPostRedisplay()


def init():
    # //clear the screen
    glClearColor(0, 0, 0, 0)
    # //load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    # //initialize the matrix
    glLoadIdentity()
    # //give PERSPECTIVE parameters
    gluPerspective(104, (500 / 800), 1, 1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    # //near distance
    # //far distance


glutInit()
glutInitWindowSize(Windows_Width, Windows_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)  # //Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Shoot The Circles!")
init()

glutDisplayFunc(display)  # display callback function
glutIdleFunc(animate)  # what you want to do in the idle time (when no drawing is occuring)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()  # The main loop of OpenGL






