from OpenGL.GL import *
from OpenGL.GLU import *
from OBJFileLoader.objloader import OBJ
import math

class Bullet():
    # Location is X, Y, Z
    # Rotation is pitch, yaw, roll
    def __init__(self, bulletModel: OBJ, locationStart: list, locationEnd: list, rotation=[90,0,0], colour=[1, 1, 1], linewidth=2.5, scale=[0.4, 0.4, 0.4], bulletSpeed=0.5, isPlayerBullet=False):
        self.bulletModel = bulletModel
        self.locationStart = locationStart.copy()
        self.locationEnd = locationEnd
        self.location = locationStart.copy()
        self.rotation = rotation
        self.linewidth = linewidth
        self.colour = colour
        self.scale = scale
        self.bulletSpeed = bulletSpeed # Measured in m/t (meteres per tick) (each tick happens 30 times a second)
        self.isPlayerBullet = isPlayerBullet

    def tick(self):
        # Move the bullet
        bulletXTravel = self.locationEnd[0] - self.locationStart[0]
        bulletZTravel = self.locationEnd[2] - self.locationStart[2]

        if (abs(bulletZTravel) <= 0.3 and abs(bulletXTravel) <= 0.3):
            # Bullet has been destroyed!
            return False
        
        bulletDistance = math.sqrt(bulletXTravel**2 + bulletZTravel**2)
        percentageToTravel = self.bulletSpeed / bulletDistance # Calculate the percentage to travel to travel bulletSpeed meters in a tick

        self.location[0] += bulletXTravel * percentageToTravel
        self.location[2] += bulletZTravel * percentageToTravel
        return True

    def render(self):
        glPushMatrix()
        glTranslatef(self.location[0], self.location[1], self.location[2])
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glColor(self.colour[0], self.colour[1], self.colour[2])
        glLineWidth(self.linewidth)
        glScale(self.scale[0], self.scale[1], self.scale[2])
        self.bulletModel.render()
        glScale(1/self.scale[0], 1/self.scale[1], 1/self.scale[2])
        glRotatef(-self.rotation[0], 1, 0, 0)
        glRotatef(-self.rotation[1], 0, 1, 0)
        glRotatef(-self.rotation[2], 0, 0, 1)
        glTranslatef(-self.location[0], -self.location[1], -self.location[2])
        glPopMatrix()
        