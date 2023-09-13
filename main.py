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
print("""
Loading...
""")

###
# Load sound files
###
pygame.mixer.init()
reload_sound = pygame.mixer.Sound("./sounds/196907__dpoggioli__laser-gun-recharge.wav")
death_sound = pygame.mixer.Sound("./sounds/542565__matthewholdensound__owi_crystalclass-shatter.wav")
laser_sound1 = pygame.mixer.Sound("./sounds/667650__deltacode__weapon_laser1.wav")
laser_sound2 = pygame.mixer.Sound("./sounds/667651__deltacode__weapon-laser2.wav")

# load music
pygame.mixer.music.load('./sounds/dark-night-141315.mp3')

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
screen = pygame.display.set_mode(windowSize, DOUBLEBUF | OPENGL)
FPS_CLOCK = pygame.time.Clock()

# Start music
pygame.mixer.music.play(-1)

# Load assets
teapotOBJ = OBJ('./utah.obj')
bulletModel = OBJ('./bullet.obj')

# Globals to store game state
global score
score = 0
global ammo
ammo = 0
global teapots
teapots = []
global bullets
bullets = []

def RenderGrid(size=70):
	glLineWidth(1)
	glColor(0, 0.5, 0)
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

bulletCooldown = 0
score = 0

global health
health = 100

# Create teapots
teapots.append(Teapot(teapotOBJ, [0, -0.5, -50]))

def renderScene():
	global score
	global health

	RenderGrid()

	# Spawn new teapots every like, ~5 seconds or when there are no teapots
	if (pygame.time.get_ticks() % 5000 == 0 or len(teapots) == 1):
		# Spawn a random number of teapot at a random radius from the player at random angles
		teapotsToSpawn = random.randint(2, 10)
		for i in range(teapotsToSpawn):
			teapots.append(Teapot(teapotOBJ, [
				cameraPosition[0] + random.randint(-10, 10),
				-0.5,
				cameraPosition[2] + random.randint(-10, 10)
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
					bullets.remove(bullet)
					health -= 5
					print("\nYOU HAVE BEEN HIT!")
					print("HEALTH:", health)
					print("SCORE:", score)
			else:
				# Calculate distance to player
				xDistance = teapot.location[0] - bullet.location[0]
				zDistance = teapot.location[2] - bullet.location[2]
				absDistance = math.sqrt(xDistance**2 + zDistance**2)

				if (absDistance <= 1):
					death_sound.play()
					teapots.remove(teapot)
					bullets.remove(bullet)
					score += 1
					if (health < 100):
						health += 1 # Destroying a UTAH allows you to absorb its mechanical life force, unethical? Probably, but how else will you recover health?
					print("\nDESTROYED A UTAH!")
					print("HEALTH:", health)
					print("SCORE:", score)

		try:
			if (teapot.tick(cameraPosition)):
				# Calculate bullet end location
				maxDistance = 100
				xDistance = math.cos(math.radians((teapot.rotation[1] * -1) + 180)) * maxDistance
				zDistance = math.sin(math.radians((teapot.rotation[1] * -1) + 180)) * maxDistance

				endLocation = teapot.location.copy()
				endLocation[0] += xDistance
				endLocation[2] += zDistance

				rotation = [90, 0, teapot.rotation[1]]

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
	playerSpeed = 0.05 + (0.05 * (health/100))

	if (health <= 0):
		print("========== GAME OVER!!! ==========")
		print('= ' + ("Score:\t" + str(score)).center(25) + ' =')
		print("==================================")
		pygame.quit()
		exit()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == KEYDOWN:
			if (event.key == pygame.K_w):
				playerVelocity[2] -= 1
			elif (event.key == pygame.K_a):
				playerVelocity[0] -= 1
			elif (event.key == pygame.K_s):
				playerVelocity[2] += 1
			elif (event.key == pygame.K_d):
				playerVelocity[0] += 1
			elif (event.key == pygame.K_LEFT):
				playerVelocity[3] -= 7
			elif (event.key == pygame.K_RIGHT):
				playerVelocity[3] += 7
			elif (event.key == pygame.K_SPACE and bulletCooldown == 0):
				# Calculate bullet end location
				maxDistance = 100
				xDistance = math.cos(math.radians(playerAngle[1])) * maxDistance
				zDistance = math.sin(math.radians(playerAngle[1])) * maxDistance

				endLocation = cameraPosition.copy()
				endLocation[0] += xDistance
				endLocation[2] += zDistance

				rotation = [90, 0, playerAngle[1]-90]

				bullets.append(Bullet(bulletModel, cameraPosition.copy(), endLocation, rotation=rotation, isPlayerBullet=True))

				if (random.randint(0, 10) > 5):
					laser_sound1.play()
				else:
					laser_sound2.play()

				bulletCooldown = 10 # Time to wait between bullet fires
				ammo -= 1
			elif (event.key == pygame.K_q): # Quits game
				pygame.quit()
				quit()
		elif event.type == KEYUP:
			if (event.key == pygame.K_w):
				playerVelocity[2] += 1
			elif (event.key == pygame.K_a):
				playerVelocity[0] += 1
			elif (event.key == pygame.K_s):
				playerVelocity[2] -= 1
			elif (event.key == pygame.K_d):
				playerVelocity[0] -= 1
			elif (event.key == pygame.K_LEFT):
				playerVelocity[3] += 7
			elif (event.key == pygame.K_RIGHT):
				playerVelocity[3] -= 7

	#glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])
	#glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])

	if (ammo == 0):
		reload_sound.play()
		ammo = 10

	playerAngle[1] += playerVelocity[3]
	cameraPosition[0] -= math.sin(math.radians(playerAngle[1])) * (playerVelocity[0] * playerSpeed)   +   math.cos(math.radians(playerAngle[1])) * (playerVelocity[2] * playerSpeed)
	cameraPosition[1] += playerVelocity[1]
	cameraPosition[2] -= math.cos(math.radians(playerAngle[1]+180)) * (playerVelocity[0] * playerSpeed)   +   math.sin(math.radians(playerAngle[1])) * (playerVelocity[2] * playerSpeed)

	# Countdown the bullet timer thing
	if (bulletCooldown != 0):
		bulletCooldown -= 1
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glTranslatef(-cameraPosition[0], -cameraPosition[1], -cameraPosition[2])
	renderScene()
	glTranslatef(cameraPosition[0], cameraPosition[1], cameraPosition[2])
	glRotatef(playerVelocity[3], 0, 1, 0)

	pygame.display.flip()
	FPS_CLOCK.tick(30)
