from engine.character import Character
from engine.skill import Skill
from engine.action import Action
from engine.rotationStep import RotationStep

from adafruit_hid.keycode import Keycode


def createDemonSlayer():

    demonSlayer = Character("demonSlayer")

    # Skills
    concussion = Skill(
            name="concussion",
            key=Keycode.RIGHT_ALT,
            action=Action.HOLD
        )

    boundless = Skill(
            name="boundless",
            key=Keycode.THREE,
            action=Action.TAP
        )

    crunch = Skill(
            name="crunch",
            key=Keycode.FOUR,
            action=Action.TAP
        )
    
    #initialize skills
    demonSlayer.add_skill(concussion)
    demonSlayer.add_skill(boundless)
    demonSlayer.add_skill(crunch)
    

    # Rotation
    demonSlayer.rotations = {}

    return demonSlayer