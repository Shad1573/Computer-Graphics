#TASK 1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width, height = 800, 600

raindrops = []
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(height // 2, height)
    raindrops.append((x, y))
rain_direction = 0

brightness = 0.1  
target_brightness = 0.1

def draw_ground_and_sky():
    
    glColor3f(brightness, brightness, brightness)
    glBegin(GL_TRIANGLES)
    glVertex2f(0, height)
    glVertex2f(width, height)
    glVertex2f(0, height * 0.6)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(width, height)
    glVertex2f(width, height * 0.6)
    glVertex2f(0, height * 0.6)
    glEnd()

    
    glColor3f(0.5, 0.25, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(0, height * 0.6)
    glVertex2f(width, height * 0.6)
    glVertex2f(0, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(width, height * 0.6)
    glVertex2f(width, 0)
    glVertex2f(0, 0)
    glEnd()

def draw_house():
    glColor3f(0.2, 0.2, 0.9)  
    glBegin(GL_TRIANGLES)
    glVertex2f(300, 300)
    glVertex2f(500, 300)
    glVertex2f(400, 400)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)  
    glBegin(GL_TRIANGLES)
    glVertex2f(320, 200)
    glVertex2f(480, 200)
    glVertex2f(320, 300)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(480, 200)
    glVertex2f(480, 300)
    glVertex2f(320, 300)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)  
    glBegin(GL_TRIANGLES)
    glVertex2f(380, 200)
    glVertex2f(420, 200)
    glVertex2f(380, 250)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(420, 200)
    glVertex2f(420, 250)
    glVertex2f(380, 250)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)  
    glBegin(GL_LINES)
    glVertex2f(340, 260)
    glVertex2f(360, 260)
    glVertex2f(360, 260)
    glVertex2f(360, 280)
    glVertex2f(360, 280)
    glVertex2f(340, 280)
    glVertex2f(340, 280)
    glVertex2f(340, 260)
    glEnd()


def draw_trees():
    glColor3f(0.2, 0.8, 0.2)
    tree_positions = [-150, 450]
    for x_offset in tree_positions:
        glBegin(GL_TRIANGLES)
        glVertex2f(200 + x_offset, 300)
        glVertex2f(250 + x_offset, 400)
        glVertex2f(300 + x_offset, 300)
        glEnd()

    glColor3f(0.4, 0.2, 0.0)
    for x_offset in tree_positions:
        glBegin(GL_TRIANGLES)
        glVertex2f(230 + x_offset, 250)
        glVertex2f(270 + x_offset, 250)
        glVertex2f(230 + x_offset, 300)
        glEnd()
        
        glBegin(GL_TRIANGLES)
        glVertex2f(270 + x_offset, 250)
        glVertex2f(270 + x_offset, 300)
        glVertex2f(230 + x_offset, 300)
        glEnd()

def draw_rain():
    glColor3f(0.0, 0.0, 0.8)
    glLineWidth(2)
    glBegin(GL_LINES)
    for x, y in raindrops:
        glVertex2f(x, y)
        glVertex2f(x + rain_direction, y - 20)
    glEnd()
    glLineWidth(1)

def update_rain():
    global raindrops
    new_raindrops = []
    for x, y in raindrops:
        y -= 5
        x += rain_direction * 0.2
        if y < 0 or x < 0 or x > width:
            y = height
            x = random.randint(0, width)
        new_raindrops.append((x, y))
    raindrops = new_raindrops
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(brightness, brightness, brightness, 1.0)
    draw_ground_and_sky()
    draw_trees()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def animate():
    update_rain()
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global brightness
    if key == b'd':
        brightness = min(1.0, brightness + 0.05)
    elif key == b'n':
        brightness = max(0.0, brightness - 0.05)

def specialKeyListener(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction = max(-10, rain_direction - 1)
    elif key == GLUT_KEY_RIGHT:
        rain_direction = min(10, rain_direction + 1)

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

glutInit()
glutInitWindowSize(width, height)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"House in Rain")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()




#TASK 2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width, height = 800, 600
points = []
speed = 1
blink = False
frozen = False

def draw_box():
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(50, 50)
    glVertex2f(width - 50, 50)
    glVertex2f(width - 50, height - 50)
    glVertex2f(50, height - 50)
    glEnd()

def draw_points():
    if blink:
        if (glutGet(GLUT_ELAPSED_TIME) // 500) % 2 == 0:
            return
    
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(p['color'][0], p['color'][1], p['color'][2])
        glVertex2f(p['x'], p['y'])
    glEnd()

def update_points():
    if frozen:
        return
    for p in points:
        p['x'] += p['dx'] * speed
        p['y'] += p['dy'] * speed
        
        if p['x'] <= 50 or p['x'] >= width - 50:
            p['dx'] *= -1
        if p['y'] <= 50 or p['y'] >= height - 50:
            p['dy'] *= -1
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_box()
    draw_points()
    glutSwapBuffers()

def mouse_listener(button, state, x, y):
    global blink
    y = height - y
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        points.append({
            'x': x, 'y': y,
            'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]),
            'color': (random.random(), random.random(), random.random())
        })
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen

def special_key_listener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed += 1
    elif key == GLUT_KEY_DOWN:
        speed = max(1, speed - 1)

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

glutInit()
glutInitWindowSize(width, height)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(update_points)
glutMouseFunc(mouse_listener)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(special_key_listener)
glutMainLoop()