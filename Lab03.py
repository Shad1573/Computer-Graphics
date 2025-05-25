from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_mode = 0
camera_pos = [0, -500, 300]
camera_look_at = [0, 0, 0]
camera_up = [0, 0, 1]
camera_radius = 500
camera_angle_h = 0
camera_height = 300

# Player gun state
player_pos = [0.0, 0.0]
player_angle = 0.0
bullets = []

tile_size = 80
grid_count = 13
half_size = (tile_size * grid_count) / 2
BOUNDARY_MIN = -half_size
BOUNDARY_MAX = half_size

life = 5
missed_bullets = 0
score = 0
game_over = False
enemy_count = 5
enemies = []

cheat_mode = False
auto_follow = False
cheat_rotation_angle = 0

def random_enemy_position():
    return [random.uniform(BOUNDARY_MIN, BOUNDARY_MAX), random.uniform(BOUNDARY_MIN, BOUNDARY_MAX), 15]

for _ in range(enemy_count):
    enemies.append([*random_enemy_position(), 0.7, 1])

fovY = 120
GRID_LENGTH = 600
rand_var = 423

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 0)

    if game_over:
    
      glRotatef(90, 1, 0, 0)  
    else:
      glRotatef(player_angle, 0, 0, 1)  


    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0, -15, 30)
    glScalef(1, 1, 2.5)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0, 15, 30)
    glScalef(1, 1, 2.5)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.5, 0.7, 0.4)
    glTranslatef(0, 0, 60)
    glScalef(1, 1.5, 2)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 95)
    glutSolidSphere(10, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.96, 0.8, 0.69)
    glTranslatef(0, -20, 65)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 20, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.96, 0.8, 0.69)
    glTranslatef(0, 20, 65)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 20, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(0, 0, 65)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 30, 10, 10)
    glPopMatrix()

    glPopMatrix()

def drawEnemies():
    if game_over:
        return  

    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy[0], enemy[1], enemy[2] + 15)
        current_scale = enemy[3]
        glScalef(current_scale, current_scale, current_scale)

        glColor3f(1, 0, 0)
        glutSolidSphere(15, 20, 20)

        glPushMatrix()
        glTranslatef(0, 0, 20)
        glColor3f(0, 0, 0)
        glutSolidSphere(10, 20, 20)
        glPopMatrix()

        glPopMatrix()


def drawBullets():
    glColor3f(1, 0.5, 0)  
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet["pos"][0], bullet["pos"][1], 65)
        glutSolidSphere(5, 15, 15)  
        glPopMatrix()

def restart_game():
    global player_pos, player_angle, bullets, enemies, life, missed_bullets, game_over, score
    player_pos = [0.0, 0.0]
    player_angle = 0.0
    bullets.clear()
    enemies[:] = [[*random_enemy_position(), 1.0, 1] for _ in range(enemy_count)]
    life = 5
    missed_bullets = 0
    score = 0
    game_over = False

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, auto_follow, cheat_rotation_angle

    move_step = 12 if camera_mode == 1 else 20  
 
    rot_step = 5

    if key == b'w':
        new_x = player_pos[0] + move_step * math.cos(math.radians(player_angle))
        new_y = player_pos[1] + move_step * math.sin(math.radians(player_angle))
        if BOUNDARY_MIN <= new_x <= BOUNDARY_MAX:
            player_pos[0] = new_x
        if BOUNDARY_MIN <= new_y <= BOUNDARY_MAX:
            player_pos[1] = new_y

    elif key == b's':
        new_x = player_pos[0] - move_step * math.cos(math.radians(player_angle))
        new_y = player_pos[1] - move_step * math.sin(math.radians(player_angle))
        if BOUNDARY_MIN <= new_x <= BOUNDARY_MAX:
            player_pos[0] = new_x
        if BOUNDARY_MIN <= new_y <= BOUNDARY_MAX:
            player_pos[1] = new_y

    elif key == b'a':
        player_angle += rot_step

    elif key == b'd':
        player_angle -= rot_step

    elif key == b'r' and game_over:
        restart_game()

    elif key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        if not cheat_mode:
            auto_follow = False
        

    elif key == b'v' or key == b'V':
        if cheat_mode and camera_mode == 1:
            auto_follow = not auto_follow
            

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global camera_angle_h, camera_height

    if camera_mode == 0:
        if key == GLUT_KEY_LEFT:
            camera_angle_h -= 5
        elif key == GLUT_KEY_RIGHT:
            camera_angle_h += 5
        elif key == GLUT_KEY_UP:
            if camera_height < 600:
                camera_height += 10
        elif key == GLUT_KEY_DOWN:
            if camera_height > 100:  
                camera_height -= 10

        

def mouseListener(button, state, x, y):
    global bullets, camera_mode , auto_follow

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        bx = player_pos[0]
        by = player_pos[1]
        angle_rad = math.radians(player_angle)
        
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)

        bullet = {
            "pos": [bx, by],
            "dir": [dx, dy]  
        }
        bullets.append(bullet)
        print("Player Bullet Fired!")


    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        
        camera_mode = 1 - camera_mode
        auto_follow = False


