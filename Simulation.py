""" Simulation.py
Purpose:
    - Producing a State-space representation of the problem space

Choices:
    - Boxes are labelled 1,2...N
    - Truck schedule is randomized
"""

import random

# initing input values -- edit at will.
WIDTH = 2
HEIGHT = 2
TOTAL = WIDTH * HEIGHT

NUM_BOXES = 4
if NUM_BOXES > TOTAL:
    print("retry pls, too many boxes to fit")
    quit()

# initialization of other vals.
BOX_SCHEDULE = random.shuffle(list(range(1,NUM_BOXES)))
CURR_BOX = 0

INPUT_LOAD = list(range(1,NUM_BOXES))
