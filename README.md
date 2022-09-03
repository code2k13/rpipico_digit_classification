# Handwritten digit classification using Raspberry Pi Pico and ML

![Handwritten digit classification using Pi Pico and ML](picoml.gif)

A project using Raspberry Pi Pico, an OV7670 camera module, a 120x160 TFT LCD display and machine learning to build a portable handwritten digit classification system. This code is highly experimental.  Even after you follow all the recommended steps in this article, some tinkering will still be necessary to get it to work.

Link to video demo of project: https://youtu.be/beKvz8K6b_4
## To run the code

You will need following files on your CircuitPython board:
- code.py
- svm_min.py
- Required libraries in *lib* folder. List of all library files you need for the project is present lib_folder_contents.txt 
- You will also need the [Helvetica-Bold-16.bdf](https://raw.githubusercontent.com/adafruit/Adafruit_Learning_System_Guides/master/PyPortal_Astronauts/fonts/Helvetica-Bold-16.bdf) font file for running the code.


## To setup hardware and wiring
For details about setting up the hardware and wiring, please visit:
https://ashishware.com/2022/09/03/pipico_digit_classification/
