from math import sqrt

from numpy.ma import arctan
from target_to_coords_config import *


# take x,y (x, y coords from the vedio), distance , f (focal legnth)
# produce rho,phi,z (cyliderical coords) raltevie to camera

def target_to_coords(target, debug):
    print("target_to_coords starts")
    if target is not None:
        x,y = target.loc
        distance = target.distance;
        # get x,y,distance from target,  x=0 and y=0 is the upper left conrer of image
        # x and y are the row and columu number of position on the vedio, distance is the actual distance to target

        x -= TOTAL_NUMBER_OF_PIXELS_IN_X_AXIS / 2
        y -= TOTAL_NUMBER_OF_PIXELS_IN_Y_AXIS / 2
        # making x,y relative to the center of image (so that x=0 and y=0 is the center of image, for example)

        x_image_size = x * PIXEL_SIZE
        y_image_size = y * PIXEL_SIZE
        # get the actual image size on the camera using pixel size

        x_cartesian = x_image_size * distance / FOCU_LENGTH
        y_cartesian = y_image_size * distance / FOCU_LENGTH
        # get x,y in Catrsian coords of target in real world relative to camera using camera matrix
        z_cartesian = sqrt(distance * distance  - x_cartesian * x_cartesian - y_cartesian * y_cartesian)
        # get z in Catrsian coords of target in real world relative to camera using pythagorean theorem
        # z direction in cartesian coords is the direction that the camera is pointing at

        phi_cylindrical = arctan(x_cartesian / z_cartesian)
        rho_cylindrical = z_cartesian
        z_cylindrical = y_cartesian
        # convert Catrsian coords to Cyliderical coords

        cylindrical_coords_phi_rho_z = (phi_cylindrical, rho_cylindrical, z_cylindrical)

        #temp print
        print("finished target_to_coords and return")
        print(cylindrical_coords_phi_rho_z)

        return cylindrical_coords_phi_rho_z
