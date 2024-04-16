import logging
from typing import List, Optional


# Assuming a NodeBase class exists that has the following methods and attributes:
# - F, G, H properties (floats)
# - Walkable (bool)
# - Neighbors (list of NodeBase)
# - Connection (NodeBase)
# - SetColor(color: tuple), where color is an RGB tuple
# - GetDistance(other: NodeBase) -> float
# - SetG(g: float)
# - SetConnection(node: NodeBase)

class Pathfinding:
    PathColor = (0.65, 0.35, 0.35)
    OpenColor = (0.4, 0.6, 0.4)
    ClosedColor = (0.35, 0.4, 0.5)

    @staticmethod
    def find_path(start_node: 'NodeBase', target_node: 'NodeBase') -> Optional[List['NodeBase']]:
        to_search = [start_node]
        processed = []

        while to_search:
            current = to_search[0]
            for t in to_search:
                if t.F < current.F or (t.F == current.F and t.H < current.H):
                    current = t

            processed.append(current)
            to_search.remove(current)

            current.set_color(Pathfinding.ClosedColor)

            if current == target_node:
                current_path_tile = target_node
                path = []
                count = 100
                while current_path_tile != start_node:
                    path.append(current_path_tile)
                    current_path_tile = current_path_tile.Connection
                    count -= 1
                    if count < 0:
                        raise Exception("Loop detected or excessive path length")
                    logging.info("Debug path information")

                for tile in path:
                    tile.set_color(Pathfinding.PathColor)
                start_node.set_color(Pathfinding.PathColor)
                logging.info(f"Path length: {len(path)}")
                return path

            for neighbor in [n for n in current.Neighbors if n.Walkable and n not in processed]:
                in_search = neighbor in to_search
                cost_to_neighbor = current.G + current.get_distance(neighbor)

                if not in_search or cost_to_neighbor < neighbor.G:
                    neighbor.SetG(cost_to_neighbor)
                    neighbor.SetConnection(current)

                    if not in_search:
                        neighbor.SetH(neighbor.get_distance(target_node))
                        to_search.append(neighbor)
                        neighbor.set_color(Pathfinding.OpenColor)
        return None


# Configure logging
logging.basicConfig(level=logging.INFO)
