"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

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

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        #Create a queue
        q = Queue()
        #Enqueue the startijng vertex
        q.enqueue(starting_vertex)
        #Create a set to store visited vertices
        visited = set()
        #While the queue is not empty...
        while q.size() > 0:
            #Dequeue vertex
            v = q.dequeue()
            #Check if in visited
            #if not visited
            if v not in visited:
                #mark as visited 
                print(v)
                visited.add(v)
                #enqueue all neighbors
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        #Create stack
        s = Stack()
        #Push the starting vertex
        s.push(starting_vertex)
        #Create a set to store visited vertices
        visited = set()
        #While the stack is not empty...
        while s.size() > 0:
            #Pop vertext
            v = s.pop()

            #Check if in visited
            #if not visited
            if v not in visited:
                #mark as visited 
                print(v)
                visited.add(v)
                
                #Push all neighbors
                for neighbour in self.get_neighbors(v):

                    s.push(neighbour)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """

        if visited == None:
            visited = set()

        if starting_vertex not in visited:
            visited.add(starting_vertex)
            print(starting_vertex)
            for neighbour in self.get_neighbors(starting_vertex):
                self.dft_recursive(neighbour, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create a queue
        q = Queue()

        # Enqueue A PATH TO the starting vertex
        q.enqueue([starting_vertex])

        # Create a set to store visited vertices
        visited = set()

        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            v = path[-1]

            # Check if it's been visited
            # If it hasn't been visited...
            if v not in visited:
                # Mark it as visited
                visited.add(v)

                # CHECK IF IT'S THE TARGET
                if v == destination_vertex:
                    # IF SO, RETURN THE PATH
                    return path

                # Enqueue A PATH TO all it's neighbors
                for neighbor in self.get_neighbors(v):
                    # MAKE A COPY OF THE PATH
                    path_copy = path.copy()

                    # ENQUEUE THE COPY
                    path_copy.append(neighbor)
                    q.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        #Make a stack
        s = Stack()

        #Push path to  starting vertex onto stack
        s.push([starting_vertex])

        #Make a set to store visisted vertices
        visited = set()

        #while stack is not empty
        while s.size() > 0:
            #Pop path off of stack
            path = s.pop()

            #get Vertex from last item in path
            v = path[-1]

            #check if vertex is in visited
            if v not in visited:
                #if it is not in visited add it
                visited.add(v)

                #if vertex is the destination
                if v == destination_vertex:
                    #return path
                    return path
                

                #push all the paths to neighbor vertices to stack
                for neighbor in self.get_neighbors(v):
                    #make a copy of path
                    path_copy = path.copy()

                    #add neighbor to path copy
                    path_copy.append(neighbor)

                    # push path copy to stack
                    s.push(path_copy)
                    



    def dfs_recursive(self, starting_vertex, desitination_vertex, visisted=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visisted == None:
            visisted = set()

        if path == None:
            path = []

        # Check if the node has been visited
        # If not...
        if starting_vertex not in visisted:

            # add vertex to path 
            path_copy = path.copy()
            path_copy.append(starting_vertex)

            # Mark it as visited
            visisted.add(starting_vertex)

            #if its the destination return path
            if starting_vertex == desitination_vertex:
                return path_copy

            # Call dfs_recursive on each neighbor
            for neighbor in self.get_neighbors(starting_vertex):
                #store the return in a var
                stored_path = self.dfs_recursive(neighbor, desitination_vertex, visisted, path_copy)

                if stored_path is not None:
                    return stored_path




if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    # print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
