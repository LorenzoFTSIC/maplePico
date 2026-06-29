from engine.character import Character
from engine.skill import Skill
from engine.action import Action
from engine.rotation import Rotation
from engine.rotationStep import RotationStep
from engine.input import Input

def createDemonSlayer():

    demonSlayer = Character("demonSlayer")

    # Skills
    concussion = Skill(
            name="concussion",
            key=Input.RIGHT_ALT
        )

    boundless = Skill(
            name="boundless",
            key=Input.THREE,
            templateLocation="./ss/pc/relentless.png"
        )

    chomp = Skill(
            name="chomp",
            key=Input.FOUR
        )
    
    #rotations
    tpFarm = Rotation("TPFarming")

    #rotation steps
    tpFarm.addRotationStep(
        RotationStep(
            skill=chomp,
            start=0,
            end=1,
            maxOffset=0.15,
            action="TAP"
        )
    )

    tpFarm.addRotationStep(
        RotationStep(
            skill=boundless,
            start=1,
            end=2,
            maxOffset=0.15,
            action="TAP"
        )
    )

    tpFarm.addRotationStep(
        RotationStep(
            skill=concussion,
            start=2,
            end=62.5,
            maxOffset=0.2,
            action="PRESS"
        )
    )

    tpFarm.addRotationStep(
        RotationStep(
            skill=concussion,
            start=63,
            end=123,
            maxOffset=0.2,
            action="PRESS"
        )
    )


    #intialize rotation
    demonSlayer.addRotation(tpFarm)

    return demonSlayer