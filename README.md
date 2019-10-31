# robomaster-vision

### Armour Panel Detection

This approach uses a pipeline of computer vision and machine learning algorithms to detect the center of the panels. At a high level, the pipeline goes as follows:
```
1. Preprocess Image
2. Bitmask LEDs
3. Locate LED rectangles
4. Match target LEDs
5. Compute center of panel
```

Step 4 involves passing a list of rectangles into a convolutional neural network and obtaining the predictions of target led pairs.

### Installation
The installation document can be found [here](https://github.com/ubcrobomaster/robomaster-vision/blob/master/source/tensorflow_pipeline/README.md)

### Raspberry Pi Set-Up (3b+ with USB camera)

1. Install Raspbian 9.0+ 
2. Update and upgrade packages
```
sudo apt update
sudo apt upgrade
```
3. Install necessary system packages
```
sudo apt install libatlas-base-dev
sudo pip install --upgrade pip
```
4. Git clone or download the repository
5. Create a virtual environment and install python packages
```
sudo pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements_rpi.txt
```
6. Run the deploy script
```
cd deploy
./run.sh
```
