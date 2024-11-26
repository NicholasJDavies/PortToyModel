# Config vars for Simulation.py
VERBOSE = True

WIDTH = 5
HEIGHT = 5
TOTAL_BOXES = WIDTH * HEIGHT

NUM_BOXES = 4
if NUM_BOXES > TOTAL_BOXES:
    print("Too many Boxes, not enough free space. Please Redo config.")
    quit()
