#!/usr/bin/env python3
import time
from cued_ia_lego import *
spins rubber wheel to eject one card

def shoot(shooter):
shooter.turn(
240,
power=100,
smoothstart=True,
brake=True
)
shooter.wait_for()

degrees turned and power increased, just for the first card

def shoot_initial(shooter):
shooter.turn(
300,
power=100,
smoothstart=True,
brake=True
)
shooter.wait_for()
rotates the machine to turn to different players

def rotate(rotator, degrees):
rotator.turn(
degrees,
power=15,
speedreg=True,
smoothstart=True,
brake=True
)
rotator.wait_for()
def main():
try:
brick = NXTBrick()
except Exception:
exit()
# "rotator" rotates dealer
rotator = Motor(
brick, PORT_A
)
# "shooter" turns wheel shooter
shooter = Motor(
brick, PORT_B
)
players = int(input("Number of players: "))
cards = int(input("Number of cards per player: "))
for c in range(cards):
for p in range(players-1):
if p == 0:
shoot_initial(shooter)
shooter.wait_for()
rotate(rotator, 360/players)
rotator.wait_for()
else:
shoot(shooter)
shooter.wait_for()
rotate(rotator, 360/players)
rotator.wait_for()
shoot(shooter)
shooter.wait_for()

rotator.turn(-((players-1)/players)360,
power=15)
shooter.turn(-250,
power=100,
smoothstart=True,
brake=True)
rotator.wait_for()
shooter.wait_for()

if __name__ == "__main__":
main()
