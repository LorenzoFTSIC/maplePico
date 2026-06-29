import time

import config
from comms.pico import Pico
from vision.screenshot import screenshot
from vision.templateMatcher import matchMyTemplate
from engine.rotationController import RotationController
from classes.ds import createDemonSlayer

LOOP_INTERVAL = 1 


def main():
    pico = Pico()

    demonSlayer = createDemonSlayer()
    rotation = demonSlayer.rotations["TPFarming"]

    controller = RotationController()
    controller.start(rotation)
    rotation.randomizeSteps()

    print(f"Starting rotation: {rotation.name}")

    try:
        while True:

            # find buff that triggers a new rotation
            image = screenshot(config.SCREEN_REGION)

            for step in rotation.rotationSteps:
                if step.skill.templateLocation is not None:
                    match = matchMyTemplate(
                        template_path=step.skill.templateLocation,
                        image=image,
                        debug=True
                    )
                    step.vision_ready = match is not None

            controller.update(pico)

            # restart when completes
            total_duration = max(
                step.currentEnd for step in rotation.rotationSteps
            )
            if controller.elapsed() >= total_duration:
                print("Rotation complete — restarting")
                controller.restart(randomize=True)

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        print("Stopping...")
        pico.release_all()
        pico.close()


if __name__ == "__main__":
    main()