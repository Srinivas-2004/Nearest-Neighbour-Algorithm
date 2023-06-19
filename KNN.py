import heapq
import math

class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right


class KDTree:
    def __init__(self, points):
        self.root = self.build_kdtree(points)

    def build_kdtree(self, points, depth=0):
        if not points:
            return None

        k = len(points[0])
        axis = depth % k

        sorted_points = sorted(points, key=lambda point: point[axis])
        median = len(sorted_points) // 2

        return Node(
            sorted_points[median],
            self.build_kdtree(sorted_points[:median], depth + 1),
            self.build_kdtree(sorted_points[median + 1:], depth + 1))

    def distance(self, point1, point2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

    def knn_search(self, query_point, k):
        heap = []
        self.knn_search_recursive(self.root, query_point, k, heap)
        return [(-dist, point) for dist, point in heap]

    def knn_search_recursive(self, node, query_point, k, heap, depth=0):
        if node is None:
            return

        dist = self.distance(query_point, node.point)
        heapq.heappush(heap, (dist, node.point))
        if len(heap) > k:
            heapq.heappop(heap)

        kth_largest = heap[0][0]

        axis = depth % len(query_point)
        if query_point[axis] < node.point[axis]:
            self.knn_search_recursive(node.left, query_point, k, heap, depth + 1)
            if node.point[axis] - query_point[axis] <= kth_largest:
                self.knn_search_recursive(node.right, query_point, k, heap, depth + 1)
        else:
            self.knn_search_recursive(node.right, query_point, k, heap, depth + 1)
            if query_point[axis] - node.point[axis] <= kth_largest:
                self.knn_search_recursive(node.left, query_point, k, heap, depth + 1)


# Example usage
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
kdtree = KDTree(points)
query_point = (6, 5)
k = 3

knn_results = kdtree.knn_search(query_point, k)
print("K Nearest Neighbors:")
for dist, point in knn_results:
    print("Point:", point, "Distance:", -dist)
