#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File name: coding.py
# Author: Meen Kim
# Date created: 11/11/2017
# Python version: 3.6.1
# Approaches:
# flatten_list: recursion
# serialize_tree: level-order traversal


class Node(object):
	def __init__(self, val):
		self.val = val
		self.left = self.right = None

class Solution(object):
	def flatten_list(self, nested_list):
		'''
		Flatten an arbitrarily nested list

		Params:
			nested_list: A nested list of int

		Returns:
			flat_list: A flattened list with only int
		'''
		flat_list = []

		for i in nested_list:
			if isinstance(i, list):
				for j in self.flatten_list(i):
					flat_list.append(j)
			else:
				flat_list.append(i)

		return flat_list

	def serialize_tree(self, root_node):
		'''
		Serialize a binary tree to a list of int and/or None

		Params:
			root_node: A root node object of binary tree

		Returns:
			serial_tree :  A list of serialized values
		'''
		if not root_node: return

		serial_tree = []
		queue = [root_node]

		while queue:
			node = queue.pop(0)
			if node:
				serial_tree.append(node.val)
				queue.append(node.left)
				queue.append(node.right)
			else:
				serial_tree.append(None)

		return serial_tree


	def deserialize_tree(self, data):
		'''
		Deserializes a list of int and/or None to a binary tree

		Params:
			data: A list of serialized values

		Returns:
			deserial_tree : A root node object of binary tree
		'''
		if not data: return

		root_node = Node(data[0])
		queue = [root_node]

		i = 1
		while queue and i < len(data):
			node = queue.pop(0)

			if not node: continue

			val = data[i]
			node.left = Node(val) if val else None
			queue.append(node.left)
			i += 1

			val = data[i]
			node.right = Node(val) if val else None
			queue.append(node.right)
			i += 1

		return root_node


if __name__ == '__main__':
	# Instatiate solution
	solution = Solution()

	# Test flatten_list
	print('==Test flatten_list==')

	test_cases = [
		[2, [[3, [4]], 5]],
		[1, 2, [3, 4, [5],[6]], [7, [[[8, 9]]]]]
	]

	for i, test_case in enumerate(test_cases):
		print('Test case {i}: {t}'.format(i=i, t=test_case))
		result = solution.flatten_list(test_case)
		print('Test result {i}: {r}'.format(i=i, r=result))

	# Test serialize_tree
	print('\n==Test serialize_tree==')

	test_case = [1, 2, 3, None, 4, 2, None]
	print('Test case: {t}'.format(t=test_case))

	root_node = solution.deserialize_tree(test_case)
	serial_tree= solution.serialize_tree(root_node)

	print('Test result {r}'.format(r=serial_tree))
