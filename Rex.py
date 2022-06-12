from cmath import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import glm
import pygame

# tamanho da tela
WINDOW_WIDHT = 1000
WINDOW_HEIGHT = 1000

# camera
cameraPos = glm.vec3(0, 3.5, 30)
cameraFront = glm.vec3(0, 0, -1)
cameraUp = glm.vec3(0, 1, 0)
angle = 0

# mouse
old_mouse_x = 0
old_mouse_y = 0
angle_x = -1.57
angle_y = 1.57
mouse_speed = 0.1
mouse_sensitivity = 0.001

door_angle = 0
window_angle = 0

half_width = WINDOW_WIDHT / 2
half_height = WINDOW_HEIGHT / 2


def draw_wall(x0, y0, z0, x1, y1, z1): # sem profundidade
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

def draw_floor(x, y, z, width, length): # sem profundidade
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + length)
    glVertex3f(x + width, y, z + length)
    glVertex3f(x + width, y, z)
    glEnd()

def draw_block(x, y, z, width, length, height): # largura, comprimento, altura
    draw_wall(x, y, z, x, y + height, z+length)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    draw_floor(x, y+height, z, width, length)

def draw_colored_block(x, y, z, width, length, height, front_color, back_color, left_color, right_color, up_color, down_color):
    #left side
    glColor3f(left_color.x, left_color.y, left_color.z)
    draw_wall(x, y, z, x, y + height, z+length)
    #back side
    glColor3f(back_color.x, back_color.y, back_color.z)
    draw_wall(x, y, z, x+width, y + height, z)
    #right side
    glColor3f(right_color.x, right_color.y, right_color.z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    #front side
    glColor3f(front_color.x, front_color.y, front_color.z)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    #down side
    glColor3f(down_color.x, down_color.y, down_color.z)
    draw_floor(x, y, z, width, length)
    #up side
    glColor3f(up_color.x, up_color.y, up_color.z)
    draw_floor(x, y+height, z, width, length)

def draw_colored_block_fixed(x, y, z, width, length, height):
    glColor3f(0.293, 0.211, 0.13)
    draw_wall(x, y, z, x, y + height, z+length)
    glColor3f(0.486, 0.293, 0)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    glColor3f(0.36, 0.2, 0.09)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    glColor3f(0.37, 0.15, 0.07)
    draw_floor(x, y+height, z, width, length)

def draw_cylinder(x, y, z, radius, height):
    px = 0
    pz = 0
    c_angle = 0
    angle_stepsize = 0.1

    #desenha cilindro
    glBegin(GL_QUAD_STRIP)
    c_angle = 0
    while c_angle < 2*glm.pi() + 1:
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

    #desenha tampa do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0
    while c_angle < 2 * glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        c_angle += angle_stepsize
    glEnd()

    #desenha fundo do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0
    while c_angle < 2 * glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

def draw_hcylinder(x, y, z, radius, height): # half cylinder
    px = 0.0
    pz = 0.0
    c_angle = 0.0
    angle_stepsize = 0.01

    #desenha cilindro
    glBegin(GL_QUAD_STRIP)
    c_angle = 0.0
    while c_angle < glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

    #desenha tampa do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0.0
    while c_angle < glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y + height, z + pz)
        c_angle += angle_stepsize
    glEnd()

    #desenha fundo do cilindro
    glBegin(GL_POLYGON)
    c_angle = 0.0
    while c_angle < glm.pi():
        px = radius * glm.cos(c_angle)
        pz = radius * glm.sin(c_angle)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()

