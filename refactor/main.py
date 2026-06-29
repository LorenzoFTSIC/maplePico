import time

import config
from comms.pico import Pico
from vision.screenshot import screenshot
from vision.templateMatcher import matchMyTemplate
from engine.rotationController import RotationController
from classes.ds import createDemonSlayer

LOOP_INTERVAL = 0.5
VISION_LOCKOUT = 2.0


def main():
    pico = Pico()

    demonSlayer = createDemonSlayer()
    rotation = demonSlayer.rotations["TPFarming"]

    controller = RotationController()
    controller.start(rotation)
    rotation.randomizeSteps()

    last_restart = 0.0

    print(f"Starting rotation: {rotation.name}")
    print("GP15 = stop | GP14 = pause/resume")

    try:
        while True:

            #  check for signals from Pico
            if pico.serial.in_waiting > 0:
                msg = pico.serial.readline().decode().strip().upper()
                if msg == "STOP":
                    print("Stop signal received.")
                    break
                elif msg == "PAUSE":
                    print("Paused — inputs suppressed, rotation clock continues.")
                    controller.pause()
                elif msg == "RESUME":
                    print("Resumed.")
                    controller.resume()

            now = time.monotonic()

            #  template match (skip while paused) 
            if not controller.paused and now - last_restart >= VISION_LOCKOUT:
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

            controller.update(pico)

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        print("Keyboard interrupt.")

    finally:
        print("Shutting down...")
        try:
            pico.release_all()
        except Exception:
            pass
        pico.close()


if __name__ == "__main__":
    main()