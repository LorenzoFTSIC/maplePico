from engine.character import Character
from engine.skill import Skill
from engine.action import Action
from engine.rotation import Rotation
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

    chomp = Skill(
            name="chomp",
            key=Keycode.FOUR,
            action=Action.TAP
        )
    
    #rotations
    universalTraining = Rotation("TPFarming")

    #rotation steps
    universalTraining.addStep(
        RotationStep(
            skill=chomp,
            start=0,
            end=1
        )
    )

    universalTraining.addStep(
        RotationStep(
            skill=boundless,
            start=1,
            end=2
        )
    )

    universalTraining.addStep(
        RotationStep(
            skill=concussion,
            start=3,
            end=53
        )
    )

    universalTraining.addStep(
        RotationStep(
            skill=concussion,
            start=49,
            end=105
        )
    )


    #intialize rotation
    demonSlayer.addRotation(universalTraining)

    return demonSlayer