def draw_table(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # tampo
    draw_colored_block(0, 2, 0, 4, 2, 0.1, # width lenght height
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(0.92, 0.92, 0.92), glm.vec3(1, 1, 1))

    draw_cylinder(2, 0, 1, 0.5, 2)

    glPopMatrix()

def draw_chair(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    # assento
    draw_colored_block_fixed(0, 1, 0, 1.2, 1, 0.1)
    # pés
    draw_colored_block_fixed(0, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(0, 0, 0.8, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0.8, 0.2, 0.2, 1)
    # encosto
    draw_colored_block_fixed(0, 1.1, 0.9, 1.2, 0.1, 1.5)
    glPopMatrix()


def draw_keyboard(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # teclado
    glColor3ub(39, 39, 39)
    draw_block(0, 1.4, 0, 4, 0.9, 0.1)
    
    # pés
    glColor3ub(30, 30, 30)

    glPushMatrix()
    glTranslatef(1.5, 0.07, 0)
    glRotatef(-45, 0, 0, 1)
    draw_block(0, 0, 0, 0.1, 0.2, 2)
    draw_block(0, 0, 0.7, 0.1, 0.2, 2)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.5, 0.0, 0)
    glRotatef(45, 0, 0, 1)
    draw_block(0, 0, 0, 0.1, 0.2, 2)
    draw_block(0, 0, 0.7, 0.1, 0.2, 2)
    glPopMatrix()

    glPopMatrix()

def draw_triangle(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # lados
    glPushMatrix()
    glTranslatef(0, 0.3, 0)
    glRotatef(-60, 0, 0, 1)
    draw_block(0, 0, 0, 0.3, 0.2, 9.825)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(16.9, 0.0, 0)
    glRotatef(60, 0, 0, 1)
    draw_block(0, 0, 0, 0.3, 0.2, 9.85)
    glPopMatrix()
    
    # base
    draw_block(0, 0, 0, 17, 0.2, 0.3)

    glPopMatrix()

def draw_notebook(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    # base
    glColor3ub(157, 150, 142)
    draw_block(0, 2, 0, 1, 0.7, 0.05)
    # tela
    glTranslatef(0, 0.35, 1.15)
    glRotatef(-35, 1, 0, 0)
    glColor3ub(10, 10, 10)

    draw_block(0, 2.05, -0.0, 1, 0.03, 0.7)
    glPopMatrix()

def draw_sc(x, y, z): # semi circle
    glPushMatrix()
    glTranslatef(x, y, z)
    #glColor3ub(80, 80, 80)
    #glTranslatef(0, 0, 0)
    glRotatef(-90, 1, 0, 0)
    draw_hcylinder(0, 0, 0, 1.5, 0.1) # half cylinder
    glPopMatrix() #
    
def draw_ihcylinder(x, y, z, radius, height): # inverced half cylinder - arco
    px = 0.0
    pz = 0.0
    c_angle = 0.0
    angle_stepsize = 0.01

    glPushMatrix()
    #glColor3f(0.0, 0.0, 1.0) # azul
    #desenha a casca interna do cilindro 1
    glTranslatef(x+radius+0.22, y, z+radius) # x+radius+0.1
    glRotatef(180, 0, 1, 0)
    glBegin(GL_QUAD_STRIP)
    c_angle = 0.0
    while c_angle < glm.half_pi():
        px = radius * glm.cos(c_angle)**3
        pz = radius * glm.sin(c_angle)**3
        glVertex3f(x + px, y + height, z + pz)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()
    glPopMatrix()

    glPushMatrix()
    #glColor3f(1.0, 0.0, 0.0) # vermelho
    #desenha a casca interna do cilindro 2
    glTranslatef(x-radius-0.22, y, z+radius) # x-radius-0.1
    glRotatef(90, 0, 1, 0)
    glBegin(GL_QUAD_STRIP)
    c_angle = 0.0
    while c_angle < glm.half_pi():
        px = radius * glm.cos(c_angle)**3
        pz = radius * glm.sin(c_angle)**3
        glVertex3f(x + px, y + height, z + pz)
        glVertex3f(x + px, y, z + pz)
        c_angle += angle_stepsize
    glEnd()
    glPopMatrix()

    #glColor3f(1.0, 1.0, 0.0) # amarelo
    #desenha o tampo de cima - retangulo
    x0 = x - radius - 0.22
    y0 = y 
    z0 = z + radius
    x1 = x + radius + 0.22
    y1 = y + height
    z1 = z + radius
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

    #glColor3f(0.0, 1.0, 0.0) # verde
    # desenha a lateral a - retangulo
    x0 = x - radius - 0.22
    y0 = y 
    z0 = z + radius
    x1 = x - radius - 0.22
    y1 = y + height
    z1 = z
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

    #glColor3f(1.0, 0.0, 1.0) # cyan
    # desenha a lateral b - retangulo
    x0 = x + radius + 0.22
    y0 = y + height 
    z0 = z + radius
    x1 = x + radius + 0.22
    y1 = y
    z1 = z
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

    #glColor3f(0.8, 0.6, 0.1) # laranja
    # desenha tampa do cilindro 1
    px = 0.0
    pz = 0.0
    x0 = x - radius - 0.22 # x - radius - 0.1
    y0 = y
    z0 = z - radius
    glRotatef(180, 0, 1, 0)
    glBegin(GL_POLYGON)
    glVertex3f(x0, y0 + height, z0)
    c_angle = 0.0
    while c_angle < glm.half_pi():
        pz = radius * glm.sin(c_angle)**3
        px = radius * glm.cos(c_angle)**3
        glVertex3f(x0 + px, y0 + height, z0 + pz)
        c_angle += angle_stepsize
    glEnd()

    #glColor3f(0.6, 0.6, 0.6) # cinza
    # desenha tampa do cilindro 2
    px = 0.0
    pz = 0.0
    x0 = x - radius - 0.22 # x - radius - 0.1
    y0 = y - height
    z0 = z - radius

    glBegin(GL_POLYGON)
    glVertex3f(x0, y0 + height, z0)
    c_angle = 0.0
    while c_angle < glm.half_pi():
        pz = radius * glm.sin(c_angle)**3
        px = radius * glm.cos(c_angle)**3
        glVertex3f(x0 + px, y0 + height, z0 + pz)
        c_angle += angle_stepsize
    glEnd()

    #glColor3f(0.7, 0.1, 0.6) # roseo
    #desenha tampa do cilindro 3
    px = 0.0
    pz = 0.0
    x0 = x - radius - 0.22 #  x - radius - 0.1
    y0 = y - 1
    z0 = z - radius
    glRotatef(180, 0, 1, 0)
    glRotatef(180, 1, 0, 0)
    glBegin(GL_POLYGON)
    glVertex3f(x0, y0 + height, z0)
    c_angle = 0.0
    while c_angle < glm.half_pi():
        pz = radius * glm.sin(c_angle)**3
        px = radius * glm.cos(c_angle)**3
        glVertex3f(x0 + px, y0 + height, z0 + pz)
        c_angle += angle_stepsize
    glEnd()

    #glColor3f(0.6, 0.6, 0.6) # cinza
    #desenha tampa do cilindro 4
    px = 0.0
    pz = 0.0
    x0 = x - radius - 0.22 #  x - radius - 0.1
    y0 = y -1 + height
    z0 = z - radius

    glBegin(GL_POLYGON)
    glVertex3f(x0, y0 + height, z0)
    c_angle = 0.0
    while c_angle < glm.half_pi():
        pz = radius * glm.sin(c_angle)**3
        px = radius * glm.cos(c_angle)**3
        glVertex3f(x0 + px, y0 + height, z0 + pz)
        c_angle += angle_stepsize
    glEnd()


def draw_isc(x, y, z): # inverted semi circle
    glPushMatrix() #begin fan
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    draw_ihcylinder(0, 0, 0, 1.281, 0.5) # arco 1.5 -> 1.281

    glPopMatrix() #end fan

def display():
    global angle, door_angle, window_angle
    # limpa cor e buffers de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # reseta transformações
    glLoadIdentity()

    # define camera
    # camx camy camz centerx centery centerz upx upy upz
    gluLookAt(cameraPos.x, cameraPos.y, cameraPos.z,
              cameraPos.x + cameraFront.x, cameraPos.y + cameraFront.y, cameraPos.z + cameraFront.z,
              cameraUp.x, cameraUp.y, cameraUp.z)


    glPushMatrix() # push bar

    # Arco com astroide
    glColor3f(0.78, 0.77, 0.74)
    #draw_isc(0,0,0)
    draw_isc(3.5,4,30.5)
    draw_isc(8.5,4,30.5)
    draw_isc(13.5,4,30.5)


    # parede do fundo
    #glColor3f(0.992, 0.768, 0.529)
    #draw_block(0, 0, 0, 17, 0.5, 8) # largura, comprimento, altura
    
    # parede esquerda
    #glColor3f(0.964, 0.78, 0.474)
    #draw_block(0, 0, 0.5, 0.5, 29.5, 8) # largura, comprimento, altura
    
    # parede direita
    glColor3f(0.964, 0.78, 0.474)
    #draw_block(16.5, 0, 0.5, 0.5, 29.5, 8) # largura, comprimento, altura
    draw_block(16.5, 0, 0.5,  0.5,   10, 8) # largura, comprimento, altura
    draw_block(16.5, 0, 10.5, 0.5,    3, 3) # largura, comprimento, altura
    draw_block(16.5, 0, 13.5, 0.5, 16.5, 8) # largura, comprimento, altura
    draw_block(16.5, 5, 10.5, 0.5,   10, 3) # largura, comprimento, altura
    #janela
    glPushMatrix()
    glTranslatef(16.5, 3, 10.5)
    glRotatef(window_angle, 0, 1, 0)
    glColor3f(0.725, 0.870, 0.952)
    draw_block(0, 0, 0, 0.15, 3, 2)
    glPopMatrix()
    
    # piso
    glColor3f(0.921, 0.858,  0.717)
    draw_block(0.5, 0, 0.5, 16, 29.5, 0) # largura, comprimento, altura

    # Teto
    glColor3f(0.905, 0.937, 0.901)
    draw_block(0.5, 8, 0.5, 16, 29.5, 0) # largura, comprimento, altura

    # Triangulo da frente com os detalhes nas arestas
    glColor3f(0.905, 0.937, 0.901)
    draw_triangle(0, 9, 30.5)

    glColor3f(0.78, 0.77, 0.74)
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3f(0, 9, 30.51)
    glVertex3f(8.5, 14, 30.51)
    glVertex3f(17, 9, 30.51)
    glEnd()
    glPopMatrix()

    # Base horizontal - Detalhe branco
    glColor3f(0.905, 0.937, 0.901)
    draw_block(0, 8, 30.5, 17, 0.2, 0.1)
    glColor3f(1, 1, 1)
    draw_wall(0, 7.7, 30.53, 17, 8, 30.53)
    glColor3f(0.905, 0.937, 0.901)
    draw_block(0, 7.7, 30.5, 17, 0.2, 0.1)

    # parede da frente
    # bloco 1
    glColor3f(0.78, 0.77, 0.74)
    draw_block(0, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # bloco 2
    glColor3f(0.78, 0.77, 0.74)
    draw_block(5, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # bloco 3
    glColor3f(0.78, 0.77, 0.74)
    draw_block(10, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # bloco 4
    glColor3f(0.78, 0.77, 0.74)
    draw_block(15, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # bloco 5 (cima - horizontal)
    glColor3f(0.78, 0.77, 0.74)
    draw_block(0, 5.28, 30, 17, 0.5, 7) # largura, comprimento, altura


    # palco
    glColor3f(0.6, 0.6, 0.6)
    draw_block(1, 0, 2, 10, 6, 1) # largura, comprimento, altura

    # teclado
    draw_keyboard(5, 1, 5)

    # lounge bar
    glColor3f(1.0, 1.0, 1.0)
    draw_block(13.5, 0, 12, 2, 6, 3) # largura, comprimento, altura

    # notebook
    draw_notebook(14, 1, 15)

    glPushMatrix()
    #mesa
    draw_table(6, 0, 12)
    #cadeira
    draw_chair(7.5, 0, 14)
    glRotatef(180, 0, 1, 0)
    draw_chair(-8.5, 0, -12)
    glPopMatrix()

    glPushMatrix()
    #mesa
    draw_table(1, 0, 12)
    #cadeira
    draw_chair(2.5, 0, 14)
    glRotatef(180, 0, 1, 0)
    draw_chair(-3.5, 0, -12)
    glPopMatrix()

    glPushMatrix()
    #mesa
    draw_table(6, 0, 18)
    #cadeira
    draw_chair(7.5, 0, 20)
    glRotatef(180, 0, 1, 0)
    draw_chair(-8.5, 0, -18)
    glPopMatrix()

    glPushMatrix()
    #mesa
    draw_table(1, 0, 18)
    #cadeira
    draw_chair(2.5, 0, 20)
    glRotatef(180, 0, 1, 0)
    draw_chair(-3.5, 0, -18)
    glPopMatrix()

    # portas
    glPushMatrix()
    glTranslatef(2, 0, 30)
    glRotatef(door_angle, 0, 1, 0)
    glColor3f(0.921, 0.6, 0.615)
    draw_block(0,0,0, 3, 0.3, 4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(7, 0, 30)
    glRotatef(door_angle, 0, 1, 0)
    glColor3f(0.921, 0.6, 0.615)
    draw_block(0,0,0, 3, 0.3, 4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(12, 0, 30)
    glRotatef(door_angle, 0, 1, 0)
    glColor3f(0.921, 0.6, 0.615)
    draw_block(0,0,0, 3, 0.3, 4)
    glPopMatrix()

    glPopMatrix()  # pop bar

    glutSwapBuffers()


def keyboard(key, x, y):
    global angle, cameraFront, cameraUp, cameraPos, door_angle, window_angle

    cameraSpeed = 0.5

    if not isinstance(key, int):
        key = key.decode("utf-8")
    #controles da camera
    if key == 'w' or key == 'W':
        cameraPos += cameraSpeed * cameraFront
    elif key == 'a' or key == 'A':
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    elif key == 's' or key == 'S':
        cameraPos -= cameraSpeed * cameraFront
    elif key == 'd' or key == 'D':
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
    elif key == 'q' or key == 'Q':
        cameraPos.y += cameraSpeed/2
    elif key == 'e' or key == 'E':
        cameraPos.y -= cameraSpeed/2

    #abertura da porta
    if key == 'o':
        door_angle += 5
    if key == 'O':
        door_angle -= 5
    #abertura das janelas
    if key == 'j':
        window_angle += 5
    if key == 'J':
        window_angle -= 5

    glutPostRedisplay()


def change_side(w, h):
    global half_width, half_height
    if h == 0:
        h = 1
    ratio = w * 1/h

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    glViewport(0, 0, w, h)

    half_width = w / 2
    half_height = h / 2

    gluPerspective(45, ratio, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)


def mouse_click(button, state, x, y):
    global old_mouse_x, old_mouse_y
    old_mouse_x = x
    old_mouse_y = y


def mouse_camera(mouse_x, mouse_y):
    global mouse_sensitivity, mouse_speed, angle_x, angle_y, cameraFront, old_mouse_x, old_mouse_y

    angle_x -= (mouse_x - old_mouse_x) * mouse_sensitivity
    angle_y -= (mouse_y - old_mouse_y) * mouse_sensitivity

    front = glm.vec3()
    front.x = glm.cos(angle_x) * glm.sin(angle_y)
    front.z = glm.sin(angle_x) * glm.sin(angle_y)
    front.y = glm.cos(angle_y)
    cameraFront = front

    old_mouse_x = mouse_x
    old_mouse_y = mouse_y
    glutPostRedisplay()

def setup_lighting():
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1])

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.8, 0.8, 0.8, 1])
    # glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1])

    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.3, 0.3, 0.3, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 7, 0, 1])


def main():
    global textures

    # inicialização
    glutInit()  # inicia glut
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(WINDOW_WIDHT, WINDOW_HEIGHT)
    window = glutCreateWindow("Rex Jazz Bar")

    #iluminação
    setup_lighting()

    #callbacks
    glutDisplayFunc(display)
    glutReshapeFunc(change_side)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_camera)

    glutMainLoop()


main()
