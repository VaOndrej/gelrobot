Install all required packages

0) First copy video in .mp4 format inside root folder

0.1) install poetry: pip install poetry

0.2) run: poetry install

This project consists of two scripts

1) save_robot.py (run: python3 save_robot.py)
    Before running script, set diameter "r" on line 31 to some desired value for example 36
    This script is run first and its purpose is to find the gel robot, diameter for circle where to find the hair and R, G, B values for hair
    Using middle mouse button get color of hair.
    Using left mouse button choose the middle of the gel robot.
    Both outputs will be printed into terminal.
    Get the outputs from terminal and pass them to main.py as specified in step 2.

1.1) The window can be closed using ctrl+D

2) Then all these values need to be passed to main.py and its output is graph of angular velocity for the gel robot    
    example run: python3 main.py --x 332 --y 97 --diameter 36 --red 112 --green 106 --blue 107


Missing import Tkinter:
For linux install: sudo apt-get install python3-tk
