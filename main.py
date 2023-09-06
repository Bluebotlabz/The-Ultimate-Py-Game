import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OBJFileLoader.OBJFileLoader.objloader import OBJ

import random

from teapot import Teapot
import math

# Initialise window
pygame.init()
windowSize = (1080, 720)
pygame.display.set_mode(windowSize, DOUBLEBUF | OPENGL)
FPS_CLOCK = pygame.time.Clock()

# Globals to store game state
global score
score = 0
global teapots
teapots = []

def RenderGrid(size=70):
	glLineWidth(1)
	glColor(0, 128/255, 0)
	glBegin(GL_LINES)
	xGrid = size
	yGrid = size
	#for xCoord in range(xGrid*2):
	for yCoord in range(yGrid*2):
		glVertex3fv([-xGrid, -2, yCoord - yGrid])
		glVertex3fv([xGrid, -2, yCoord - yGrid])

	for xCoord in range(xGrid*2):
		glVertex3fv([xCoord - xGrid, -2, -yGrid])
		glVertex3fv([xCoord - xGrid, -2, yGrid])
	glEnd()

def RenderMagicTeapot(location, rotation=(0, 0,0,0), scale=(1, 1, 1)):
	glPushMatrix()
	glTranslatef(location[0], location[1], location[0])
	glRotatef(rotation[0], rotation[1], rotation[2], -rotation[3])
	glColor(0, 0, pygame.time.get_ticks())
	glLineWidth(2.5)
	glScale(scale[0], scale[1], scale[2])
	teapot.render()
	glScale(1/scale[0], 1/scale[1], 1/scale[2])
	glRotatef(-rotation[0], -rotation[1], -rotation[2], -rotation[3])
	glTranslatef(-location[0], -location[1], -location[0])
	glPopMatrix()

# Create teapots
teapotOBJ = OBJ('./utah.obj')
teapot = Teapot(teapotOBJ, [0, 0, -50])

cameraPosition = [0.0, 0.0, -5.0]  # x, y, z
playerVelocity = [0.0, 0.0, 0.0, 0.0] # x, y, z, YAW
playerAngle = [0, 270, 0] # Pitch, yaw, roll
playerSpeed = 0.1

def renderScene():
	# Draw a teapot
	RenderGrid()
	teapot.tick(cameraPosition)
	teapot.render()

gluPerspective(45, (windowSize[0]/windowSize[1]), 0.1, 50.0)
#glRotatef(45, 0, 1, 0)
#glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])

pygame.mouse.set_visible(False)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == KEYDOWN:
			if (event.key == pygame.K_w):
				playerVelocity[2] -= playerSpeed
			elif (event.key == pygame.K_a):
				playerVelocity[0] -= playerSpeed
			elif (event.key == pygame.K_s):
				playerVelocity[2] += playerSpeed
			elif (event.key == pygame.K_d):
				playerVelocity[0] += playerSpeed
			elif (event.key == pygame.K_LEFT):
				playerVelocity[3] -= 10
			elif (event.key == pygame.K_RIGHT):
				playerVelocity[3] += 10
			elif (event.key == pygame.K_q): # Quits game
				pygame.quit()
				quit()
		elif event.type == KEYUP:
			if (event.key == pygame.K_w):
				playerVelocity[2] += playerSpeed
			elif (event.key == pygame.K_a):
				playerVelocity[0] += playerSpeed
			elif (event.key == pygame.K_s):
				playerVelocity[2] -= playerSpeed
			elif (event.key == pygame.K_d):
				playerVelocity[0] -= playerSpeed
			elif (event.key == pygame.K_LEFT):
				playerVelocity[3] += 10
			elif (event.key == pygame.K_RIGHT):
				playerVelocity[3] -= 10
		elif event.type == MOUSEMOTION:
			pass
			#print(event.pos)
			#pygame.mouse.set_pos((0, 0))

	#glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])
	#glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])
	
	playerAngle[1] += playerVelocity[3]
	cameraPosition[0] -= math.sin(math.radians(playerAngle[1])) * playerVelocity[0]   +   math.cos(math.radians(playerAngle[1])) * playerVelocity[2]
	cameraPosition[1] += playerVelocity[1]
	cameraPosition[2] -= math.cos(math.radians(playerAngle[1]+180)) * playerVelocity[0]   +   math.sin(math.radians(playerAngle[1])) * playerVelocity[2]
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glTranslatef(-cameraPosition[0], -cameraPosition[1], -cameraPosition[2])
	renderScene()
	glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])
	glRotatef(playerVelocity[3], 0, 1, 0)
	pygame.display.flip()
	FPS_CLOCK.tick(30)
