# PortToyModel
## Purpose:
    - Producing a State-space representation of the problem space
## Program specific Choices:
    - Boxes are labelled 1,2...N
    - Truck schedule is randomized
    - State is currently represented as a 1D string
    - Use config.py to change variables
        > Use "VERBOSE" to choose whether to print problem space
    - Boxes are a tuple - (Box #, Weight, Priority)
        > Box # is just a box identifier (Currently not doing much)
        > Box weight is the weight of the box -- boxes may only go ontop of heavier boxes.
        > Box priority is the placement of hte box in the Truck schedule (order that the boxes must go out.)
            - lower numbers represent a higher priority 
## Usage:
### Linux/unix:
    Run with ```python3 ./Truck_schedule_simulation.py > output.txt``` (Pipes output to output.txt)
### Windows: 
    Run with ```python ./Truck_schedule_simulation.py > output.txt``` (Pipes output to output.txt)
