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
            maxOffset=0.2,
            action="TAP"
        )
    )

    tpFarm.addRotationStep(
        RotationStep(
            skill=boundless,
            start=1,
            end=2,
            maxOffset=0.2,
            action="TAP"
        )
    )

    tpFarm.addRotationStep(
        RotationStep(
            skill=concussion,
            start=3,
            end=53,
            maxOffset=0.2,
            action="PRESS"
        )
    )

    tpFarm.addRotationStep(
        RotationStep(
            skill=concussion,
            start=49,
            end=105,
            maxOffset=0.2,
            action="PRESS"
        )
    )


    #intialize rotation
    demonSlayer.addRotation(tpFarm)

    return demonSlayer