# Config vars for Simulation.py
VERBOSE = True

WIDTH = 3
HEIGHT = 2
TOTAL_BOXES = WIDTH * HEIGHT

# current format of boxes: (box #, box weight)
def init_load_plan():
    # edit this function as needed to change the input to the program.
    num_boxes = 5
    load_plan = [(i,10-i) for i in range(1, num_boxes+1)]
    return load_plan
LOAD_PLAN = init_load_plan()

NUM_BOXES = len(LOAD_PLAN)
if NUM_BOXES > TOTAL_BOXES:
    print("Too many Boxes, not enough free space. Please Redo config.")
    quit()
