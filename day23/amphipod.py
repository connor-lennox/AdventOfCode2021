from os import defpath
import sys
from collections import namedtuple
from typing import List


# Define consts and costs
EMPTY = 0
A = 1
B = 10
C = 100
D = 1000

ROOM_DEPTH = 2
NUM_ROOMS = 4
HALL_LEN = 11

# Quick conversion for input reading
charmap = {'A': A, 'B': B, 'C': C, 'D': D}
roommap = {A: 0, B: 1, C: 2, D: 3}
reverse_roommap = {0: A, 1: B, 2: C, 3: D}
roomopenings = {A: 2, B: 4, C: 6, D: 8}

moveout_positions = [0, 1, 3, 5, 7, 9, 10]


State = namedtuple("State", "hallway rooms cost")


# The hallway is the stretch along the top:
start_hallway = [EMPTY] * HALL_LEN

# Rooms along hallway. At end, should be [[AA][BB][CC][DD]]
start_rooms = [[EMPTY, EMPTY] for _ in range(NUM_ROOMS)]
complete_rooms = [[A, A], [B, B], [C, C], [D, D]]

with open(sys.argv[1]) as infile:
    room_line = 0
    for line in infile:
        pods = ''.join((filter(lambda x: x in ['A','B','C','D'], line)))
        if len(pods) > 0:
            for i, c in enumerate(pods):
                start_rooms[i][room_line] = charmap[c]
            room_line += 1


start_state = State(start_hallway, start_rooms, 0)


def to_record(state):
    return tuple([tuple(state.hallway), tuple([tuple(room) for room in state.rooms])])


def hallway_path(hallway, p1, p2)->bool:
    # Returns if a path is possible down the hallway between p1 and p2
    # Swap if needed for proper slicing
    if p1 > p2:
        p1, p2 = p2, p1
    return sum(hallway[p1:p2+1]) == 0


def can_move_into_room(position: int, hallway, rooms)->bool:
    # Tell if a pod at given position can move into its target room.
    # The room must have no incorrect pods in it, and the path must be clear.
    
    # Find the pod value and target room
    pod = hallway[position]
    target_room = roommap[pod]

    # If the room is able to be moved into
    room_open = all(slot == EMPTY or slot == pod for slot in rooms[target_room])

    # Find deepest position to move in to
    movein_depth = ROOM_DEPTH-1
    while(rooms[target_room][movein_depth] != EMPTY and movein_depth > 0): movein_depth -= 1
    
    # If the path from pod to room is open
    target_pos = roomopenings[pod]
    path_open = hallway_path(hallway, position + (1 if position < target_pos else -1), target_pos)

    # Cost to move * pod value
    cost = (abs(roomopenings[pod] - position) + (movein_depth+1)) * pod

    return room_open and path_open, cost, movein_depth


def expand(state: State)->List[State]:
    # Expand a state into all possible futures
    new_states = []
    # Start with moving things out of the hallway into their target room
    for i, pod in enumerate(state.hallway):
        if pod != EMPTY:
            room_available, cost, depth = can_move_into_room(i, state.hallway, state.rooms)
            if room_available:
                # If we can move into the room, we'll always want to.
                # There is no benefit to leaving a pod in the hallway.
                new_hallway = [state.hallway[j] if i != j else EMPTY for j in range(len(state.hallway))]
                new_rooms = [[state.rooms[n][d] if (n != roommap[pod] or d != depth) else pod for d in range(ROOM_DEPTH)] for n in range(NUM_ROOMS)]
                new_cost = state.cost + cost
                new_states.append(State(new_hallway, new_rooms, new_cost))
                
                # Early return: we only want to make this single move!
                return new_states

    # Now we can move from rooms into the hallway
    for i, room in enumerate(state.rooms):
        opening = (i+1) * 2
        room_complete = room == complete_rooms[i]
        if not room_complete:
            for depth, slot in enumerate(room):
                moving_pod = slot
                moved = False
                if slot != EMPTY and (not all([r == reverse_roommap[i] for r in room[depth:]])):
                    for outpos in moveout_positions:
                        if hallway_path(state.hallway, opening, outpos):
                            new_hallway = [state.hallway[j] if outpos != j else moving_pod for j in range(HALL_LEN)]
                            new_rooms = [[state.rooms[n][d] if (n != i or d != depth) else EMPTY for d in range(ROOM_DEPTH)] for n in range(NUM_ROOMS)]
                            new_cost = state.cost + ((depth + 1) + abs(outpos-opening)) * moving_pod
                            new_states.append(State(new_hallway, new_rooms, new_cost))
                            moved = True

                    if moved:
                        break

    return new_states


# Open list and closed set
open_list = [start_state]

closed = {}
closed[to_record(start_state)] = 0

state_sort = lambda s: s.cost

# Part 1
while(len(open_list) > 0):
    # Pop minimum cost state
    cur = open_list[0]
    open_list = open_list[1:]

    # Are we done?
    if cur.rooms == complete_rooms:
        print(f"Part 1: Min Cost = {cur.cost}")
        break

    # Expand, extend, sort
    for state in expand(cur):
        record = to_record(state)
        if record not in closed or closed[record] > state.cost:
            closed[record] = state.cost
            open_list.append(state)

    open_list.sort(key=state_sort)
