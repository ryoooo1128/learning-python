import math, random
from collections import defaultdict, Counter
from data_science_04 import dot

users_interests = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]


#リコメンドシステム

#人気が高いものをリコメンドする
popular_interests = Counter(interest for user_interests in users_interests for interests in user_interests).most_common()
"""
結果
[('Python', 4), ('R', 4), ('Java', 3), ('regression', 3), ('statistics', 3), ('probability', 3), ...]
"""

def most_popular_new_interests(user_interests, max_results = 5):
    suggestions = [(interests, frequency) for interest, frequency in popular_interests
                    if interest not in user_interests]
    return suggestions[:max_results]

"""
ユーザー１は既に次の興味を持っている
["NoSOL", "MongoDB", "Cassandra", "HBase", "Postgres"]
よって
most_popular_new_interests(user_interests[1], 5)
#[('Python', 4), ('R', 4), 'Java', 3), ('regression', 3), ('statistics', 3)]
"""

"""
ユーザー３は
[('Java', 3), ('HBase', 3), ('Big Data', 3), ('neural networks', 2), ('Hadoop', 2)]
"""


#ユーザーベース協調フィルタリング

#コサイン類似度
def cosine_similarity(v, w):
    return dot(v, w) / math.squt(dot(v, v) * dot(w, w))

unique_interests = sorted(list({ interest for user_interests in users_interests for interest in user_interests}))
#['Big Data', 'C++', 'Cassandra', 'HBasa', 'Hadoop', 'Haskell', ...]

def make_user_interest_vector(user_interests):#興味を持ってれば1、持っていなければ0のベクトルを作る
    return [1 if interest in user_interests else 0 for interest in unique_interests]

user_interest_matrix = map(make_user_interest_vector, user_interests)

#全てのユーザーの類似度を計算
user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                     for interest_vector_j in user_interest_matrix] for interest_vector_i in user_interest_matrix]

def most_similar_users_to(user_id):
    #類似度が0以外のユーザーを検索する
    pairs = [(other_user_id, similarity)
             for other_user_id, similarity in enumerate(user_similarities[user__id])
             if user_id != other_user_id and similarity > 0]

    return sorted(pairs, key = lambda ( , similarity): similarity, reverse = True)

"""
most_similar_users_to(0)
[(9, 0.5669467095138409),
 (1, 0.3380617018914066),
 (8, 0.1889822365046136),
 (13, 0.1690308509457033),
 (5, 0.1543033499620919)]
"""

#これを生かしてリコメンドする
def user_based_suggestions(user_id, include_current_interests = False):
    #類似度を加算
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_to):
        for interest im user_interests[other_user_id]:
            suggestions[interest] += similarity

    #リストをソートする
    suggestions = sorted(suggestions.items(), key = lambda (_, weight): weight, reverse = True)

    #おそらく既に興味として持っているものを除く
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) for suggestion, weight in suggestions if suggestion not in user_interests[user_id]]

"""
user_based_suggestions(0)
[('MapReduce', 0.566694670905138409),
 ('MongoDB', 0.50709255283711),
 ('Postgres', 0.50709255283711),
 ('NoSQL', 0.3380617018914066),
 ('neural networks', 0.1889822365046136),
 ('deep learning', 0.1889822365046136),
 ('artificial intelligence', 0.1889822365046136),
 ...]
"""


#アイテムベース協調フィルタリング

interest_user_matrix = [[user_interest_vector[j] for user_interest_vector in user_interest_matrix]
                        for j, _ in enumerate(unique_interests)]
"""
Big Dataの場合
interst_user_matrix[0] = [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
"""

interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                         for user_vector_j in interest_user_matrix]
                         for user_vector_i in interest_user_matrix]

def most_similar_interests_to(interest_id):
    similarities = interest_similarities[interest_id]
    pairs = [(unique_interests[others_interest_id], similarity) for others_interest_id, similarity in enumerate(similarities)
             if interest_id != other_interest_id and similarity > 0]

    return sorted(pairs, key = lambda (_, similarity): similarity, reverse = True)

"""
類似度の結果
[('Hadoop', 0.8164965809277261),
 ('Java', 0.6666666666666666),
 ('MapReduce', 0.5773502691896258),
 ('Spark', 0.5773502691896258),
 ('Storm', 0.5773502691896258),
 ('Cassandra', 0.4082482904638631),
 ('artificial intelligence', 0.4082482904638631),
 ('deep learning', 0.4082482904638631),
 ('neural networks', 0.4082482904638631),
 ('HBase', 0.3333333333333333)]
"""

#これを使って興味を持っている分野の類似度をユーザーごとに合計する
def item_based_suggestions(user_id, include_current_interests = False):
    #持っている興味に対する類似の分野の類似度を比較する
    suggestions = defaultdict(float)
    user_interest_vector = user_interest_matrix[user_id]
    for interest_id, is_interested in enumerate(user_interest_vector):
        if is_interested == 1:
            similar_interests = most_similar_interests_to(interested_id)
            for interest, similarity in similar_interests:
                suggestions[interest] += similarity

    #類似度の合計でソートする
    suggestions = sorted(suggestions.item(), key = lambda (_, similarity): similarity, reserve = True)

    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) for suggestion, weight in suggestions if suggestion not in user_interests[user_id]]

"""
ユーザー0へのおすすめ
[('MapReduce', 1.861807319565799),
 ('Postgres', 1.3164965809277263),
 ('MongoDB', 1.3164965809277263),
 ('NoSQL', 1.2844570503761732),
 ('programming languages', 0.5773502691896258),
 ('MySQL', 0.5773502691896258),
 ('Haskell', 0.5773502691896258),
 ('database', 0.5773502691896258),
 ('neural networks', 0.4082482904638631),
 ('deep learning', 0.4082482904638631),
 ('C++', 0.4082482904638631),
 ('artificial intelligence', 0.4082482904638631),
 ('Python', 0.2886751345948129),
 ('R', 0.2886751345948129)]
"""

