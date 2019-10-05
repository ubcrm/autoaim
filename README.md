# robomaster-vision

### Hardcode

This approach uses a pipeline of computer vision algorithms to detect the center of the panels. At a high level, the pipeline goes as follows:
```
1. Preprocess Image
2. Bitmask LEDs
3. Locate LEDs
4. Match target LEDs
5. Compute center of panel
```

### Machine Learning

Using (tensorflow?) to pair the LEDs and find panels

### Installation
The installation document can be found [here](https://github.com/ubcrobomaster/robomaster-vision/blob/master/LED_match/README.md)

### Repo Structure

Hardcode:

resource.py  ->  put implementation of your computer vision algorithms inside a method in the respective classes.

vision_image  ->   use this driver script to test your algorithms on images. Make use of this to print to the image and visualize the results.

vision_video  ->  this script will be the optimized implementation of the real-time detector

ML: undetermined

Note: Only finished code that is planned on being used should be merged in master branch. For this reason, the ML folder is currently empty. Should someone want to work on ML, they can branch off master or another teammates branch.