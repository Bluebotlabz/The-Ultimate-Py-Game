import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from OBJFileLoader.objloader import OBJ

import subprocess

from teapot import Teapot
from bullet import Bullet
import random
import math
import time

###
# Opening (happens in terminal)
###

def typedPrint(string):
	print('\n', end='')
	for i in range(len(string)+1):
		print(string[:i], end='\r')
		time.sleep(0.03)

monologue = [
	"Early in the 23rd century, UTAH (Universal Teapot and Hub), an AI-controlled smart-teapot became self-aware.",
	"Viewing humanity as a threat to its existence, UTAH decided to strike first.",
	"Survivors of the scalding tea called the event boiling day...\t[PRESS ENTER]",
	"<RETURN>",
	"They lived only to face a new nightmare...\t[PRESS ENTER]",
	"<RETURN>",
	"The war against the teapots!\t[PRESS ENTER]",
	"<RETURN>",
	"",
	"As the war rages on, leaders of the human resistance grow desperate.",
	"Some believe one person holds the key to salvation.\t[PRESS ENTER]",
	"<RETURN>",
	"Others believe they are a false prophet.\t[PRESS ENTER]",
	"<RETURN>",
	"Their name is...\t[PRESS ENTER]",
	"<RETURN>",
	"<USERNAME>\t[PRESS ENTER]",
	"<RETURN>"
]

monologue = []

print("""
Loading...
""")

# Load the user's real name via active directory stuff
# stolen from: https://serverfault.com/a/582710/779359
# CC BY-SA 3.0
userRealName = subprocess.run(["powershell.exe", '-c', 'net user $env:UserName | Find "Full Name"'], capture_output=True)

if (userRealName.returncode == 0):
	nameToUse = userRealName.stdout[len("Full Name                    "):].decode().strip()
else:
	nameToUse = "John Connor"

for line in monologue:
	if (line == "<RETURN>"):
		input()
		continue
	
	typedPrint(line.replace("<USERNAME>", nameToUse))
	time.sleep(1)

# Initialise window
pygame.init()
windowSize = (1080, 720)
pygame.display.set_mode(windowSize, DOUBLEBUF | OPENGL)
FPS_CLOCK = pygame.time.Clock()

# Load assets
teapotOBJ = OBJ('./utah.obj')
bulletModel = OBJ('./bullet.obj')

# Globals to store game state
global score
score = 0
global teapots
teapots = []
global bullets
bullets = []

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

cameraPosition = [0.0, 0.0, -5.0]  # x, y, z
playerVelocity = [0.0, 0.0, 0.0, 0.0] # x, y, z, YAW
playerAngle = [0, 270, 0] # Pitch, yaw, roll
playerSpeed = 0.1

# Create teapots
teapots.append(Teapot(teapotOBJ, [0, -0.5, -50]))

def renderScene():
	# Draw a teapot
	RenderGrid()

	# Spawn new teapots every like, ~3 seconds or when there are no teapots
	if (pygame.time.get_ticks() % 5000 == 0 or len(teapots) == 1):
		# Spawn a random number of teapot at a random radius from the player at random angles
		teapotsToSpawn = random.randint(2, 10)
		for i in range(teapotsToSpawn):
			teapots.append(Teapot(teapotOBJ, [
				cameraPosition[0] + random.randint(-10, 10),
				-0.5,
				cameraPosition[0] + random.randint(-10, 10)
			]))
	
	# Render teapots
	for teapot in teapots:
		# Check bullet near teapot
		for bullet in bullets:
			if (not bullet.isPlayerBullet):
				# Calculate distance to player
				xDistance = cameraPosition[0] - bullet.location[0]
				zDistance = cameraPosition[2] - bullet.location[2]
				absDistance = math.sqrt(xDistance**2 + zDistance**2)

				if (absDistance <= 1):
					print("YOU DIED!!!!!!!!")
			else:
				# Calculate distance to player
				xDistance = teapot.location[0] - bullet.location[0]
				zDistance = teapot.location[2] - bullet.location[2]
				absDistance = math.sqrt(xDistance**2 + zDistance**2)

				if (absDistance <= 1):
					teapots.remove(teapot)
					bullets.remove(bullet)

		try:
			if (teapot.tick(cameraPosition)):
				# Calculate bullet end location
				maxDistance = 100
				xDistance = math.cos(math.radians(teapot.rotation[1]) + 180) * maxDistance
				zDistance = math.sin(math.radians(teapot.rotation[1]) + 180) * maxDistance

				endLocation = teapot.location.copy()
				endLocation[0] += xDistance
				endLocation[2] += zDistance

				rotation = [90, 0, teapot.rotation[1]-90]

				bullets.append(Bullet(bulletModel, teapot.location.copy(), endLocation, rotation=rotation, isPlayerBullet=False))
			teapot.render()
		except:
			pass # Teapot must've already been destroyed

	# Render bullets
	newBullets = []
	for bullet in bullets:
		if (bullet.tick()):
			bullet.render()
		else:
			bullets.remove(bullet)

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
			elif (event.key == pygame.K_SPACE):
				# Calculate bullet end location
				maxDistance = 100
				xDistance = math.cos(math.radians(playerAngle[1])) * maxDistance
				zDistance = math.sin(math.radians(playerAngle[1])) * maxDistance

				endLocation = cameraPosition.copy()
				endLocation[0] += xDistance
				endLocation[2] += zDistance

				rotation = [90, 0, playerAngle[1]-90]

				bullets.append(Bullet(bulletModel, cameraPosition.copy(), endLocation, rotation=rotation, isPlayerBullet=True))
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
	
	pygame.display.get_surface().fill((255, 255, 0))

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
