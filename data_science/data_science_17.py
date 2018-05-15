from collections import Counter, defaultdict
from functools import partial
import math, random


#決定木

#エントロピー
def entropy(class_probabilities):
	return sum(-p * math.log(p, 2) for p in class_probabilities if p)#p=0の時は計算しない

def class_probabilities(labels):
	total_count = len(labels)
	return [count / total_count for count in Counter(labels).values()]

def data_entropy(labeled_data):
	labels = [label for _, label in labeled_data]
	probabilities = class_probabilities(labels)

	return entropy(probabilities)


#分割のエントロピー

#データを部分に分割した場合のエントロピーを求める
#部分集合は、ラベル付けされたデータリストのリスト
def partition_entropy(subsets):
	total_count = sum(len(subset) for subset in subsets)
	return sum(data_entropy(subset) * len(subset) / total_count for subset in subsets)


#決定木の作成
inputs = [
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'no'},   False),
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'yes'},  False),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'no'},     True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'no'},  True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'yes'},    False),
        ({'level':'Mid','lang':'R','tweets':'yes','phd':'yes'},        True),
        ({'level':'Senior','lang':'Python','tweets':'no','phd':'no'}, False),
        ({'level':'Senior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'yes','phd':'no'}, True),
        ({'level':'Senior','lang':'Python','tweets':'yes','phd':'yes'},True),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'yes'},    True),
        ({'level':'Mid','lang':'Java','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'yes'},False)
    ]

#inputs=(属性辞書, ラベル)
#keyを属性、値をinputとする辞書を作る
def partiton_by(inputs, attribute):
	return group_by(inputs, lambda x: x[0][attribute])

#分割したもののエントロピーを計算する
def partition_entropy_by(inputs, attribute):
	partitions = partition_by(inputs, attribute)
	return partition_entropy(partitions.values())

#エントロピーが最小になる方法を探す
for key in ['level', 'lang', 'tweets', 'phd']:
	print(key, partition_entropy_by(inputs, key))
"""
level: 0.693536138896
lang: 0.860131712855
tweets: 0.788450457308
phd: 0.892158928262

よってlevelで分割するとエントロピーが最小になることがわかる
"""

#Seniorは結果がTrueとFalseの人がいるため、さらに分割する
senior_inputs = [(input, label) for input, label in inputs if input["level"] == ["Senior"]]

for key in ['lang', 'tweets', 'phd']:
	print(key, partition_entropy_by(senior_inputs, key))
"""
lang: 0.4
tweets: 0.0
phd: 0.950977500433

tweetsでは完全にTrueとFalseを分けられる
"""


#まとめて、実装する
"""
決定木は以下になる
('level',
	{'Junior' : ('phd', {'no' : True, 'yes' : False}),
		'Mid' : True,
			'Senior' : ('tweets', {'no' : False, 'yes' : True})})
"""

def classify(tree, input):

	#末端ノードであれば、その値を返す
	if tree in [True, False]:
		return tree

	#そうでなければ決定木は、分類を行う属性と、その属性の値と、次に適用する決定木の辞書の、タプルである
	attribute, subtree_dict = tree

	subtree_key = input.get(attribute)#その属性が存在しなければNoneが返る

	if subtree_key not in subtree_dict:#辞書にその属性が入っていなかったらNoneが返る
		subtree_key = None

	subtree = subtree_dict[subtree_key]
	return classfy(subtree, input)


def build_tree_id3(inputs, split_candidates = None):

	#初回は入力全てのkeyを分割の候補とする
	if split_candidates = None:
		split_candidates = inputs[0][0].key()

	#入力中のTrueとFalseの数を数える
	num_inputs = len(inputs)
	num_trues = len([label for item, label in inputs if label])
	num_falses = num_point - num_trues

	if num_trues == 0: return False#Trueが存在しなければ、Falseの末端ノードを返す
	if num_falses == 0: return True#Falseが存在しなければ、Trueの末端ノードを返す

	#分割候補が存在しなければ、TrueかFalseの多い方を返す
	if not split_candidates:
		return num_trues >= num_falses

	#そうでなければ最良の属性を使って分割する
	best_attribute = min(split_candidates, key = partial(partition_entropy_by, inputs))

	partitions = partition_by(inputs, best_attribute)
	new_candidates = [a for a in split_candidates if a != best_attribute]

	#再度部分木を作成する
	subtrees = { attribute_value : build_tree_id3(subset, new_candidates) for attribute_value, subset in partitions.items()}

	suntrees[None] = num_trues > num_falses#TrueかFalseがNoneの時は一般的な方を使う

	return (best_attribute, subtrees)


#学習データにないものにはどのように働くか
tree = build_tree_id3(inputs)
classify(tree, {'level' : 'Junior', 'lang' : 'Java', 'tweets': 'yes', 'phd' : 'no'})#True
classify(tree, {'level' : 'Junior', 'lang' : 'Java', 'tweets' : 'yes', 'phd' : 'yes'})#False

#属性が欠けている、存在しない時
classify(tree, {'level' : 'Intern'})#True
classify(tree, {'level' : 'Senior'})#False



#ランダムフォレスト







