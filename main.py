import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

import meshes
import math

# Initialise window
pygame.init()
windowSize = (1080, 720)
pygame.display.set_mode(windowSize, DOUBLEBUF | OPENGL)


def Cube():
	glBegin(GL_QUADS)
	for vertex in meshes.Cube.rawVertices:
		glVertex3fv(vertex)
	glEnd()

def renderScene():
	Cube()


cameraPosition = [0.0, 0.0, -5.0]  # x, y, z
playerVelocity = [0.0, 0.0, 0.0]
playerAngle = [0, 270, 0] # Pitch, yaw, roll
playerSpeed = 0.1

gluPerspective(45, (windowSize[0]/windowSize[1]), 0.1, 50.0)
#glRotatef(45, 0, 1, 0)
glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == KEYDOWN:
			if (event.key == pygame.K_w):
				playerVelocity[2] += playerSpeed
			elif (event.key == pygame.K_a):
				playerVelocity[0] -= playerSpeed
			elif (event.key == pygame.K_s):
				playerVelocity[2] -= playerSpeed
			elif (event.key == pygame.K_d):
				playerVelocity[0] += playerSpeed
			elif (event.key == pygame.K_q): # Quits game
				pygame.quit()
				quit()
		elif event.type == KEYUP:
			if (event.key == pygame.K_w):
				playerVelocity[2] -= playerSpeed
			elif (event.key == pygame.K_a):
				playerVelocity[0] += playerSpeed
			elif (event.key == pygame.K_s):
				playerVelocity[2] += playerSpeed
			elif (event.key == pygame.K_d):
				playerVelocity[0] -= playerSpeed

	# glRotatef(1, 3, 1, 1)
	
	# TODO: Calculate velocity direction from player facing or smth?
	# TODO: Test if rotation is actually translated like in opengl
	# Abstraction in this case WOULD be quite nice!
	# UPDATE: IT DOES NOT... :/

	glTranslatef(math.sin(playerAngle[1]) * playerVelocity[0], playerVelocity[1], math.cos(playerAngle[1]) * playerVelocity[2])
	#print(playerAngle[1])
	print(playerVelocity)
	print(math.cos(playerAngle[1]))
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	renderScene()
	pygame.display.flip()
	pygame.time.wait(10)
