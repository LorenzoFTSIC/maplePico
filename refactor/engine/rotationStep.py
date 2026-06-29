class RotationStep:

    def __init__(self, skill, start, end, randomization=0):

        self.skill = skill

        # Base timings
        self.start = start
        self.end = end

        # Runtime timings
        self.currentStart = start
        self.currentEnd = end

        self.randomization = randomization