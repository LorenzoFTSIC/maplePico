import random
import time


class Rotation:

    def __init__(self, name):

        self.name = name
        self.rotationSteps = []

    def addRotationStep(self, step):
        self.rotationSteps.append(step)

    def randomizeSteps(self):

        if len(self.rotationSteps) == 0:
            return

        # Reset timings
        for step in self.rotationSteps:
            step.currentStart = step.start
            step.currentEnd = step.end

        # First step's start never changes
        self.rotationSteps[0].currentStart = self.rotationSteps[0].start

        for i, step in enumerate(self.rotationSteps):

            if i == 0:

                minimumOffset = (
                step.minimumGap - (step.end - step.start)
                )

                minimumOffset = min(
                    minimumOffset,
                    step.maxOffset
                )

                offset = random.uniform(
                    minimumOffset,
                    step.maxOffset
                )

            else:
                previousStep = self.rotationSteps[i - 1]

                currentGap = step.end - previousStep.currentEnd

                minimumOffset = (
                    -currentGap + step.minimumGap
                )

                minimumOffset = min(
                    minimumOffset,
                    step.maxOffset
                )

                offset = random.uniform(
                    minimumOffset,
                    step.maxOffset
                )

            step.currentEnd += offset

            # Push the next step's start to match
            if i < len(self.rotationSteps) - 1:
                self.rotationSteps[i + 1].currentStart = step.currentEnd