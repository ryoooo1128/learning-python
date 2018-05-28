import math, random, re
from collections import defaultdict, Counter, deque
from data_science_04 import dot, get_row, get_column, make_matrix, magnitude, scalar_multiply, shape, distance
from functools import partial


users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
]

friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]



#ネットワーク分析

#ユーザーの辞書に知り合いのリストを追加
 for user in users:
 	user["friends"] = []

 for i, j in friendships:
 	users[i]["friends"].append(users[j])#iの友人にjを追加
 	users[j]["friends"].append(users[i])#jの友人にiを追加


#媒介中心性
def sortest_paths_from(form_users):
	#指定のユーザーに至るまでの最短経路を保持する辞書
	sortest_paths_to = { form_users["id"] : [[]]}

	#確認すべきユーザーを(前のユーザー, 今のユーザー)形式でキューに入れる
	#開始時点では(from_user, from_userの知り合い)組みの全てを持たせる
	frontier = deque((from_user, friend) for friend in from_user["friends"])

	#キューに値がある限り続ける
	while fronter:
		prev_user, user = frontier.popleft()#最初の要素を取り出し
		user_id = user["id"]#キューから削除する

		#キューへの値追加方法により、必然的に「前のユーザー」までの最短経路は既知である
		paths_to_prev_user = shortest_paths_to[prev_user["id"]]
		new_paths_to_user = [path + [user_id] for path in paths_to_prev_user]

		#最短経路が既知である可能性
		old_paths_to_user = shortest_paths_to.get(user_id, [])

		#ここに至る最短経路は既知であるか
		if old_paths_to_user:
			min_path_length = len(old_paths_to_user[])
		else:
			min_path_length = float('inf')

		#その経路の長さがこれまでのもの以下で、新しいものであった場合のみリストに加える
		new_paths_to_user = [path for path in new_paths_to_user
							 if len(path) <= min_path_length and path not in old_paths_to_user]

		#frontierキューに新しく見つけた知り合いだけを加える
		fronteir.extend((user, freind) for freind in user["friends"] if friends["id"] not in shortest_paths_to)

	return sortest_paths_to

#得られた結果を各ユーザーごとに保存しておく
for user in users:
	user["shortest_paths"] = shortest_path_from(user)

#中心媒介性を求める
for user in users:
	user["betweenness_certainlity"] = 0.0

for source in users:
	source_id = source["id"]
	for target_id, paths in source["shortest_paths"].items():
		if source_id < target_id:#二重計上を防ぐため
			num_paths = len(paths)#最短距離をいくつ持つか
			contrib = 1 / num_paths#中心性に対する貢献度
			for path in paths:
				for id in [source_id, target_id]:
					users[id]["betweenness_certainlity"] += contrib


#近接中心性
def farness(user):
	return sum(len(paths[0]) for paths in user["shortest_paths"].values())

for user in users:
	user["closest_certainlity"] = 1 / farness(user)

	