class RotationStep:

    def __init__(self, skill, start, end):

        self.skill = skill

        self.start = start
        self.end = end
        #move to rotationcontroller?
        self.rndmDelay = 0

        self.runtime_start = start
        self.runetime_end = end


    def is_active(self, elapsed):

        return (
            self.start + self.rndmDelay
            <= elapsed
            <
            self.end + self.rndmDelay
        )
        # RotationStep(
        #     skill=crunch,
        #     start=0,
        #     end=1
        # ),

        # RotationStep(
        #     skill=boundless,
        #     start=2,
        #     end=4
        # ),

        # RotationStep(
        #     skill=concussion,
        #     start=5,
        #     end=46
        # ),

        # RotationStep(
        #     skill=concussion,
        #     start=48,
        #     end=120
        # )
    