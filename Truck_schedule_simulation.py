"""Truck_schedule_simulation.py
This one simulates the post-load plan part - the Truck schedule.
If a Box CAN go out to a truck, it does so immediately.
"""

import random
from itertools import product
from config import VERBOSE, NUM_BOXES, WIDTH, HEIGHT, TOTAL_BOXES, LOAD_PLAN
from copy import deepcopy
import Load_plan_simulation

# initialization of vals.
BOX_SCHEDULE = random.shuffle(list(range(1,NUM_BOXES)))
TOTAL_NODES = 0
EMPTY_BOX = (0,0,0)
TOTAL_SOLUTION_STATES = 0

INPUT_LOAD = list(range(1,NUM_BOXES))

def print_state(node):
    print("TRUCK SCHEDULE: State:")
    print(f"Touches so far: {node['touches']}")
    print(f"Parent Node: {node['parent node']}")
    print(f"Node: {node['current node']}")
    yard = node['state']['yard']
    print("Box format (Box #, weight, priority)")
    print("yard:")
    for row in range(HEIGHT - 1, -1, -1):
        for col in range(WIDTH):
            index = row*WIDTH+col
            box = yard[index]
            print(f"| {(str(box[0]) + ',' + str(box[1]) + ','+str(box[2])) if box != EMPTY_BOX else '     ' } |", end="")
        print("", end="\n")
    print("\n-------------------------------------------\n")
    return

def is_empty(yard):
    return all(box == EMPTY_BOX for box in yard)

def drop_box(yard, column, box):
    """Drop a box into the column, Connect-4 style"""
    # Check if the column is valid
    if column < 0 or column >= WIDTH:
        raise ValueError("Invalid column index.")
    # Traverse the column from bottom to top
    box_weight = box[1]
    prev_weight = float('inf') # begins @ infinity
    for row in range(0, HEIGHT):
        index = row * WIDTH + column
        
        stacked_box = yard[index]
        if stacked_box == EMPTY_BOX:  # cell is empty
            if box_weight <= prev_weight:
                yard[index] = box
                return yard  # Successfully dropped the box
            else:
                return None
        else:
            prev_weight = stacked_box[1]
    return None # no empty cells.
        
def top_box(yard, col):
    """ Returns the index of the top box of a column.
    Returns -1 iff column is empty.
    """
    print(f"given col: {col}")
    for row in range(HEIGHT-1, -1, -1):
        # index of potentially blocking box
        index = row * WIDTH + col
        if yard[index] != EMPTY_BOX:
            return index
    return -1

def generate_moves(node):
    """Generate all possible states after the next move
    """
    state = node['state']
    child_states = []
    next_box_indexes = []
    yard = state['yard']
    # find lowest priority -- next box to go out
    min_priority_index = min((i for i, x in enumerate(yard) if x != EMPTY_BOX), key=lambda i: yard[i][2])
    curr_row = min_priority_index % WIDTH
    curr_col = min_priority_index - curr_row*WIDTH
    top_index = top_box(yard, curr_col)
    if top_index == min_priority_index: # Box is free.
        # pop the box and move onto the next.
        child_state = {
            'yard':deepcopy(yard),
        }
        child_state['yard'][min_priority_index] = EMPTY_BOX
        child_states.append(child_state)
    else:
        for i in range(1):
            # leaving room to allow for other movements.
            next_box_indexes.append(top_index)
        print(f"top index = {top_index}")
        for i in range(WIDTH):
            row = i % WIDTH
            col = i - row*WIDTH
            if col == curr_col: # cant move box to same column.
                continue
            child_state = {
                'yard':deepcopy(yard),
            }
            index_next_box = next_box_indexes[0]
            next_box = child_state['yard'][index_next_box]
            child_state['yard'][index_next_box] = EMPTY_BOX
            child_state['yard'] = drop_box(child_state['yard'],i,next_box)
            
            print(f"next box index- {index_next_box}")
            print(f"next box itself - {next_box}")
            print(f"next yard - {child_state['yard']}")
            if child_state['yard'] == None:
                continue
            else:
                child_states.append(child_state)
    print(child_states)
    return child_states

def build_graph(node):
    """Recursively build a graph of all possible box movements/shipments"""
    # Create a node for the current state
    if VERBOSE:
        print_state(node)
    state = node['state']

    if is_empty(state['yard']):
        global TOTAL_SOLUTION_STATES
        TOTAL_SOLUTION_STATES += 1
        print("asdf")
        return node # terminal state / solution state

    for child_state in generate_moves(node):
        global TOTAL_NODES
        TOTAL_NODES += 1
        child_node = {
            'state': child_state,
            'parent node': node['current node'],
            'current node': TOTAL_NODES,
            'touches': node['touches']+1,
            'solution state': False,
            'children': []
        }
        
        # TODO: Better not to be recursive (BFS has big benefits -- can know that the first time you see a specific hash state is one of the optimal ways to reach it.) but eh for now
        node['children'].append(build_graph(child_node))
        
    return node

# usage
root = Load_plan_simulation.build_graph()

def count_nodes(node):
    """Count all nodes in the graph (Recursive)"""
    return 1 + sum(count_nodes(child) for child in node['children'])

print("Total nodes:", count_nodes(root))
print("Total solution states:", TOTAL_SOLUTION_STATES)
print("BEGINNING TRUCK SCHEDULE\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def get_solution_space(node):
    # recursively find the solution space.
    # solution space of the load plan simulation.
    
    if node['solution state']:
        return [node]

    # recursion -- inefficient but easy to code for now
    leaves = []
    for child in node['children']:
        leaves.extend(get_solution_space(child))
    
    return leaves

solution_space = get_solution_space(root)

# print(solution_space[0])
build_graph(solution_space[0])
