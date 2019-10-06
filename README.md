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
The installation document can be found [here](https://github.com/ubcrobomaster/robomaster-vision/blob/master/source/tensorflow_pipeline/README.md)

### Repo Structure

Hardcode:
```
resource.py  ->  put implementation of your computer vision algorithms inside a method in the respective classes.

vision_image.py  ->   use this driver script to test your algorithms on images. Make use of this to print to the image and visualize the results.

vision_video.py  ->  this script will be the optimized implementation of the real-time detector
```
ML: undetermined

*** Etiquette: 
1. Only finished code should be merged in master branch. For this reason, the ML folder is currently empty. Should someone want to work on ML, they can branch off master or another teammates branch.

2. Do not add unecessary files to your commits. A git ignore is included to help prevent this, but it is good practice to not even include these files in your commits.
A run-time switch can be used to locate datasets and output directories on your local machine.
