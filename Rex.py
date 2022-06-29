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


fan_rotation = 0
door_angle = 0
window_angle = 0

half_width = WINDOW_WIDHT / 2
half_height = WINDOW_HEIGHT / 2

#textures
textures = {
    'brick': None,
    'floor': None,
    'roof': None,
    'door1': None,
    'door2': None,
    'bar': None,
    'stage': None,
    'computer': None,
    'keyboard': None,
    'chair': None
}


def draw_wall(x0, y0, z0, x1, y1, z1): # sem profundidade
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y0, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x0, y1, z0)
    glEnd()

def draw_textured_wall(x0, y0, z0, x1, y1, z1, texture, power_tile):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x0, y0, z0)
    glTexCoord2f(power_tile, 0.0)
    glVertex3f(x1, y0, z1)
    glTexCoord2f(power_tile, power_tile)
    glVertex3f(x1, y1, z1)
    glTexCoord2f(0.0, power_tile)
    glVertex3f(x0, y1, z0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_floor(x, y, z, width, length): # sem profundidade
    glBegin(GL_QUADS)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + length)
    glVertex3f(x + width, y, z + length)
    glVertex3f(x + width, y, z)
    glEnd()

def draw_textured_floor(x, y, z, width, length, texture, power_tile): # sem profundidade

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(x, y, z)
    glTexCoord2f(power_tile, 0.0)
    glVertex3f(x, y, z + length)
    glTexCoord2f(power_tile, power_tile)
    glVertex3f(x + width, y, z + length)
    glTexCoord2f(0.0, power_tile)
    glVertex3f(x + width, y, z)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def draw_block(x, y, z, width, length, height): # largura, comprimento, altura
    draw_wall(x, y, z, x, y + height, z+length)
    draw_wall(x, y, z, x+width, y + height, z)
    draw_wall(x+width, y, z, x + width, y + height, z + length)
    draw_wall(x, y, z+length, x + width, y + height, z + length)
    draw_floor(x, y, z, width, length)
    draw_floor(x, y+height, z, width, length)

def draw_texturized_block(x, y, z, width, length, height, texture, left, right, front, back, top, bottom, filler, repeat_tile_left, repeat_tile_right, repeat_tile_front, repeat_tile_back, repeat_tile_top, repeat_tile_bottom):
    
    if left == 1:
        #left side
        #draw_wall(x, y, z, x, y + height, z+length)
        #glColor3f(1, 1, 1)
        draw_textured_wall(x, y, z, x, y + height, z+length, texture, repeat_tile_left)
    else:
        draw_wall(x, y, z, x, y + height, z+length)

    if right == 1:
        #right side
        #draw_wall(x+width, y, z, x + width, y + height, z + length)
        #glColor3f(1, 1, 1)
        draw_textured_wall(x+width, y, z, x + width, y + height, z + length, texture, repeat_tile_right)
    else:
        draw_wall(x+width, y, z, x + width, y + height, z + length)

    if front == 1:
        #front side
        #draw_wall(x, y, z+length, x + width, y + height, z + length)
        #glColor3f(1, 1, 1)
        draw_textured_wall(x, y, z+length, x + width, y + height, z + length, texture, repeat_tile_front)
    else:
        draw_wall(x, y, z+length, x + width, y + height, z + length)
    
    if back == 1:
        #back side
        #draw_wall(x, y, z, x+width, y + height, z)
        #glColor3f(1, 1, 1)
        draw_textured_wall(x, y, z, x+width, y + height, z, texture, repeat_tile_back)
    else:
        draw_wall(x, y, z, x+width, y + height, z)

    if top == 1:
        #top side
        #draw_floor(x, y+height, z, width, length)
        #glColor3f(1, 1, 1)
        draw_textured_floor(x, y+height, z, width, length, texture, repeat_tile_top)
    else:
        draw_floor(x, y+height, z, width, length)

    if bottom == 1:
        #bottom side
        #draw_floor(x, y, z, width, length)
        #glColor3f(1, 1, 1)
        draw_textured_floor(x, y, z, width, length, texture, repeat_tile_bottom)
    else:
        draw_floor(x, y, z, width, length)


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

