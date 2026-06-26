from engine.character import Character
from engine.skill import Skill
from engine.action import Action
from engine.rotation import RotationStep

from adafruit_hid.keycode import Keycode


def create_character():

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
    demonSlayer.rotation = [

        RotationStep(
            skill=crunch,
            start=0,
            end=1
        ),

        RotationStep(
            skill=boundless,
            start=2,
            end=4
        ),

        RotationStep(
            skill=concussion,
            start=5,
            end=46
        ),

        RotationStep(
            skill=concussion,
            start=48,
            end=120
        )
    ]

    return demonSlayer