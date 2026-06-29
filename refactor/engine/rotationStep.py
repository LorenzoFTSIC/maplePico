class RotationStep:

    def __init__(self, skill, start, end, maxOffset=0):

        self.skill = skill

        # Base timings
        self.start = start
        self.end = end

        # Randomization
        self.maxOffset = maxOffset
        self.minimumGap = 0.05

        # Runtime timings
        self.currentStart = start
        self.currentEnd = end