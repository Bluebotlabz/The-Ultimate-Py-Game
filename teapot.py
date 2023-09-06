from OpenGL.GL import *
from OpenGL.GLU import *
from OBJFileLoader.OBJFileLoader.objloader import OBJ
import math

class Teapot():
    # Location is X, Y, Z
    # Rotation is pitch, yaw, roll
    def __init__(self, teapotModel: OBJ, location: list, rotation=[0,0,0], colour=[1, 0, 0], linewidth=2.5, scale=[1, 1, 1]):
        self.teapotOBJ = teapotModel
        self.location = location
        self.rotation = rotation
        self.linewidth = linewidth
        self.colour = colour
        self.scale = scale

    def tick(self, playerLocation):
        ###
        # Point towards player
        ###

        # First calculate Z distance from player
        zDistance = self.location[2] - playerLocation[2]
        xDistance = self.location[0] - playerLocation[0]

        # Now use tangent to figure out the angle
        if (zDistance == 0):
            print(playerLocation)
            print(self.location)
            print("Z 0")
            return

        ###
        # Move towards player
        ###
        #zDistance -= 0.1
        #xDistance -= 0.1

        print(playerLocation)
        print(self.location)
        print(zDistance)
        print(xDistance)

        self.location[0] -= xDistance / 70
        self.location[2] -= zDistance / 70

        # Recalculate Z distance from player
        zDistance = self.location[2] - playerLocation[2]
        xDistance = self.location[0] - playerLocation[0]

        # Now use tangent to figure out the angle
        if (xDistance == 0):
            self.rotation[1] = 270
            return
        
        if (zDistance == 0):
            angleToPlayer = 0
        else:
            angleToPlayer = math.degrees(math.atan(xDistance/zDistance))
        
        if (zDistance < 0):
            angleToPlayer -= 180
        print("\n")

        # Make the teapot face the player
        self.rotation[1] = angleToPlayer + 270 # Add 270 degrees

    def render(self):
        glPushMatrix()
        glTranslatef(self.location[0], self.location[1], self.location[2])
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glColor(self.colour[0], self.colour[1], self.colour[2])
        glLineWidth(self.linewidth)
        glScale(self.scale[0], self.scale[1], self.scale[2])
        self.teapotOBJ.render()
        glScale(1/self.scale[0], 1/self.scale[1], 1/self.scale[2])
        glRotatef(-self.rotation[0], 1, 0, 0)
        glRotatef(-self.rotation[1], 0, 1, 0)
        glRotatef(-self.rotation[2], 0, 0, 1)
        glTranslatef(-self.location[0], -self.location[1], -self.location[2])
        glPopMatrix()
        