import time
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

import config
from comms.pico import Pico
from vision.screenshot import screenshot
from vision.templateMatcher import matchMyTemplate
from engine.rotationController import RotationController
from classes.ds import createDemonSlayer

LOOP_INTERVAL = 0.5
VISION_LOCKOUT = 2.0

# state
pico: Pico = None
controller: RotationController = None
rotation = None
last_restart = 0.0
running = False  # controls the rotation thread loop


# rotation loop (background thread)


def rotation_loop():
    global last_restart, running

    while running:
        try:
            # signals from pico
            # with pico._lock:
            #     if pico.serial.in_waiting > 0:
            #         msg = pico.serial.readline().decode().strip().upper()
            #         if msg == "STOP":
            #             print("Stop signal from Pico button.")
            #             _shutdown()
            #             break
            #         elif msg == "PAUSE":
            #             print("Paused via Pico button.")
            #             controller.pause()
            #             pico.release_all()
            #         elif msg == "RESUME":
            #             print("Resumed via Pico button.")
            #             controller.resume()

            now = time.monotonic()

            # template matching
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

            #  rotation tick 
            controller.update(pico)

        except Exception as e:
            print(f"Rotation loop error: {e}")

        time.sleep(LOOP_INTERVAL)


def _shutdown():
    global running
    running = False
    try:
        pico.release_all()
    except Exception:
        pass


#api app / routes

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    with open("ui.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/pause")
def api_pause():
    controller.pause()
    pico.release_all()
    print("Paused via web UI.")
    return JSONResponse({"status": "paused"})


@app.post("/resume")
def api_resume():
    controller.resume()
    print("Resumed via web UI.")
    return JSONResponse({"status": "running"})


@app.post("/stop")
def api_stop():
    _shutdown()
    print("Stopped via web UI.")
    return JSONResponse({"status": "stopped"})


@app.post("/restart")
def api_restart():
    global last_restart
    pico.release_all()
    controller.restart(randomize=True)
    last_restart = 0.0
    print("Restarted via web UI.")
    return JSONResponse({"status": "running"})


@app.get("/status")
def api_status():
    return JSONResponse({
        "running": running,
        "paused": controller.paused,
        "elapsed": round(controller.elapsed(), 1),
        "rotation": rotation.name,
    })



def main():
    global pico, controller, rotation, running

    pico = Pico()

    demonSlayer = createDemonSlayer()
    rotation = demonSlayer.rotations["TPFarming"]

    controller = RotationController()
    controller.start(rotation)
    rotation.randomizeSteps()

    running = True

    print(f"Starting rotation: {rotation.name}")
    print("Web UI available at http://localhost:8000")
    print("On your phone: http://<your-pc-ip>:8000")

    thread = threading.Thread(target=rotation_loop, daemon=True)
    thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

    # uvicorn blocks until killed — clean up after it exits
    _shutdown()
    pico.close()


if __name__ == "__main__":
    main()