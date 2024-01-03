# RePacker
RePacker is a sophisticated utility crafted to facilitate the rebuilding of Cordova applications. It efficiently removes RASP or other native code security measures, resulting in an enhanced application free from such constraints.

This tool leverages novel techniques to bypass security controls embedded within Cordova apps.

## Requirements
1- **Js2Py** from my repo 
```shell
git clone https://github.com/D4rkTT/Js2Py
cd Js2Py && python3 setup.py install
```
2- Prepare the build environment
  - iOS (requires MacOS):
    - Install Xcode
    - Install npm
    - Install Cordova using npm (Version 9.0 is the most widely used)
  - Android:
    - Install android studio
    - Install npm
    - Install Cordova using npm (Version 9.0 is the most widely used)
3- Download RePacker
```shell
git clone https://github.com/D4rkTT/RePacker
cd RePacker && python3 repacker.py -h
```

## Usage
```shell

    ____       ____             __
   / __ \___  / __ \____ ______/ /_____  _____
  / /_/ / _ \/ /_/ / __ `/ ___/ //_/ _ \/ ___/
 / _, _/  __/ ____/ /_/ / /__/ ,< /  __/ /
/_/ |_|\___/_/    \__,_/\___/_/|_|\___/_/  V0.1


usage: repacker.py [-h] application_file
```
## Encountering Bugs?
RePacker still beta version so if you facing any bugs, please report it in Issues section.

## Known Issues
Users may face a white screen upon running the app. If encountered, try utilizing a different Cordova version. Version 9 is the most popular; however, consider attempting versions above 11 if necessary.

