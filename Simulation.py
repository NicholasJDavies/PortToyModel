""" Simulation.py

"""

import random
from itertools import product
from config import VERBOSE, NUM_BOXES, WIDTH, HEIGHT, TOTAL_BOXES

# initialization of vals.
BOX_SCHEDULE = random.shuffle(list(range(1,NUM_BOXES)))
CURR_BOX = 0
TOTAL_NODES = 0

INPUT_LOAD = list(range(1,NUM_BOXES))

def print_state(node):
    print("\nPrinting State:")
    print(f"Touches so far: {node['touches']}")
    print(f"Parent Node: {node['parent node']}")
    print(f"Node: {node['current node']}")
    state = node['state']
    for row in range(HEIGHT - 1, -1, -1):
        for col in range(WIDTH):
            index = row*WIDTH+col
            print(f"| {state[index] if state[index] != 0 else ' ' } |", end="")
        print("", end="\n")

    print("\n\n-------------------------------------------")
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
    return None # no empty cells.
        
def generate_moves(state, box):
    """Generate all possible next moves"""
    child_states = []
    for i in range(WIDTH):
        child_state = drop_box(state[:],i,box)
        if child_state == None:
            continue
        else:
            child_states.append(child_state)
    return child_states

def build_graph(state=None, curr_box=1, touches=0, node_num=0, parent_node= None):
    """Recursively build a graph of all possible Tic-Tac-Toe games."""
    if state is None:
        state = [0 for _ in range(WIDTH*HEIGHT)]  # Start with an empty board

    
    # Create a node for the current state
    node = {
        'state': state,
        'parent node': parent_node,
        'current node': node_num,
        'touches': touches,
        'children': [] # TODO: stop repeats
    }

    if VERBOSE:
        print_state(node)

    if curr_box > NUM_BOXES or is_full(state):

        return node # terminal state / solution state
    
    # Generate child nodes
    next_box = curr_box + 1

    for child_state in generate_moves(state, curr_box):
        global TOTAL_NODES
        TOTAL_NODES += 1
        node['children'].append(build_graph(child_state, next_box, touches+1,TOTAL_NODES,node_num))
        
    return node

# Example usage
root = build_graph()

def count_nodes(node):
    """Count all nodes in the graph (Recursive)"""
    return 1 + sum(count_nodes(child) for child in node['children'])

print("Total nodes:", count_nodes(root))
