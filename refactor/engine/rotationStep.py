
class RotationStep:

    def __init__(self, skill, start, end, action, maxOffset=0):

        self.skill = skill
        self.vision_ready = skill.templateLocation is None

        # Base timings
        self.start = start
        self.end = end

        self.action = action

        # Randomization
        self.maxOffset = maxOffset
        self.minimumGap = 0.05

        # Runtime timings
        self.currentStart = start
        self.currentEnd = end