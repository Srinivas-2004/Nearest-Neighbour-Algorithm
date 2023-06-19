# Number of dimensions
k = 2


class Node:
	def __init__(self, point):
		self.point = point
		self.left = None
		self.right = None


def newNode(point):
	return Node(point)

def insertRec(root, point, depth):

	if not root:
		return newNode(point)


	cd = depth % k

	if point[cd] < root.point[cd]:
		root.left = insertRec(root.left, point, depth + 1)
	else:
		root.right = insertRec(root.right, point, depth + 1)

	return root


def insert(root, point):
	return insertRec(root, point, 0)

def arePointsSame(point1, point2):

	for i in range(k):
		if point1[i] != point2[i]:
			return False

	return True

def searchRec(root, point, depth):

	if not root:
		return False
	if arePointsSame(root.point, point):
		return True

	cd = depth % k

	if point[cd] < root.point[cd]:
		return searchRec(root.left, point, depth + 1)

	return searchRec(root.right, point, depth + 1)

def search(root, point):
	
	return searchRec(root, point, 0)


if __name__ == '__main__':
	root = None
	points = [[3, 6], [17, 15], [13, 15], [6, 12], [9, 1], [2, 7], [10, 19]]

	n = len(points)

	for i in range(n):
		root = insert(root, points[i])

	point1 = [10, 19]
	if search(root, point1):
		print("Found")
	else:
		print("Not Found")

	point2 = [12, 19]
	if search(root, point2):
		print("Found")
	else:
		print("Not Found")
		