from room import Room
from player import Player
from world import World

from util import Stack, Queue  # These may come in handy


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def adv_bfs(starting_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    # Create a queue
    q = Queue()

    # Enqueue A PATH TO the starting vertex
    q.enqueue([[starting_vertex, None]])

    # Create a set to store visited vertices
    visited = set()

    # While the queue is not empty...
    while q.size() > 0:
        # Dequeue the first PATH
        path = q.dequeue()
        # GRAB THE VERTEX FROM THE END OF THE PATH
        v = path[-1][0]

        # Check if it's been visited
        # If it hasn't been visited...
        if v not in visited:
            # Mark it as visited
            visited.add(v)

            # CHECK all directions for '?'
            for direction in adjacency_dict[v]:

                # if a '?' is found
                if adjacency_dict[v][direction] == "?":
                    # IF SO, RETURN THE A TRAVERSAL TO THAT ROOM
                    traversal = []

                    for i in range(len(path)):

                        #TODO CLEANUP 
                        if path[i][1] is not None:
                            traversal.append(path[i][1])
                    return traversal

            # Enqueue A PATH TO all it's neighbors
            for neighbor in adjacency_dict[v]:
                # MAKE A COPY OF THE PATH
                path_copy = path.copy()

                # ENQUEUE THE COPY
                path_copy.append([adjacency_dict[v][neighbor], neighbor])
                q.enqueue(path_copy)
    return False
#make a function that takes in a dir and returns the oppisite direction
def get_opposite_dir(dir):
    if dir == 'n':
        return 's'

    elif dir == 's':
        return 'n'
    
    elif dir == 'w':
        return 'e'

    elif dir == 'e':
        return 'w'



# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

adjacency_dict = {}

# make an adjacency dictionary with all possible directions
#iterate through all the rooms in the world
for room_id in world.rooms:

    # iterate through the exits in that room
    for exit_dir in world.rooms[room_id].get_exits():

        # if the room object hasnt been created yet
        if room_id not in  adjacency_dict.keys():
            # create an dictionary for that room 
            adjacency_dict[room_id] = dict()

        # asign a value of '?'  for each exit
        adjacency_dict[room_id][exit_dir] = '?'


while True:
    room_id = player.current_room.id
    direction = None

    # choose a direction from current rooms exits
    for exit_dir in player.current_room.get_exits():
        if adjacency_dict[room_id][exit_dir] == '?':
            direction = exit_dir

    # if no unexplored direction 
    if direction == None:
        # do a adv_bfs searching for exit with '?'
        search = adv_bfs(room_id)

        # if adv_bfs returns a path 
        if search != False:
            # add path to the traversal_path
            traversal_path += search

            # walk that path and continue   
            for move in search:
                player.travel(move)

        # if adv_bfs  returns false
        else:
            break

    #otherwise travel in selected direction and mark rooms in adjacency_dict
    else:        
        prev_room_id = player.current_room.id


        player.travel(direction)

        room_id = player.current_room.id

        #assign prev room the direction to current_room id
        adjacency_dict[prev_room_id][direction] = room_id

        #assign current rooms id to oppisite direction from wich we traveled
        opposite_dir = get_opposite_dir(direction)
        adjacency_dict[room_id][opposite_dir] = prev_room_id

        traversal_path.append(direction)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
