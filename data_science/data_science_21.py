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
