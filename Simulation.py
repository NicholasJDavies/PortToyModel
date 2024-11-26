""" Simulation.py
Purpose:
    - Producing a State-space representation of the problem space

Choices:
    - Boxes are labelled 1,2...N
    - Truck schedule is randomized
"""

import random
from itertools import product

# initing input values -- edit at will.
WIDTH = 3
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

def print_state(state):
    print("Printing State:")
    for i in range(WIDTH*HEIGHT):
        row = i % WIDTH
        col = i - row*WIDTH
        if (row == 0):
            print("", end="\n")
        print(f"| {state[i]} |", end="")
    print("\n\n")
    return

def is_full(state):
    """Check if the board is full."""
    return all(cell != 0 for cell in state)

def drop_box(state, column, box):
    """Drop a box into the state, Connect-4 style"""
    # Check if the column is valid
    if column < 0 or column >= WIDTH:
        raise ValueError("Invalid column index.")
    # Traverse the column from bottom to top
    for row in range(0, HEIGHT):
        index = row * WIDTH + column
        if state[index] == 0:  # If the cell is empty
            state[index] = box
            return state  # Successfully dropped the box
        
def generate_moves(state, box):
    """Generate all possible next moves"""
    return [
        drop_box(state[:],i,box)
        for i in range(WIDTH)
    ]

def build_graph(state=None, curr_box=1):
    """Recursively build a graph of all possible Tic-Tac-Toe games."""
    if state is None:
        state = [0 for _ in range(WIDTH*HEIGHT)]  # Start with an empty board
        
    print_state(state)

    # Create a node for the current state
    node = {
        'state': state,
        'children': [] # TODO: children to nodes? who knows, lets not have repeats.
    }

    
    if curr_box == NUM_BOXES or is_full(state):
        return node  # Terminal state, no children

    # Generate child nodes
    next_box = curr_box + 1
    for state in generate_moves(state, curr_box):
        node['children'].append(build_graph(state, next_box))

    return node

# Example usage
root = build_graph()

def count_nodes(node):
    """Count all nodes in the graph."""
    return 1 + sum(count_nodes(child) for child in node['children'])

print("Total nodes:", count_nodes(root))
