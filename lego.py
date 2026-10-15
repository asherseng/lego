#!/usr/bin/env python3
import time

# imports the cued_ia_lego library, which contains the NXTBrick and Motor classes
# and associated methods for controlling the motors - we use turn() and wait_for(),
# which turns the motor a specified number of degrees and tells the program to wait
# until the prior movement has finished before continuing, respectively.
from cued_ia_lego import *


# turns the "shooter" motor which turns a rubber wheel 240 degrees to eject a card.
# the number of degrees to turn was experimentally determined.
# smoothstart and brake enable gradual acceleration and deceleration of the "shooter" motor,
# reducing the likelihood of the wheel slipping.
def shoot(shooter):
    shooter.turn(
    240,
    power=100,
    smoothstart=True,
    brake=True
    )
    shooter.wait_for()

# the number of degrees turned is increased for the very first card
# to overcome the initial static friction between the rubber wheel and the card,
# which is greater than the kinetic friction once the wheel is already moving.
def shoot_initial(shooter):
    shooter.turn(
    300,
    power=100,
    smoothstart=True,
    brake=True
    )
    shooter.wait_for()

# rotates the "rotator" motor on which the dealing mechanism is mounted,
# rotating the dealer to the next player.
# the number of degrees to rotate is calculated automatically based on the
# inputted number of players (360 degrees divided by the number of players).
# the power is set to 15 to reduce the angular velocity of the mechanism
# so it doesn't topple. 
# smoothstart, brake, and speedreg are employed for this reason as well. 
# speedreg maintains a constant motor torque even under varying loads.
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

    # attempts to connect to the NXT brick, and exits if it fails.
    try:
        brick = NXTBrick()
    except Exception:
        exit()
    
    # the "rotator" is an instance of the Motor class,
    # which corresponds to an NXT motor.
    # the rotator turns the dealing mechanism.
    rotator = Motor(
    brick, PORT_A
    )

    # the "shooter" is another instance of the Motor class,
    # which corresponds to a different NXT motor.
    # the shooter turns the rubber wheel to eject cards.
    shooter = Motor(
    brick, PORT_B
    )

    # this is where the number of players and the number of cards per player 
    # can be inputted.
    # unfortunately, the NXT brick cannot accept input,
    # so this must be done in the terminal.
    players = int(input("Number of players: "))
    cards = int(input("Number of cards per player: "))

    # the number of cards determines the number of cycles of dealing, with each cycle
    # consisting of each player receiving one card.
    # each iteration of the inner (players) loop ejects one card to the current player,
    # then rotates to the next player.
    # (it is assumed that the players are seated in a circle, so the rotator turns through 
    # 360 degrees divided by the number of players to reach the next player.)
    # as such, the final action of each iteration of the outer (cards) loop is to eject a card
    # to the last player, without rotating to the 'next' player. instead, the rotator turns 
    # back to the first player to begin the next cycle.
    # for the first card/player in each cycle, the shoot_initial() function is called; 
    # for all subsequent cards/players, the regular shoot() function is called.
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

        # for each cycle, after the last player has received their card,
        # the rotator turns in the opposite direction back to the first player - 
        # this is indicated by the minus sign in the argument.
        # the rotator cannot keep rotating in the same direction as it is connected
        # to the NXT brick by a short cable, which would become tangled if it kept
        # rotating in the same direction.
        # the expression for the number of degrees turned back is as such because
        # the rotator does not turn through 360 degrees - this would turn it one full round.
        rotator.turn(-((players-1)/players)*360,
        power=15)

        # as the rotator is turning back, the shooter turns in the opposite direction as well, 
        # rotating the wheel backwards to reset the position of the first card of the next cycle.
        # this is because the arguments of the turn() method of 240 and 300 degrees are slightly 
        # greater than the angle that ejects exactly one card in order to provide some leeway,
        # to ensure that a card is definitely ejected. 
        # this however results in subsequent cards overhanging the wheel (they are partially
        # ejected), so the wheel must be rotated backwards after each cycle to reset 
        # the position of the first card. 
        # 250 degrees was experimentally determined to be sufficient to draw the first card 
        # back in completely.
        shooter.turn(-250,
        power=100,
        smoothstart=True,
        brake=True)
        rotator.wait_for()
        shooter.wait_for()


    if __name__ == "__main__":
        main()
