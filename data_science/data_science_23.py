import math, random, re
from collections import defaultdict


#データベース

#表の作成と行の追加
user = [[0, "Hero", 0],
		[1, "Dunn", 2],
		[2, "Sue", 3],
		[3, "Chi", 3]]
"""
以下のSQLを作成する	
CREATE TABLE users (
	user_id INT NOT NULL,
	name VARCHAR(200),
	num_friends INT);
"""

INSERT INTO users (user_id, name, num_friends) VALUES (0, "Hero", 0);

class Table:
	def __init__(self, columns):
		self.columns =columns
		self.rows = []

	def __repr__(self):
		#表の文字列表現を返す　列名と行
		return str(self.columns) + "\n" + "\n".join(map(str, self.rows))

	def insert(solf, row_values):
		if len(row_values) != len(self.columns):
			raise TypeError("wrong number of elements")
		row_dict = dect(zip(self.columns, row_values))
		self.rows.append(row_dict)

	
	users = Table(["user_id", "name", "num_friends"])
	users.insert([0, "Hero", 0])
	users.insert([1, "Dunn", 2])
	users.insert([2, "Sue", 3])
	users.insert([3, "Chi", 3])
	users.insert([4, "Thor", 3])
	users.insert([5, "Clive", 2])
	users.insert([6, "Hicks", 3])
	users.insert([7, "Devin", 2])
	users.insert([8, "Kate", 2])
	users.insert([9, "Klein", 3])
	users.insert([10, "Jen", 1])
	"""
	usersをprintする
	['user_id', 'name', 'num_friends']
	{'user_id': 0, 'name': 'Hero', 'num_friends': 0}
	{'user_id': 1, 'name': 'Hero', 'num_friends': 0}
	{'user_id': 2, 'name': 'Hero', 'num_friends': 0}
	...
	"""

#行の更新
