import time
from engine.action import Action


class RotationController:

    def __init__(self):
        self.rotation = None

        self.running = False
        self.paused = False

        self.start_time = 0
        self.pause_start = 0
        self.total_pause_time = 0

        # track held PRESS keys
        self._held_steps = set()

    def start(self, rotation):
        self.rotation = rotation

        self.running = True
        self.paused = False

        self.start_time = time.monotonic()
        self.total_pause_time = 0

    def stop(self):
        self.running = False
        self.paused = False

    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_start = time.monotonic()

    def resume(self):
        if self.paused:
            paused_time = time.monotonic() - self.pause_start
            self.total_pause_time += paused_time
            self.paused = False

    def elapsed(self):
        if not self.running:
            return 0
        return (
            time.monotonic()
            - self.start_time
            - self.total_pause_time
        )

    def restart(self, randomize=True):
        self.start_time = time.monotonic()
        self.total_pause_time = 0
        self._held_steps.clear()

        if randomize:
            self.rotation.randomizeSteps()

    def update(self, pico):
        if not self.running or self.paused:
            return

        elapsed = self.elapsed()

        for i, step in enumerate(self.rotation.rotationSteps):

            start = step.currentStart
            end = step.currentEnd
            action = step.action
            key = step.skill.key.value

            in_window = start <= elapsed < end

            if action == "TAP":
                if in_window and step.vision_ready:
                    pico.tap(key)

            elif action == "PRESS":
                if in_window and step.vision_ready and i not in self._held_steps:
                    pico.press(key)
                    self._held_steps.add(i)
                elif not in_window and i in self._held_steps:
                    pico.release(key)
                    self._held_steps.discard(i)
