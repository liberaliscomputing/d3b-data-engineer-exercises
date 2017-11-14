# D3b Data Engineer Exercises

```python
# Author: Meen Kim
# Date submitted: 11/11/2017
# Python version: 3.6.1
```

## Coding Section ([Link to Code](https://github.com/liberaliscomputing/d3b-data-engineer-exercises/blob/master/coding.py))

### Coding Exercise 1: Flatten Nested List (Recursion)

```python
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

		# Prints 
		# ==Test flatten_list==
		# Test case 0: [2, [[3, [4]], 5]]
		# Test result 0: [2, 3, 4, 5]
		# Test case 1: [1, 2, [3, 4, [5], [6]], [7, [[[8, 9]]]]]
		# Test result 1: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```


### Coding Exercise 2: Serialize a Binary Tree (Level-order Traversal)

```python
class Node(object):
	def __init__(self, val):
		self.val = val
		self.left = self.right = None

class Solution(object):
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

	# Test serialize_tree
	print('\n==Test serialize_tree==')

	test_case = [1, 2, 3, None, 4, 2, None]
	print('Test case: {t}'.format(t=test_case))

	root_node = solution.deserialize_tree(test_case)
	serial_tree= solution.serialize_tree(root_node)

	print('Test result {r}'.format(r=serial_tree))

	# Prints
	# ==Test serialize_tree==
	# Test case: [1, 2, 3, None, 4, 2, None]
	# Test result: [1, 2, 3, None, 4, 2, None]
```

## Data Section ([Link to Code](https://github.com/liberaliscomputing/d3b-data-engineer-exercises/blob/master/data.py))

```python
import sqlite3, time


dname = 'data'
fname = 'openmrs.db'

con = sqlite3.connect('/'.join([dname, fname]))
with con:
	cur = con.cursor()
```

### Data Exercise 1

Provide a list of male patients in the database.

```python
	query = 'SELECT * FROM patient WHERE gender = \'M\';'
	cur.execute(query);
	male_patients = cur.fetchall()
	print(male_patients)
	
	# Prints [('M', 'MRN000002', 2, '1941-05-01', 0), ('M', 'MRN000006', 6, '1962-04-21', 0), ... ]
```

Provide the counts of patients by gender.

```python    
	query = 'SELECT gender, COUNT(*) FROM patient GROUP BY gender;'
	cur.execute(query);
	gender_counts = cur.fetchall()
	print(gender_counts)

	# Prints [('', 1), ('F', 3484), ('M', 1800)]
```

### Data Exercise 2

Count patients in the database diagnosed with DERMATITIS at an encounter.

```python
	query = [
		'SELECT DISTINCT e.patient_id', 
		'FROM encounter AS e',
		'INNER JOIN encounter_diagnosis AS ed',
		'ON e.id = ed.encounter_id',
		'INNER JOIN diagnosis AS d',
		'ON ed.diagnosis_id = d.id',
		'WHERE d.name = \'DERMATITIS\';'
	]
	cur.execute(' '.join(query))
	patient_ids = cur.fetchall()
	print(len(patient_ids)) 

	# Prints 131
```

### Data Exercise 3

Provide a list patients, by MRN, who have had a CD4 count of less than 300.

```python
	query = [
		'SELECT DISTINCT p.mrn', 
		'FROM patient AS p',
		'INNER JOIN encounter AS e',
		'ON p.id = e.patient_id',
		'INNER JOIN lab_result AS l',
		'ON e.id = l.encounter_id',
		'WHERE l.cd4 < 300;'
	]
	cur.execute(' '.join(query))
	patient_mrns = cur.fetchall()
	print(patient_mrns)

	# Prints [('MRN003396',), ('MRN000574',), ('MRN003353',), ... ]
```

### Data Exercise 4

Count all female patients above the age of 30 in the database as of today’s date

```python
	query = 'SELECT birthdate FROM patient WHERE gender = \'F\';'
	cur.execute(query);
	birthdates = cur.fetchall()

	now = time.time()
	def is_above_thirty(birthdate):
		epoch = time.mktime(time.strptime(birthdate, '%Y-%m-%d'))
		return (now - epoch) / 60 / 60 / 24 /365 >= 30

	f = lambda x: is_above_thirty(x[0])

	print(len(list(filter(f, birthdates)))) 

	# Prints 2,852
```

### Bonus Data Exercise

Describe any potential concerns with either the data itself or the design of the database.

Answer: 
+ **Time complexity**: It is agreed that using multiple JOIN opeartions with SQL significantly affects the effectiveness of data retrieval. For instance, the time complexity of data exercise 2 is O(n^3). The creation of every many-to-many relationship table is not necessarily needed and, in turn, avoiding this could be one solution. In the exercise, having the **encounter_diagnosis** table seems redundant. If the **encounter** table keeps **diagnosis_id** as a foreign key, the time complexity decreases to O(n^2).