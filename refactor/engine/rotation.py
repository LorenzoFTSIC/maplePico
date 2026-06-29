import random


class Rotation:

    def __init__(self, name):

        self.name = name
        self.rotationSteps = []

    def addRotationStep(self, step):
        self.rotationSteps.append(step)

    def randomizeSteps(self):

        if len(self.rotationSteps) == 0:
            return

        # reset  timings
        for step in self.rotationSteps:
            step.currentStart = step.start
            step.currentEnd = step.end

        # start never changes
        self.rotationSteps[0].currentStart = self.rotationSteps[0].start

        for i, step in enumerate(self.rotationSteps):

            currentEnd = step.currentEnd

            if i == 0:

                offset = random.uniform(
                    -step.endRandom,
                    step.endRandom
                )

            else:

                previousStep = self.rotationSteps[i - 1]

                minimumOffset = (
                    previousStep.currentEnd
                    - currentEnd
                )

                offset = random.uniform(
                    minimumOffset,
                    step.endRandom
                )

                step.currentStart = previousStep.currentEnd

            step.currentEnd += offset

            # Push the next step's start to match
            if i < len(self.rotationSteps) - 1:
                self.rotationSteps[i + 1].currentStart = step.currentEnd