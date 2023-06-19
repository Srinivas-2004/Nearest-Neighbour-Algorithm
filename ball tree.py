import numpy as np

class BallTreeNode:
    def __init__(self, center, radius, left_child=None, right_child=None, points=None):
        self.center = center
        self.radius = radius
        self.left_child = left_child
        self.right_child = right_child
        self.points = points

class BallTree:
    def __init__(self):
        self.root = None

    def insert(self, point):
        if self.root is None:
            self.root = BallTreeNode(point, 0)
        else:
            self._insert_recursive(self.root, point)

    def _insert_recursive(self, node, point):
        if node.points is not None:
            node.points = np.vstack((node.points, point))
            radius = np.max(np.linalg.norm(node.points - node.center, axis=1))
            node.radius = radius
        else:
            distance = np.linalg.norm(point - node.center)
            if distance <= node.radius:
                if node.left_child is None:
                    node.left_child = BallTreeNode(point, 0)
                else:
                    self._insert_recursive(node.left_child, point)
            else:
                if node.right_child is None:
                    node.right_child = BallTreeNode(point, 0)
                else:
                    self._insert_recursive(node.right_child, point)

    def find_nearest_neighbor(self, query_point):
        if self.root is None:
            return None

        best_point, best_distance = self._find_nearest_neighbor_recursive(self.root, query_point, None, np.inf)
        return best_point

    def _find_nearest_neighbor_recursive(self, node, query_point, best_point, best_distance):
        distance = np.linalg.norm(query_point - node.center)

        if distance < best_distance:
            best_distance = distance
            best_point = node.center

        if node.left_child is not None and node.right_child is not None:
            if distance <= node.radius:
                best_point, best_distance = self._find_nearest_neighbor_recursive(node.left_child, query_point, best_point, best_distance)
            else:
                best_point, best_distance = self._find_nearest_neighbor_recursive(node.right_child, query_point, best_point, best_distance)

            if distance - best_distance <= node.radius:
                if distance <= node.radius:
                    best_point, best_distance = self._find_nearest_neighbor_recursive(node.right_child, query_point, best_point, best_distance)
                else:
                    best_point, best_distance = self._find_nearest_neighbor_recursive(node.left_child, query_point, best_point, best_distance)

        elif node.left_child is not None:
            best_point, best_distance = self._find_nearest_neighbor_recursive(node.left_child, query_point, best_point, best_distance)

        elif node.right_child is not None:
            best_point, best_distance = self._find_nearest_neighbor_recursive(node.right_child, query_point, best_point, best_distance)

        return best_point, best_distance


tree = BallTree()
data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
print(data)
for point in data:
    tree.insert(point)

query_point = np.array([2, 3])
nearest_neighbor = tree.find_nearest_neighbor(query_point)

print("Query Point:", query_point)
print("Nearest Neighbor:", nearest_neighbor)