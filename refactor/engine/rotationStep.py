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