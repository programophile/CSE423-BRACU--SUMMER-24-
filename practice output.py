from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Window dimensions
W_Width, W_Height = 500, 500
bg_color = (1.0, 1.0, 1.0, 1.0)

# House boundaries
house_x_min = 100
house_x_max = 400
house_y_min = 100
house_y_max = 300

# Raindrop initialization
arr = []
for i in range(100):
    while True:
        x = random.uniform(0, 500)
        y = random.uniform(0, 500)
        if not (house_x_min <= x <= house_x_max and house_y_min <= y <= house_y_max):
            break
    arr.append((x, y))


# Draw a raindrop
def raindrops(x, y):
    glColor3f(0, 0, 1.0)
    glPointSize(5)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y - 10)
    glEnd()


# Update raindrops position
def mul_raindrops():
    for i in range(len(arr)):
        x, y = arr[i]
        y -= 1
        if y < 0:
            y = W_Height
            while True:
                x = random.uniform(0, 500)
                if not (house_x_min <= x <= house_x_max):
                    break
        arr[i] = (x, y)


# Animation function
def animation(value):
    mul_raindrops()
    glutPostRedisplay()
    glutTimerFunc(30, animation, 0)


# Function to set up viewport and projection
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 500, 0.0, 500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Draw house
def house():
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    # Roof
    glVertex2f(400, 300)
    glVertex2f(100, 300)
    glVertex2f(400, 300)
    glVertex2f(250, 400)
    glVertex2f(100, 300)
    glVertex2f(250, 400)
    # Body
    glVertex2f(380, 300)
    glVertex2f(380, 100)
    glVertex2f(120, 300)
    glVertex2f(120, 100)
    glVertex2f(120, 100)
    glVertex2f(380, 100)
    glEnd()

    glBegin(GL_LINES)
    # Door
    glVertex2f(140, 100)
    glVertex2f(140, 200)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(140, 200)
    glVertex2f(200, 200)
    # Window
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

    glBegin(GL_POINTS)
    # Door lock
    glVertex2f(190, 120)
    glEnd()


# Display function
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    house()

    for i in arr:
        raindrops(i[0], i[1])

    glutSwapBuffers()


# Main function
def main():
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutCreateWindow(b"OpenGL Coding Practice")

    # init()
    glutDisplayFunc(showScreen)
    glutTimerFunc(0, animation, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()
