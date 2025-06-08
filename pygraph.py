from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple, Iterable, Union

Node = Union[str, int]
Edge = Tuple[Node, Node]

class Graph:
    """Graph data structure, undirected by default."""
    
    def __init__(self, edges: Iterable[Edge] = [], directed: bool = False):
        self.adjacency_list: Dict[Node, List[Node]] = {}
        self.directed = directed
        
        for node1, node2 in edges:
            self.add_edge((node1, node2))

    def has_node(self, node: Node):
        """Whether a node is in graph"""
        return node in self.adjacency_list

    def has_edge(self, edge: Edge):
        """Whether an edge is in graph"""
        node1, node2 = edge
        return (node1 in self.adjacency_list and 
                node2 in self.adjacency_list and 
                node2 in self.adjacency_list[node1])

    def add_node(self, node: Node):
        """Add a node"""
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, edge: Edge):
        """Add an edge (node1, node2). For directed graph, node1 -> node2"""
        node1, node2 = edge
        self.add_node(node1)
        self.add_node(node2)
        
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        
        if not self.directed and node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)

    def remove_node(self, node: Node):
        """Remove all references to node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not in graph")
            
        # Remove node from all adjacency lists
        for _, neighbors in self.adjacency_list.items():
            if node in neighbors:
                neighbors.remove(node)
        
        # Remove the node itself
        del self.adjacency_list[node]

    def remove_edge(self, edge: Edge):
        """Remove an edge from graph"""
        node1, node2 = edge
        if (node1 not in self.adjacency_list or 
            node2 not in self.adjacency_list or
            node2 not in self.adjacency_list[node1]):
            raise ValueError(f"Edge {edge} not in graph")
        
        self.adjacency_list[node1].remove(node2)
        
        if not self.directed and node1 in self.adjacency_list[node2]:
            self.adjacency_list[node2].remove(node1)

    def indegree(self, node: Node) -> int:
        """Compute indegree for a node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not in graph")
            
        count = 0
        for _, neighbors in self.adjacency_list.items():
            if node in neighbors:
                count += 1
        return count

    def outdegree(self, node: Node) -> int:
        """Compute outdegree for a node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not in graph")
            
        return len(self.adjacency_list[node])
    
    def get_neighbors(self, node: Node) -> List[Node]:
        """Get neighbors of a node"""
        if node not in self.adjacency_list:
            raise ValueError(f"Node {node} not in graph")
        return self.adjacency_list.get(node, [])
    
    def depth_first_search(self, start: Node) -> List[Node]:
        """Depth-first search"""
        if start not in self.adjacency_list:
            raise ValueError(f"Node {start} not in graph")
            
        visited = []
        stack = [start]
        
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.append(current)
                for neighbor in reversed(self.adjacency_list.get(current, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited
    
    def breadth_first_search(self, start: Node) -> List[Node]:
        """Breadth-first search"""
        if start not in self.adjacency_list:
            raise ValueError(f"Node {start} not in graph")
            
        visited = []
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.append(current)
                for neighbor in self.adjacency_list.get(current, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        return visited
    
    def find_shortest_path(self, start: Node, end: Node) -> Optional[List[Node]]:
        """Find shortest path using BFS"""
        if start not in self.adjacency_list or end not in self.adjacency_list:
            raise ValueError("Start or end node not in graph")
            
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            if current == end:
                return path
                
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

    def __str__(self):
        """String representation of the graph"""
        return "\n".join(
            f"{node}: {', '.join(map(str, neighbors))}" 
            for node, neighbors in sorted(self.adjacency_list.items())
        )

    def __repr__(self):
        return f"Graph(adjacency_list={self.adjacency_list}, directed={self.directed})"