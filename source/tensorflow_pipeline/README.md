# LED Matching
Using Tensorflow to pair LEDs

## Requirements

```
python==3.7.4
```

## Installation
How to install and setup the

Windows:
```
pip install virtualenv
virtualenv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

Linux/Mac:
```
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt --no-cache-dir
``` 

## Maintenance

### Tensorflow Pipeline
When updating python packages, be sure to run:
```
pip freeze > requirements.txt
```
