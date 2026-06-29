import random


class Rotation:

    def __init__(self, name):
        self.name = name
        self.rotationSteps = []

    def addRotationStep(self, step):
        self.rotationSteps.append(step)

    def randomizeSteps(self):
        for step in self.rotationSteps:
            offset = random.uniform(-step.maxOffset, step.maxOffset)
            step.currentStart = step.start + offset
            step.currentEnd = step.end + offset