class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()
        pass  # TODO

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        pass  # TODO
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print("error: Error vertex does not exsist")
    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise ValueError("vertex does not exist")

def earliest_ancestor(ancestors, starting_node):
    #create a graph 
    g = Graph()

    #for each tuple in ancestors
    for pair in ancestors:
        # add each pair to vertices
        if pair[0] not in g.vertices:
            g.add_vertex(pair[0])

        if pair[1] not in g.vertices:
            g.add_vertex(pair[1])

        #add edge in reverse so that the traversal goes up to earlier ancestors
        g.add_edge(pair[1], pair[0])
    #do the traversal

    # create a queue
    q = Queue()

    # enqueue starting node path
    q.enqueue( [starting_node] )

    #no need to make a visited set since acyclic

    # create vars to store the oldest ancestor and the length of the path
    oldest_ancestor = -1
    longest_path = 1
    # while queue is not empty
    while q.size() > 0:
        #dequeue path
        path = q.dequeue()

        # get last ancestor from path
        v = path[-1]

        # if the ancestor is less than the oldest_ancestor and the path is more than or equal to the longest path
        if (v < oldest_ancestor and len(path) <= longest_path) or len(path) > longest_path:
            oldest_ancestor = v
            longest_path = len(path)

        # enqueue neightbors
        for neighbor in g.get_neighbors(v):
            path_copy = path.copy()
            path_copy.append(neighbor)
            q.enqueue(path_copy)
    return oldest_ancestor


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 9))