def draw_cylinder(x, y, z, radius, height): # Usada para desenhar o pé da pesa
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


def draw_table(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    # tampo
    draw_colored_block(0, 2, 0, 4, 2, 0.1, # width lenght height
                       glm.vec3(0.8, 0.8, 0.8), glm.vec3(1, 1, 1),
                       glm.vec3(0.6, 0.6, 0.6), glm.vec3(1, 1, 1),
                       glm.vec3(0.92, 0.92, 0.92), glm.vec3(1, 1, 1))

    # pé 
    draw_cylinder(2, 0, 1, 0.5, 2)

    glPopMatrix()

def draw_chair(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    # assento
    #draw_colored_block_fixed(0, 1, 0, 1.2, 1, 0.1)
    draw_texturized_block(0, 1, 0, 1.2, 1, 0.1, textures['chair'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)
    # pés
    draw_colored_block_fixed(0, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0, 0.2, 0.2, 1)
    draw_colored_block_fixed(0, 0, 0.8, 0.2, 0.2, 1)
    draw_colored_block_fixed(1, 0, 0.8, 0.2, 0.2, 1)
    # encosto
    #draw_colored_block_fixed(0, 1.1, 0.9, 1.2, 0.1, 1.5)
    draw_texturized_block(0, 1.1, 0.9, 1.2, 0.1, 1.5, textures['chair'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)
    glPopMatrix()


def draw_keyboard(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # teclado
    #glColor3ub(39, 39, 39)
    #draw_block(0, 1.4, 0, 4, 0.9, 0.1)
    draw_texturized_block(0, 1.4, 0, 4, 0.9, 0.1, textures['keyboard'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)
    
    # pés
    glColor3f(0.15, 0.15, 0.15)

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

def draw_computer(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # base
    glColor3ub(157, 150, 142)
    draw_block(0, 0, 0, 0.8, 0.8, 0.1)
    
    # tela
    glTranslatef(0.4, 0.1, 1.3)
    glRotatef(90, 0, 1, 0)
   
    #glColor3ub(10, 10, 15)
    #draw_block(0, 0, 0, 2, 0.1, 2)
    draw_texturized_block(0, 0, 0, 2, 0.1, 2, textures['computer'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)

    glPopMatrix()
    
def draw_ihcylinder(x, y, z, radius, height): # inverted half cylinder - arco
    px = 0.0
    pz = 0.0
    c_angle = 0.0
    angle_stepsize = 0.01

    glPushMatrix()
    #glColor3f(0.0, 0.0, 1.0) # azul
    # desenha a casca interna do cilindro 1
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
    # desenha a casca interna do cilindro 2
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
    # desenha o tampo de cima - retangulo
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

    glRotatef(180, 0, 1, 0) # Vale para as tampas 1, 2, 3 e 4
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
    # desenha tampa do cilindro 3
    px = 0.0
    pz = 0.0
    x0 = x - radius - 0.22 #  x - radius - 0.1
    y0 = y - 1
    z0 = z - radius
    glRotatef(180, 0, 1, 0) # Vale para a tampa 3 e 4
    glRotatef(180, 1, 0, 0) # Vale para a tampa 3 e 4
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
    # desenha tampa do cilindro 4
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
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    draw_ihcylinder(0, 0, 0, 1.281, 0.5) # arco 1.5 -> 1.281

    glPopMatrix()

def draw_fan(x, y, z, rotation):
    glPushMatrix() #begin fan
    
    
    glTranslatef(x, y, z) # Origem de tudo
    #glRotatef(90, 1, 0, 0)
    #glutSolidSphere(0.05, 10, 10)
    # push base
    glPushMatrix()

    glTranslatef(0, 0.4, -1)
    glRotatef(90, 1, 0, 0)

    # base
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 0, 0, 0.5, 0.1)

    # pop base
    glPopMatrix()

    # push haste
    glPushMatrix()

    glTranslatef(0, 0.2, -1.06)
    glRotatef(45, 1, 0, 0)

    # haste
    glColor3ub(60, 60, 60)
    draw_cylinder(0, 0.2, 0, 0.1, 1.5)

    # pop haste
    glPopMatrix()

    # motor + helices
    glPushMatrix()
    
    glTranslatef(0, 1.7, -2)
    glRotatef(90, 1, 0, 0)

    # motor
    glColor3ub(80, 80, 80)
    draw_cylinder(0, 1.7, 0, 0.4, 0.8)

    # haste helices
    glColor3ub(10, 10, 10)
    draw_cylinder(0, 2.5, 0, 0.05, 0.1)  

    glRotatef(-rotation, 0, 1, 0) # ISSO AQUI RODA O VENLILADOR
    
    # push helices
    glPushMatrix()
    glColor3ub(100, 100, 100)
    draw_cylinder(0, 2.6, 0, 0.3, 0.2)  # centro helices
    glColor3ub(130, 130, 130)

    glPushMatrix() # pop helices 1 e 2
    glScalef(2.5, 1, 1)
    
    draw_cylinder(-0.45, 2.7, 0, 0.3, 0.03) # helice 1
    draw_cylinder(0.45, 2.7, 0, 0.3, 0.03)  # helice 2
    glPopMatrix() # pop helices 1 e 2

    glScalef(1, 1, 2.5)
    draw_cylinder(0, 2.7, 0.45, 0.3, 0.03)  # helice 3
    draw_cylinder(0, 2.7, -0.45, 0.3, 0.03) # helice 4

    # pop helices
    glPopMatrix()

    glutPostRedisplay()

    # pop motor + helices
    glPopMatrix()

    glPopMatrix() # end fan

####################################################################################################################

def display():
    global angle, door_angle, window_angle, fan_rotation
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

    # parede do fundo
    glColor3f(0.992, 0.768, 0.529)
    draw_texturized_block(0, 0, 0, 17, 0.5, 8, textures['brick'], 1, 1, 1, 1, 1, 1, 42, 2, 2, 2, 2, 2, 2)
    # x, y, z, width, length, height, texture, # largura, comprimento, altura
    # left, right, front, back, top, bottom,
    # filler,
    # repeat_tile_left, repeat_tile_right, repeat_tile_front, repeat_tile_back, repeat_tile_top, repeat_tile_bottom
    
    # parede esquerda
    glColor3f(0.964, 0.78, 0.474)
    draw_texturized_block(0, 0, 0.5, 0.5, 29.5, 8, textures['brick'], 1, 1, 1, 1, 1, 1, 42, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5)
    
    # parede direita (4 partes)
    glColor3f(0.964, 0.78, 0.474)

    # 1) parte fundo
    #draw_block(16.5, 0, 0.5,  0.5,   10, 8) # largura, comprimento, altura
    draw_texturized_block(16.5, 0, 0.5,  0.5,   10, 8, textures['brick'], 1, 1, 1, 1, 1, 1, 42, 2, 2, 2, 2, 2, 2)

    # 2) parte meio em baixo
    #draw_block(16.5, 0, 10.5, 0.5,    3, 3) # largura, comprimento, altura
    draw_texturized_block(16.5, 0, 10.5, 0.5,    3, 3, textures['brick'], 1, 1, 1, 1, 1, 1, 42, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7)

    # 3) parte meio em cima
    #draw_block(16.5, 5, 10.5, 0.5,   10, 3) # largura, comprimento, altura
    draw_texturized_block(16.5, 5, 10.5, 0.5,    3, 3, textures['brick'], 1, 1, 1, 1, 1, 1, 42, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7)

    # 4) parte frente
    #draw_block(16.5, 0, 13.5, 0.5, 16.5, 8) # largura, comprimento, altura
    draw_texturized_block(16.5, 0, 13.5, 0.5, 16.5, 8, textures['brick'], 1, 1, 1, 1, 1, 1, 42, 2, 2, 2, 2, 2, 2)

    # janela
    glPushMatrix()
    glTranslatef(17, 3, 10.5)
    glRotatef(window_angle, 0, 1, 0)
    glColor3f(0.725, 0.870, 0.952)
    draw_block(0, 0, 0, 0.15, 3, 2)
    glPopMatrix()

    # piso
    glColor3f(0.921, 0.858,  0.717)
    #draw_block(0.5, 0, 0.5, 16, 29.5, 0) # largura, comprimento, altura
    draw_texturized_block(0.5, 0, 0.5, 16, 29.5, 0, textures['floor'], 1, 1, 1, 1, 1, 1, 42, 10, 10, 10, 10, 10, 10)

    # teto
    glColor3f(0.905, 0.937, 0.901)
    #draw_block(0.5, 8, 0.5, 16, 29.5, 0) # largura, comprimento, altura
    #draw_texturized_block(0.5, 8, 0.5, 16, 29.5, 0, textures['roof'], 1, 1, 1, 1, 1, 1, 42, 6, 6, 6, 6, 6, 6)
    
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

    # parede da frente (5 partes)
    # 1) bloco 1 - Esquerda em baixo
    glColor3f(0.78, 0.77, 0.74)
    draw_block(0, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # 2) bloco 2 - Entre as portas 1 e 2 em baixo
    glColor3f(0.78, 0.77, 0.74)
    draw_block(5, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # 3) bloco 3 - Entre as portas 2 e 3 em baixo
    glColor3f(0.78, 0.77, 0.74)
    draw_block(10, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # 4) bloco 4 - Direita em baixo
    glColor3f(0.78, 0.77, 0.74)
    draw_block(15, 0, 30, 2, 0.5, 5.28) # largura, comprimento, altura

    # 5) bloco 5 - Cima - horizontal
    glColor3f(0.78, 0.77, 0.74)
    draw_block(0, 5.28, 30, 17, 0.5, 7) # largura, comprimento, altura

    # Arcos com astroide

    # Cor
    glColor3f(0.78, 0.77, 0.74)
    #glColor3f(1, 1, 1)

    # Teste
    #draw_isc(0,0,0) 

    # Arco da porta 1
    draw_isc(3.5,4,30.5)

    # Arco da porta 2
    draw_isc(8.5,4,30.5)

    # Arco da porta 3
    draw_isc(13.5,4,30.5)
    
    # palco
    glColor3f(0.6, 0.6, 0.6)
    #draw_block(1, 0, 2, 10, 6, 1) # largura, comprimento, altura
    draw_texturized_block(1, 0, 2, 10, 6, 1, textures['stage'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)

    # teclado
    draw_keyboard(5, 1, 5)

    # lounge bar
    glColor3f(1.0, 1.0, 1.0)
    #draw_block(13.5, 0, 12, 2, 6, 3) # largura, comprimento, altura
    draw_texturized_block(13.5, 0, 12, 2, 6, 3, textures['bar'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)

    # computer
    draw_computer(14, 3, 16.5)

    # mesas e cadeiras (4 partes)

    # 1)
    glPushMatrix()
    # mesa
    draw_table(6, 0, 12)

    # cadeira
    draw_chair(7.5, 0, 14)
    glRotatef(180, 0, 1, 0)
    draw_chair(-8.5, 0, -12)
    glPopMatrix()

    # 2)
    glPushMatrix()
    # mesa
    draw_table(1, 0, 12)

    # cadeira
    draw_chair(2.5, 0, 14)
    glRotatef(180, 0, 1, 0)
    draw_chair(-3.5, 0, -12)
    glPopMatrix()

    # 3)
    glPushMatrix()
    # mesa
    draw_table(6, 0, 18)

    # cadeira
    draw_chair(7.5, 0, 20)
    glRotatef(180, 0, 1, 0)
    draw_chair(-8.5, 0, -18)
    glPopMatrix()

    # 4)
    glPushMatrix()
    # mesa
    draw_table(1, 0, 18)

    # cadeira
    draw_chair(2.5, 0, 20)
    glRotatef(180, 0, 1, 0)
    draw_chair(-3.5, 0, -18)
    glPopMatrix()
    
    # portas (3 portas)
    # 1)
    glPushMatrix()
    glTranslatef(2, 0, 30)
    glRotatef(door_angle, 0, 1, 0)
    glColor3f(0.921, 0.6, 0.615)
    #draw_block(0,0,0, 3, 0.3, 4)
    draw_texturized_block(0,0,0, 3, 0.3, 4, textures['door2'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)
    glPopMatrix()

    # 2)
    glPushMatrix()
    glTranslatef(7, 0, 30)
    glRotatef(door_angle, 0, 1, 0)
    glColor3f(0.921, 0.6, 0.615)
    #draw_block(0,0,0, 3, 0.3, 4)
    draw_texturized_block(0,0,0, 3, 0.3, 4, textures['door2'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)
    glPopMatrix()
    
    # 3)
    glPushMatrix()
    glTranslatef(12, 0, 30)
    glRotatef(door_angle, 0, 1, 0)
    glColor3f(0.921, 0.6, 0.615)
    #draw_block(0,0,0, 3, 0.3, 4)
    draw_texturized_block(0,0,0, 3, 0.3, 4, textures['door2'], 1, 1, 1, 1, 1, 1, 42, 1, 1, 1, 1, 1, 1)
    glPopMatrix()

    #mesa do ventilador
    glPushMatrix()
    #glTranslatef(-1.3, 0, 9.9)
    #glRotatef(180, 0, 1, 0)

    #glScalef(0.7, 0.7, 0.7)
    draw_fan(4, 4, 1.5, fan_rotation)
    glPopMatrix()

    glPopMatrix()  # pop bar

    glutSwapBuffers()

    # incrementa a rotação do ventilador
    if fan_rotation >= 360:
        fan_rotation = 0.0
    fan_rotation += 3 # velocidade da rotação


def keyboard(key, x, y):
    global angle, cameraFront, cameraUp, cameraPos, door_angle, window_angle

    cameraSpeed = 0.5

    if not isinstance(key, int):
        key = key.decode("utf-8")
    # controles da camera
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

    # abertura da porta
    if key == 'o':
        door_angle += 5
    if key == 'p':
        door_angle -= 5
    # abertura das janelas
    if key == 'j':
        window_angle += 5
    if key == 'k':
        window_angle -= 5
    
    # controle da iluminação
    if key == 'x':
        glEnable(GL_LIGHT0)
    if key == 'z':
        glDisable(GL_LIGHT0)

    # controle spotlight 1
    if key == 'v':
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
    if key == 'c':
        glDisable(GL_LIGHT1)
        glDisable(GL_LIGHT2)
        
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

def load_texture(image):
    textureSurface = pygame.image.load(image)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glGenerateMipmap(GL_TEXTURE_2D)

    return texid

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
    
    glLightfv(GL_LIGHT0, GL_POSITION, [8.5, 7, 15, 1])

    # spot light 1
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1, 1, 1, 1])

    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0, 0, -1])
    glLightfv(GL_LIGHT1, GL_POSITION, [8.5, 7, 15, 1])

    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 20)
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)

    # spot light 2
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [1, 1, 1, 1])

    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, [0, -1, 0])
    glLightfv(GL_LIGHT2, GL_POSITION, [8.5, 6, 30])

    glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 20)
    glLightf(GL_LIGHT2, GL_SPOT_EXPONENT, 2.0)


def main():
    global textures

    # inicialização
    glutInit()  # inicia glut
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(WINDOW_WIDHT, WINDOW_HEIGHT)
    window = glutCreateWindow("Rex Jazz Bar")

    # iluminação
    setup_lighting()

    # callbacks
    glutDisplayFunc(display)
    glutReshapeFunc(change_side)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_camera)

    # textures
    textures['brick'] = load_texture("textures/bricks.png")
    textures['floor'] = load_texture("textures/floor.png")
    textures['roof'] = load_texture("textures/roof.png")
    textures['door1'] = load_texture("textures/door1.png")
    textures['door2'] = load_texture("textures/door2.png")
    textures['bar'] = load_texture("textures/bar.png")
    textures['stage'] = load_texture("textures/stage.png")
    textures['computer'] = load_texture("textures/computer.png")
    textures['keyboard'] = load_texture("textures/keyboard.png")
    textures['chair'] = load_texture("textures/chair.png")
    
    glutMainLoop()


main()
