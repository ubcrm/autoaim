import numpy as np
import cv2

PIXEL_SIZE = 1.4E-6  # (m)
FOCAL_LENGTH = 28E-3  # (m)
CAMERA_CONSTANT = 8E-4  # (PIXEL_SIZE / FOCAL_LENGTH) does not produce accurate result

COLOR = (255, 255, 255)
FONT = 0
FONT_SIZE = 0.5
LABEL_POSITION = (0.36, 0.96)


def target_to_coords(target, com):
    if target is None:
        return None

    distance = target.distance
    x, y = (target.center - com.orig_dims // 2) * distance * CAMERA_CONSTANT
    z = np.sqrt(distance ** 2 - x ** 2 - y ** 2)
    rho, phi, z = z, np.arctan2(x, z), -y

    if com.debug:
        label = f'rho, phi, z = {rho:.2f}, {np.rad2deg(phi):.1f}, {z:.2f}'
        label_position = tuple(com.orig_to_debug(np.multiply(com.orig_dims, LABEL_POSITION)))
        cv2.putText(com.debug_frame, label, label_position, FONT, FONT_SIZE, COLOR)
    return rho, phi, z
