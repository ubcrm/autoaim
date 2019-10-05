import sensor, image, time

EXPOSURE_TIME_SCALE = 0.1 # 1/10th of normal exposure
red_threshold_01 = (30, 100, 33, 127, -128, 78) #LAB values（minL, maxL, minA, maxA, minB, maxB）

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.
sensor.skip_frames(500) # Let new settings take affect.
sensor.set_auto_whitebal(False) #Shut off white balance

current_exposure_time_in_microseconds = sensor.get_exposure_us()
sensor.set_auto_exposure(False, \
    exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))

clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.
    #  pixels_threshold=100, area_threshold=100
    blobs = img.find_blobs([red_threshold_01], area_threshold=5)

    if blobs:
    #If found color
        print(blobs)
        for b in blobs:
            # Draw a rect around the blob.
            img.draw_rectangle(b[0:4]) #rect
            img.draw_cross(b[5], b[6]) #cx, cy

    print(clock.fps()) # Not really necessary, just to look at how it's running
