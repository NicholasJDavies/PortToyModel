""" Simulation.py

"""

import random
from itertools import product
from config import VERBOSE, NUM_BOXES, WIDTH, HEIGHT, TOTAL_BOXES
from copy import deepcopy

# initialization of vals.
BOX_SCHEDULE = random.shuffle(list(range(1,NUM_BOXES)))
TOTAL_NODES = 0
EMPTY_BOX = (0,0)

INPUT_LOAD = list(range(1,NUM_BOXES))

def print_state(node):
    print("\nPrinting State:")
    print(f"Touches so far: {node['touches']}")
    print(f"Parent Node: {node['parent node']}")
    print(f"Node: {node['current node']}")
    yard = node['state']['yard']
    print("yard:")
    for row in range(HEIGHT - 1, -1, -1):
        for col in range(WIDTH):
            index = row*WIDTH+col
            box = yard[index]
            print(f"| {(str(box[0]) + ', ' + str(box[1])) if box != EMPTY_BOX else '    ' } |", end="")
        print("", end="\n")

    load_plan = node['state']['load plan']
    print("load plan:")
    for box in load_plan:
        print(f"| {(str(box[0]) + ', ' + str(box[1]))} |", end="")
    print("", end="\n")

    print("\n\n-------------------------------------------")
    return

def is_full(yard):
    """Check if the board is full."""
    return all(box[0] != 0 for box in yard)

def is_empty(load_plan):
    return len(load_plan) == 0

def drop_box(state, column, box):
    """Drop a box into the state, Connect-4 style"""
    # Check if the column is valid
    if column < 0 or column >= WIDTH:
        raise ValueError("Invalid column index.")
    # Traverse the column from bottom to top
    box_weight = box[1]
    prev_weight = float('inf') # begins @ infinity
    for row in range(0, HEIGHT):
        index = row * WIDTH + column
        
        stacked_box = state[index]
        if stacked_box == EMPTY_BOX:  # cell is empty
            if box_weight <= prev_weight:
                state[index] = box
                return state  # Successfully dropped the box
            else:
                return None
        else:
            prev_weight = stacked_box[1]
    return None # no empty cells.
        
def generate_moves(state):
    """Generate all possible states after the next move
    Some future planning to allow for easy transition to a different format of load_plan
    """

    child_states = []
    boxes = []
    yard = state['yard']
    load_plan = state['load plan']

    for i in range(1):
        boxes.append(load_plan[0])

    for i in range(WIDTH):
        child_state = {
            'yard':deepcopy(yard),
            'load plan': deepcopy(load_plan)
        }
        next_box = boxes[0]
        index_next_box = child_state['load plan'].index(next_box)
        child_state['load plan'].pop(index_next_box)

        child_state['yard'] = drop_box(child_state['yard'],i,next_box)
        if child_state['yard'] == None:
            continue
        else:
            child_states.append(child_state)
    return child_states

def init_load_plan():
    # needs num boxes.
    load_plan = [(i,4-i) for i in range(1, NUM_BOXES)]
    return load_plan

def build_graph(state=None, touches=0, node_num=0, parent_node= None):
    """Recursively build a graph of all possible Tic-Tac-Toe games."""
    if state is None:
        state = {
            'yard': [EMPTY_BOX for _ in range(WIDTH*HEIGHT)],  # Start with an empty board
            'load plan': init_load_plan()
        }

    # Create a node for the current state
    node = {
        'state': state,
        'parent node': parent_node,
        'current node': node_num,
        'touches': touches,
        'children': []
    }

    if VERBOSE:
        print_state(node)

    if is_empty(state['load plan']) or is_full(state['yard']):
        return node # terminal state / solution state

    for child_state in generate_moves(state):
        global TOTAL_NODES
        TOTAL_NODES += 1
        node['children'].append(build_graph(child_state, touches+1, TOTAL_NODES, node_num))
        
    return node

# usage
root = build_graph()

def count_nodes(node):
    """Count all nodes in the graph (Recursive)"""
    return 1 + sum(count_nodes(child) for child in node['children'])

print("Total nodes:", count_nodes(root))
