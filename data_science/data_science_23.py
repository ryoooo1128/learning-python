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
	def group_by(self, group_by_columns, aggregates, having = None):
		grouped_rows = defaultdict(list)

		#グループを追加する
		for row in self.rows:
			key = tuple(row[column] for column in group_by_columns)
			grouped_rows[key].append(row)

		#出力用の表はgroup_byで指定した列と集約値の列をもつ
		result_table = Table(group_by_columns + aggregates.keys())

		for key, rows in grouped_rows.items()
			if having is None or having(rows):
				new_row = list(key)
				for aggregate_name, aggregate_fn in aggregates.items():
					new_row.append(aggregate_fn(rows))
				result_table.insert(new_row)

		return result_table

	def min_user_id(rows): return min(row["user_id"] for row in rows)

	stats_by_length = user \
		.selsct(additional_columns = {"name_length" : name_length} ) \
		.group_by(group_by_columns = ["name_length"], aggregates = {"min_users_id" : min_user_id, "num_min" : len })


	#最初の一文字ごとの知り合いの数
	def first_letter_of_name(row):
		return row["name"][0] if row["name"] else ""

	def average_num_friends(rows):
		return sum(row["num_friend"] for row in rows) / len(rows)

	def enough_friends(rows):
		return average_num_friends(rows) > 1

	avg_freinds_by_letter = user \
		.select(additional_columns = { "first_letter" : first_letter_of_name}) \
		.group_by(group_by_columns = ['first_letter'], aggregates = { "avg_num_friends" : average_num_friends }, having = enough_friends)


	#user_idの合計
	def sum_user_ids(rows): return sum(row["user_id"] for row in rows)

	user_id_sum = user \
	.where(lambda row: row["user_id"] > 1) \
	.group_by(group_by_columns = [], aggregates = { "user_id_sum" : sum_user_ids })



#並び替え
	"""
	SELECT * FROM users
	ORDER BY name
	LIMIT 2;
	"""
	def order_by(self, order):
		new_table = self.selsct() #コピーを作成
		new_table.rows.sort(key = order)

		return new_table

	friendliest_letters = avg_freinds_by_letter \
		.order_by(lambda row; -row["avg_num_friends"]) \
		.limit(4)


#結合
	"""
	CREATE TABLE user_interests (user_id INT NOT NULL, interest VARCHAR(100) NOT FULL);
	"""
	user_interests = Table(["user_id", "interest"])
	user_interests.insert([0, "SQL"])
	user_interests.insert([0, "NoSQL"])
	user_interests.insert([2, "SQL"])
	user_interests.insert([2, "MySQL"])

	"""
	INNER JOIN：合致した行だけを返す　SQLに興味のあるユーザーの見つけ方
	SELECT user.name
	FROM users
	JOIN user_interests
	ON users.user_id = user_interests.user_id
	WHERE user_interests.interest ="SQL"

	LEFT JOIN：合致しなかった行も返す
	SELECT user_id, COUNT(user_interests.interest) AS num_interests
	FROM users
	LEFT JOIN user_interests
	ON users.user_id = user_imterests.user_id
	"""
	def join(self, other_table, left_join = False):
		#両方の表に存在する列
		join_on_columns = [c for c in self.columns if c in other_table.columns]
		#右側の表にのみ存在する列
		additional_columns = [c for c in other_table.columns if c not in join_on_columns]

		#左側にある全ての列と右側の表だけにある列
		join_table = Table(self.columns + additional_columns)

		for row in self.row:
			def is_join(other_table):
				return all(other_row[c] == row[c] for c in join_on_columns)

			other_rows = other_table.where(is_join).rows

			#結合先の表の中で、この表の行と合致したものが結果になる
			for other_row in other_rows:
				join_table.insert([row[c] for c in self.columns] + [other_row[c] for c in additional_columns])

			#合致した行が存在せず、これがLIFT JOINだった場合、Noneが返る
			if left_join and not other_rows:
				join_table.insert([row[c] for c in self.columns] + [None for c in additional_columns])

		return join_table

	sql_users = users \
		.join(user_interests, left_join = True)
		.where(lambda row: row["interest"] == "SQL")
		.select(keep_columns = ["name"])

	def count_interests(rows):
		#Noneではない興味の数を数える
		return len([row for row in rows if rows if row["interest"] is not None])

	user_interest_count = users \
		.join(user_interests, left_join = True) \
		.group_by(group_by_columns = ["user_id"], aggregates = { "num_interests" : count_interests })

#サブクリエ
	"""
	SELECT MIN(user_id) AS min_user_id FROM
	(SELECT user_id FROM user_interests WHERE interest = "SQL") sql_interests;
	"""
	likes_sql_user_ids = user_interests \
		.where(lambda row: row["interest"] == "SQL") \
		.select(keep_columns = ["user_id"])

	likes_sql_user_ids.group_by(group_by_columns = [], aggregates = { "min_user_id" : min_user_id })


#クリエ最適化
	"""
	SELECT users.name
	FROM users
	JOIN user_interests
	ON users.user_id = user_interests.user_id
	WHERE user_interests.interest = "SQL"
	"""
	#結合する前に要素を取り出しておく
	user_interests \
		.where(lambda row: row["interest"] == "SQL") \
		.join(users) \
		.select(["name"])
	#結合結果から必要なものを選択する方法
	user_interest \
		.join(users) \
		.where(lambda row: row["interest"] == "SQL") \
		.select(["name"])

