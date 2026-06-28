import cv2
import numpy as np

import config


def show_debug(image, matches):

    debug_img = image.copy()

    for (x, y, w, h) in matches:
        cv2.rectangle(
            debug_img,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    cv2.imshow("Template Match Debug", debug_img)
    cv2.waitKey(1)

def matchMyTemplate(template_path, image, debug):

    template = cv2.imread(template_path)

    if template is None:
        raise Exception(f"Could not load {template_path}")

    result = cv2.matchTemplate(
        image,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    locations = np.where(result >= config.MATCH_THRESHOLD)

    matches = []

    h = template.shape[0]
    w = template.shape[1]

    for (x, y) in zip(locations[1], locations[0]):
        # groupRectangles expects duplicate rectangles in order to keep single detections.
        matches.append([int(x), int(y), int(w), int(h)])
        matches.append([int(x), int(y), int(w), int(h)])

    matches, weights = cv2.groupRectangles(matches, 1, 0.2)

    if debug:
        show_debug(image, matches)

    if len(matches) == 0:
        return None

    x, y, w, h = matches[0]


    return {
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "center_x": x + w // 2,
        "center_y": y + h // 2
    }