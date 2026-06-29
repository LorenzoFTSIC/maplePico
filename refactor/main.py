import time

import config
from comms.pico import Pico
from vision.screenshot import screenshot
from vision.templateMatcher import matchMyTemplate
from engine.rotationController import RotationController
from classes.ds import createDemonSlayer

LOOP_INTERVAL = 0.5       
VISION_LOCKOUT = 8.0       # seconds to ignore vision after a restart


def main():
    print("waiting a sec to tab in")
    time.sleep(1)

    pico = Pico()

    demonSlayer = createDemonSlayer()
    rotation = demonSlayer.rotations["TPFarming"]

    controller = RotationController()
    controller.start(rotation)
    rotation.randomizeSteps()

    last_restart = 0.0

    print(f"Starting rotation: {rotation.name}")

    try:
        while True:

            now = time.monotonic()

            # --- Vision pass ---
            if now - last_restart >= VISION_LOCKOUT:
                image = screenshot(config.SCREEN_REGION)

                for step in rotation.rotationSteps:
                    if step.skill.templateLocation is not None:
                        match = matchMyTemplate(
                            template_path=step.skill.templateLocation,
                            image=image,
                            debug=False
                        )
                        if match is not None:
                            print(f"{step.skill.name} ready — restarting rotation")
                            pico.release_all()
                            controller.restart(randomize=True)
                            last_restart = time.monotonic()
                            break

            # --- Rotation tick ---
            controller.update(pico)

            time.sleep(LOOP_INTERVAL)


    except Exception as e:
        print(f"CRASH: {e}")
        import traceback
        traceback.print_exc()
        pico.release_all()
        pico.close()

    except KeyboardInterrupt:
        print("Stopping...")
        pico.release_all()
        pico.close()


if __name__ == "__main__":
    main()