"""Dijkstra pathfinding implementation for maze grids."""

from collections import deque
from dataclasses import dataclass, field


@dataclass
class Node:
    pos: tuple[int, int]
    links: set['Node'] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.pos)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and self.pos == other.pos


class Dijkstra:
    """
    Implement Dijkstra's algorithm (uniform-cost BFS variant).

    Compute shortest paths in a maze by assigning distances
    from a root node and reconstructing paths to targets.
    """

    def __init__(self, root: Node | None) -> None:
        self.root: Node | None = root
        self.map: dict[Node, int] = {}

    def calculate(self) -> None:
        """Compute distances from the root to all reachable nodes."""
        start: Node | None = self.root
        if start:
            self.map.update({start: 0})

        frontier = deque([self.root])
        while frontier:
            node = frontier.popleft()
            if not node:
                raise ValueError
            new_nodes: set[Node] = self._explore(node)
            frontier += new_nodes

    def _explore(self, node: Node) -> set[Node]:
        """Explore neighbors and update distances."""
        current: int = self.map[node]
        new_nodes: set[Node] = set()

        for neighbor in node.links:
            if neighbor not in self.map:
                self.map[neighbor] = current + 1
                new_nodes.add(neighbor)

        return new_nodes

    def path_to_end(self, end: Node | None) -> list[Node]:
        """Reconstruct the shortest path from root to end."""
        if not end or end not in self.map:
            return []

        path: list[Node] = [end]
        current: Node = end

        while current is not self.root:
            next_node = None
            for neighbor in current.links:
                if self.map.get(neighbor) == self.map[current] - 1:
                    next_node = neighbor
                    break

            if next_node is None:
                break

            current = next_node
            path.append(current)

        path.reverse()
        return path

    @staticmethod
    def make_path(start: Node | None, end: Node | None) -> list[Node] | None:
        """Compute a shortest path between two nodes."""
        if start and end:
            dijkstra = Dijkstra(start)
            dijkstra.calculate()
            return dijkstra.path_to_end(end)
        return None
