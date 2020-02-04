Easy ADB Tool

This is my first Python app I've ever build. Messy code and intending bugs you will find when using.
The tool helps me and my friends on target the Android device when testing. Install application build for the test and capture screenshots to save evidences for testing report.
It will have Screen Record function very soon and bug fixing as well.

<hr>
BEFORE GET START

Make sure you have ADB binary available on your system.
Download from:
+ Windows: https://dl.google.com/android/repository/platform-tools-latest-windows.zip
+ MacOS: https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
+ Linux: https://dl.google.com/android/repository/platform-tools-latest-linux.zip

<hr>
HOW TO BUILD

This project is based on Python 3. It requires to have Python 3 installed on your system.
Make sure you have Pip3 and installed all required packages from 'requirements' file by running:
> pip3 install -r requirements

To build the project, you need the Pyinstaller (already installed from the above step) then run the following:
> pyinstaller adbtool.py -windowed

You will get 2 new folders: build and dist. You executable file is located in 'dist'.
Depending on your OS when building, you will have Mac, Windows or Linux executable file.

