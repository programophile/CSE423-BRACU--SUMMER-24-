from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

window_w, window_h = 500, 500
points = []
speed_of_points = 0.05
blinking = False
freeze = False
blink_timer = 0  # Timer to control blinking

def drawBox():
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2d(-200, -150)
    glVertex2d(-200, 150)
    glVertex2d(200, -150)
    glVertex2d(200, 150)
    glVertex2d(-200, -150)
    glVertex2d(200, -150)
    glVertex2d(-200, 150)
    glVertex2d(200, 150)
    glEnd()


def draw_point():
    global points, color, blinking
    glPointSize(5)

    glBegin(GL_POINTS)  # Begin drawing points
    for i in points:
        x, y, dx, dy, color, visibility = i #UNPACK
        if visibility or not blinking:
            glColor3f(*color)  # Set the color of the point
            glVertex2f(x, y)  # Draw a point at (x, y)
    glEnd()


def converting_coordinates(x, y): #ball box
    global window_w, window_h
    x = x - (window_w / 2)
    y = (window_h / 2) - y
    return x, y


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    drawBox()
    draw_point()
    glutSwapBuffers()

def animate():
    global points, speed_of_points, blinking, freeze, blink_timer

    if freeze:
        return

    # Update positions of points
    for i in range(len(points)):
        points[i][0] += points[i][2] * speed_of_points  # Update x-coordinate
        points[i][1] += points[i][3] * speed_of_points  # Update y-coordinate

        # Bounce back if hitting boundaries
        if points[i][0] >= 200 or points[i][0] <= -200:
            points[i][2] *= -1
        if points[i][1] >= 150 or points[i][1] <= -150:
            points[i][3] *= -1

    # Control blinking
    if blinking:
        blink_timer += 1
        if blink_timer >= 60:  # Toggle visibility approximately every 0.5 seconds (30 frames)
            for i in range(len(points)):
                points[i][5] = not points[i][5]  # Toggle visibility
            blink_timer = 0

    glutPostRedisplay()  # Request redraw

def mouseListener(button, state, x, y):
    global points, blinking, freeze

    if freeze:
        return

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            point_x, point_y = converting_coordinates(x, y)

            if -200 < point_x < 200 and -150 < point_y < 150:
                color = [random.random(), random.random(), random.random()]
                direction_x, direction_y = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
                points.append([point_x, point_y, direction_x, direction_y, color, True])

    elif button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            blinking = not blinking


def keyboardListener(key, x, y):
    global freeze
    if key == b" ":
        freeze = not freeze

def specialKeyListener(key, x, y):
    global speed_of_points, freeze

    if freeze:
        return

    if key == GLUT_KEY_UP:
        speed_of_points += 0.05  # Increase speed
    elif key == GLUT_KEY_DOWN:
        if speed_of_points > 0.05:  # Ensure speed doesn't go below a certain limit
            speed_of_points -= 0.05  # Decrease speed


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(window_w, window_h)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Magic Box_T2")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()
