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
	"""
	Dunnに知り合いが増えた場合
	UPDATE users
	SET num_friends = 3
	WHERE user_id = 1;
	"""

	def update(self, predicate = lambda row: True):
		for row in self.rows:
			if predicate(row):
				for column, new_value in updates.items():
					row[column] = new_value

	users.update({'num_friends' : 3}, lambda row: row['user_id'] == 1)#user_id == 1の行だけnum_friends = 3にする


#行の削除
	"""
	全ての行を削除
	DELETE FROM users;
	"""

	"""
	特定の行だけを削除する
	DELETE FROM users WHERE user_id = 1;
	"""

	def delete(self, predicate = lambda row: True):
		#全ての行、またはpredicateが指定された場合はそれに合致するものを削除する
		self.rows = [row for row in self.rows if not (predicate(row))]

		user.delete(lambda row: row["user_id"] == 1)#user_id == 1の行だけを削除する
		user.delete()#全ての行を削除する


#行の問い合わせ
	"""
	SELECT * FROM users;							#全ての中身を取り出す
	SELECT * FROM users LIMIT 2;					#最初の2行だけ取り出す
	SELECT user_id FROM users;						#特定の列のみを取り出す
	SELECT user_id FROM users WHERE name = 'Dunn'	#特定の行のみを取り出す
	
	SELECT LENGTH(name) AS name_length FROM users;	#列の値を使った計算も可能
	"""

	def select(self, keep_columns = None, additional_columns = None):
		#列が指定されていなければ全ての、列を返す
		if keep_columns is None:
			keep_columns = self.columns

		if additional_columns is None:
			additional_columns = {}

		result_table = Table(keep_columns + additional_columns.keys())

		for row in self.rows:
			new_row = [row[column] for column in keep_columns]
			for column_name, calculation in additional_columns.items():
				new_row.append(calculation(row))
			result_table.insert(new_row)

		return result_table

	def where(self, predicate = lambda row: True):
		#指定したpreditcateに合致した行だけ返す
		where_table = Table(self.columns)
		where_table.rows = filter(predicate, self.rows)

		return where_table


	def limit(self, num_rows):
		#先頭から一致した行数だけを返す
		limit_table = Table(self.columns)
		limit_table.rows = self.row[:num_rows]

		return limit_table

	#SELECT * FROM users;
	users.select()
	#SELECT * FROM users LIMIT 2;
	users.limit(2)
	#SELECT user_id FROM users;
	users.select(keep_columns = ['user_id'])
	#SELECT user_id FROM users WHERE name = "Dunn"
	users.where(lambda row: row["name"] == "Dunn") \
		 .select(keep_columns = ["user_id"])

	#SELECT LENGTH(name) AS name_length FROM users:
	def name_length(row): return len(row["name"])

	users.select(keep_columns = [], additional_columns = { "name_length" : name_length})


#グループ化
	"""
	SELECT LENGTH(name) as name_lenght, MIN(user_id) AS min_users, COUNT(*) AS num_users FROM users GROUP BY LENGTH(name);
	
	SELECT SUBSTR(name, 1, 1) AS first_letter, AVG(num_friends) AS avg_num_friends FROM users GROUP BY SUBSTR(name, 1, 1) HAVING AVG (num_friemds) > 1;

	SELECT SUM(user_id) as user_id_sum FROM users WHERE user_id > 1;
	"""
