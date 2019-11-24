# Raspberry Pi Set-Up

### Step 0 - Requirements

* Hardware: Raspberry Pi 3B, 3B+ or 4B
* OS: Raspbian *Buster*
* SD Card: 16GB+
* USB camera
* This tutorial assumes you are using the !/bin/bash shell interpreter

### Step 1 - Install OS

* Flash Raspbian Buster onto micro sd card, using Balena Etcher
* Boot raspberry pi from sd card, follow configuration prompts

### Step 2 (Optional) - Expand filesystem, reclaim space

```
sudo raspi-config
```

Select "Advanced Options" -> "Expand Filesystem".
Then reboot.

Remove wolfram and libreoffice,

```
sudo apt-get purge wolfram-engine
sudo apt-get purge libreoffice*
sudo apt-get clean
sudo apt-get autoremove
```

### Step 3 - Clone/Download robomaster-vision repository

```
cd ~
git clone https://github.com/ubcrobomaster/robomaster-vision.git
```

### Step 4 - Install system dependencies

```
cd ~/robomaster-vision/raspberrypi_setup
sudo chmod a+x install_dependencies_rpi.sh
./install_dependencies_rpi.sh
```

### Step 5 - Build Python 3.6 (~30min)

```
cd ~
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
make
sudo make altinstall
```

### Step 6 - Set-up virtual python environment (~1h, need to build numpy, scipy, wrapt, and h5py)

```
cd ~/robomaster-vision
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements_rpi.txt
```

### Step 7 - Build and Install OpenCV 4.1.1 with floating point ARM optimizations (~3h)

```
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.1.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.1.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.1.1 opencv
mv opencv_contrib-4.1.1 opencv_contrib
```

Increase the SWAP space on your sd card,

```
sudo nano /etc/dphys-swapfile
```

change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024,
restart swap service,

```
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

Now begin compilation, this can take 2-4 hours.

```
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
    -D BUILD_EXAMPLES=OFF ..
make -j4
sudo make install
sudo ldconfig
```

This is a good time to reset your SWAP back to 100 to avoid burning out the sd card.

### Step 8 - Link your opencv binary to your virtual environment

```
cd /usr/local/lib/python3.6/site-packages/cv2/python-3.6
sudo mv cv2.cpython-36m-arm-linux-gnueabihf.so cv2.so
cd ~/robomaster-vision/venv/lib/python3.6/site-packages/
ln -s /usr/local/lib/python3.6/site-packages/cv2/python-3.6/cv2.so cv2.so
```

### Step 9 - Test Run

```
cd ~/robomaster-vision/deploy
./run.sh
```

Resources - To read more about the process checkout
https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

