import time
import random


class RotationController:

    def __init__(self):
        self.rotation = None

        self.running = False
        self.paused = False

        self.start_time = 0
        self.pause_start = 0
        self.total_pause_time = 0


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
    
    def restart(self):
        self.start_time = time.monotonic()

        self.total_pause_time = 0

    def prepare_rotation(self):
        ##
        ##TODO:: ensure minimum breakpoint of a breakpoint is > the one before it
        ##
        for step in self.rotation.steps:

            step.runtime_start = (
                step.start +
                random.uniform(-0.2, 0.2)
            )

            step.runtime_end = (
                step.end +
                random.uniform(-0.2, 0.2)
            )