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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


'''
To solve this path, you'll want to construct your own traversal graph. You start in room 0, which contains exits ['n', 's', 'w', 'e']. Your starting graph should look something like this:

{
  0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
}
Try moving south and you will find yourself in room 5 which contains exits ['n', 's', 'e']. You can now fill in some entries in your graph:

{
  0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
  5: {'n': 0, 's': '?', 'e': '?'}
}

'''



def bfs(starting_vertex):
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
            for direction in visited_dirs[v]:
                if visited_dirs[v][direction] == "?":
                    # IF SO, RETURN THE PATH
                    traversal = []
                    for i in range(len(path)):
                        if path[i][1] != None:
                            traversal.append(path[i][1])
                    return traversal

            # Enqueue A PATH TO all it's neighbors
            for neighbor in visited_dirs[v]:
                # MAKE A COPY OF THE PATH
                path_copy = path.copy()

                # ENQUEUE THE COPY
                path_copy.append([visited_dirs[v][neighbor], neighbor])
                q.enqueue(path_copy)
    return False

'''
Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.
'''
def get_opposite_dir(dir):
    if dir == 'n':
        return 's'

    elif dir == 's':
        return 'n'
    
    elif dir == 'w':
        return 'e'

    elif dir == 'e':
        return 'w'

visited_dirs = {}


# make an adjacency dictionary with all possible directions
#iterate through all the rooms in the world
for room_id in world.rooms:

    # iterate through the exits in that room
    for exit_dir in world.rooms[room_id].get_exits():

        # if the room object hasnt been created yet
        if room_id not in  visited_dirs.keys():
            # create an dictionary for that room 
            visited_dirs[room_id] = dict()

        # asign a value of '?'  for each exit
        visited_dirs[room_id][exit_dir] = '?'
loop = True
while loop:
    room_id = player.current_room.id
    direction = None

    # choose a direction from current rooms exits
    for exit_dir in player.current_room.get_exits():
        if visited_dirs[room_id][exit_dir] == '?':
            direction = exit_dir
    if direction == None:
        # do a bfs searching for exit with '?'
        search = bfs(room_id)
        # if bfs returns a path 
        if search != False:
            # add path to the traversal_path
            traversal_path += search

            # walk that path and continue   
            for move in search:
                player.travel(move)
        else:
            loop = False

            # if bft dosent return anything break loop
    prev_room_id = player.current_room.id


    player.travel(direction)

    room_id = player.current_room.id

    #assign prev room the direction to current_room id
    visited_dirs[prev_room_id][direction] = room_id

    #assign current rooms id to oppisite direction from wich we traveled
    opposite_dir = get_opposite_dir(direction)
    visited_dirs[room_id][opposite_dir] = prev_room_id

    traversal_path.append(direction)




'''
You can find the path to the shortest unexplored room by using a breadth-first search for a room with a `'?'` for an exit. If you use the `bfs` code from the homework, you will need to make a few modifications.
'''




'''
1. Instead of searching for a target vertex, you are searching for an exit with a `'?'` as the value. If an exit has been explored, you can put it in your BFS queue like normal.

2. BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.

If all paths have been explored, you're done!

You know you are done when you have exactly 500 entries (0-499) in your graph and no `'?'` in the adjacency dictionaries. To do this, you will need to write a traversal algorithm that logs the path into `traversal_path` as it walks.
'''

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