def animate():
    global enemies, bullets, missed_bullets, life, game_over, score , cheat_rotation_angle , player_angle

    if game_over:
        glutPostRedisplay()
        return

    
    for enemy in enemies:
        dx = player_pos[0] - enemy[0]
        dy = player_pos[1] - enemy[1]
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist < 20:  
            life -= 1
            print(f"Remaining Player Life: {life}")

            if life <= 0:
                game_over = True
            enemy[:] = [*random_enemy_position(), 1.0, 1]
        else:
            move_speed = 0.1
            enemy[0] += (dx / dist) * move_speed
            enemy[1] += (dy / dist) * move_speed

        

        scale, direction = enemy[3], enemy[4]
        scale_change = 0.005  
        scale += scale_change * direction

        

        scale, direction = enemy[3], enemy[4]
        scale_change = 0.01  

        if direction == 1:  
            scale += scale_change
            if scale >= 1.5:  
                direction = -1
        else:  
            scale -= scale_change
            if scale <= 0.7:  
                direction = 1

        enemy[3] = scale
        enemy[4] = direction

   
    updated_bullets = []
    for bullet in bullets:
        bullet["pos"][0] += bullet["dir"][0] * 5
        bullet["pos"][1] += bullet["dir"][1] * 5

        bx, by = bullet["pos"]
        if not (BOUNDARY_MIN <= bx <= BOUNDARY_MAX and BOUNDARY_MIN <= by <= BOUNDARY_MAX):
            missed_bullets += 1
            print(f"Bullet Missed: {missed_bullets}")

            if missed_bullets >= 10:
                game_over = True
            continue

        hit = False
        for i, enemy in enumerate(enemies):
            ex, ey = enemy[0], enemy[1]
            if math.dist([bx, by], [ex, ey]) < 20 * enemy[3]:
                enemies[i] = [*random_enemy_position(), 1.0, 1]
                score += 1
                hit = True
                break

        if not hit:
            updated_bullets.append(bullet)

    bullets = updated_bullets

    if cheat_mode and not game_over:
        cheat_rotation_angle += 1.8 if camera_mode == 1 else 2
        cheat_rotation_angle %= 360

        player_angle = cheat_rotation_angle



        
        for enemy in enemies:
            dx = enemy[0] - player_pos[0]
            dy = enemy[1] - player_pos[1]
            angle_to_enemy = math.degrees(math.atan2(dy, dx)) % 360
            angle_diff = abs((angle_to_enemy - cheat_rotation_angle + 180) % 360 - 180)

            
            if angle_diff < 1:
                angle_rad = math.radians(cheat_rotation_angle)
                bullets.append({
                    "pos": [player_pos[0], player_pos[1]],
                    "dir": [math.cos(angle_rad), math.sin(angle_rad)]
                })
                break  

    glutPostRedisplay()



def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)

    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()

    global camera_mode

    if camera_mode == 0:
        
        angle_rad = math.radians(camera_angle_h)
        camera_pos[0] = player_pos[0] + camera_radius * math.cos(angle_rad)
        camera_pos[1] = player_pos[1] + camera_radius * math.sin(angle_rad)
        camera_pos[2] = camera_height
        camera_look_at[0] = player_pos[0]
        camera_look_at[1] = player_pos[1]
        camera_look_at[2] = 60
    else:
        
        if cheat_mode and auto_follow:
            
            angle_rad = math.radians(cheat_rotation_angle)
        else:
            if cheat_mode:
                if auto_follow:
                    angle_rad = math.radians(cheat_rotation_angle)  
                else:
                    angle_rad = math.radians(0)  
            else:
                angle_rad = math.radians(player_angle) 

        camera_pos[0] = player_pos[0] + 10 * math.cos(angle_rad)
        camera_pos[1] = player_pos[1] + 10 * math.sin(angle_rad)
        camera_pos[2] = 95
        camera_look_at[0] = player_pos[0] + 50 * math.cos(angle_rad)
        camera_look_at[1] = player_pos[1] + 50 * math.sin(angle_rad)
        camera_look_at[2] = 95

 

    gluLookAt(*camera_pos, *camera_look_at, *camera_up)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

   
    for x in range(grid_count):
        for y in range(grid_count):
            if (x + y) % 2 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1.0, 1.0, 1.0)

            x_start = -half_size + x * tile_size
            y_start = -half_size + y * tile_size

            glBegin(GL_QUADS)
            glVertex3f(x_start, y_start, 0)
            glVertex3f(x_start + tile_size, y_start, 0)
            glVertex3f(x_start + tile_size, y_start + tile_size, 0)
            glVertex3f(x_start, y_start + tile_size, 0)
            glEnd()

  
    height = 50.0
    base_z = -0.1

    
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MIN, base_z)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MIN, height)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MAX, height)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MAX, base_z)
    glEnd()

    
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MIN, base_z)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MIN, height)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MAX, height)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MAX, base_z)
    glEnd()

   
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MIN, base_z)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MIN, height)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MIN, height)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MIN, base_z)
    glEnd()

   
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MAX, base_z)
    glVertex3f(BOUNDARY_MIN, BOUNDARY_MAX, height)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MAX, height)
    glVertex3f(BOUNDARY_MAX, BOUNDARY_MAX, base_z)
    glEnd()

   
    draw_shapes()
    drawEnemies()
    drawBullets()


    if not game_over:
        draw_text(10, 680, f"Player Life Remaining: {life}")
        draw_text(10, 650, f"Game Score: {score}")
        draw_text(10, 620, f"Player Bullet Missed: {missed_bullets}")
    

    if game_over:
        draw_text(10, 680, f"GAME OVER. Your score is {score}", font=GLUT_BITMAP_HELVETICA_12)
        draw_text(10, 650, "Press 'R' to Restart", font=GLUT_BITMAP_HELVETICA_12)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"3D Shooter Game")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(animate)

    glEnable(GL_DEPTH_TEST)
    glutMainLoop()


if __name__ == "__main__":
    main()